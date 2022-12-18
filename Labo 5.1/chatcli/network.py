import os

from twisted.protocols.basic import LineReceiver, FileSender
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor


class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.EOL = '\r\n'

    def lineReceived(self, line):
        line = line.decode('utf-8')
        self.factory.gui.print_debug(line)

        if line.startswith('INN'):
            if line[3:]:
                self.factory.user_in(line[3:])
            else:
                self.factory.gui.print_debug_info('User not provided')

        elif line.startswith('FTR'):
            features = line[3::2]
            if len(features) == 4:
                features = [bool(int(feature)) for feature in features]
                self.factory.features_received(features)
            else:
                self.factory.gui.print_debug_info('Incorrect features')

        elif line.startswith('MSG'):
            sender, message = line[3:].split(' ', 1)
            if sender in self.factory.users and message:
                self.factory.message_received(sender, message)
            elif not sender:
                self.factory.gui.print_debug_info('User not provided')
            elif sender not in self.factory.users:
                self.factory.gui.print_debug_info('User unknown')
            else:
                self.factory.gui.print_debug_info('Message not provided')

        elif line.startswith('USR'):
            self.factory.user_list_received(line[3:].split())
            self.send_command('NME', self.factory.username)

        elif line.startswith('OUT'):
            username = line[3:]
            if username in self.factory.users:
                self.factory.user_out(username)
            elif not username:
                self.factory.gui.print_debug_info('Username not provided')
            else:
                self.factory.gui.print_debug_info('User unknown')

        elif line.startswith('NOP'):
            self.factory.nop_received()

        elif line.startswith('WRT'):
            self.factory.wrt_received(line[3:])

        elif line.startswith('FIL'):
            sender, file_code, file_name = line[3:].split(' ', 2)
            if sender in self.factory.users and len(file_code) == 5 \
                    and file_name:
                self.factory.fil_received(sender, file_code, file_name)
            elif not sender:
                self.factory.gui.print_debug_info('User not provided')
            elif sender not in self.factory.users:
                self.factory.gui.print_debug_info('User unknown')
            elif len(file_code != 5):
                self.factory.gui.print_debug_info('Incorrect file code')
            else:
                self.factory.gui.print_debug_info('File name not provided')

        elif line.startswith('+'):
            if self.lastCommand == "TLS":
                self.factory.set_tls()
            elif self.lastCommand == "PUT":
                self.factory.send_file_data()
            elif self.lastCommand == "GET":
                file_size = line[1:]
                if not file_size:
                    self.factory.gui.print_debug_info('No file size received')
                try:
                    file_size = int(file_size)
                except ValueError:
                    self.factory.gui.print_debug_info('Incorrect file size')
                else:
                    if file_size < 0:
                        self.factory.gui.print_debug_info('Negative file size')
                    elif self.factory.gui.get_file_confirmation(file_size):
                        self.file_data = b''
                        self.file_size = file_size
                        self.send_command('SND')
                        self.setRawMode()
                    else:
                        self.send_command('RST')

        elif line.startswith('-'):
            code = line[1:]
            if code:
                self.factory.error_received(int(code))
            else:
                self.factory.gui.print_debug_info('Error code not provided')

    def send_command(self, command, parameters='', EOL=True):
        msg = command + parameters
        if EOL:
            msg += self.EOL
        self.transport.write(msg.encode('utf-8'))
        self.lastCommand = command

    def rawDataReceived(self, data):
        self.file_data += data
        self.file_size -= len(data)
        if self.file_size <= 0:
            self.factory.file_data_received(self.file_data)
            self.setLineMode()


class ChatClient(ClientFactory):
    def __init__(self, gui):
        self.gui = gui
        self.ERROR_STRINGS = (
            'Unknown or unexpected command.',
            'The room is full.',
            'Username has forbiden characters.',
            'Username is too long.',
            'There is someone with this name in the room.',
            'The message is too long.',
            'Undefined error.',
            'The message is incorrect.',
            'The file is too big.',
            'The file code is not valid.'
        )

    def open_connection(self, server, port, username):
        self.username = username
        reactor.connectTCP(server, port, self)

    def finish(self):
        reactor.stop()

    def send_message(self, msg):
        self.protocol.send_command('MSG', msg)

    def send_typing(self):
        if self.features['CEN']:
            self.protocol.send_command('WRT')

    def ask_tls(self):
        if self.features['TLS']:
            self.protocol.send_command('TLS')

    def send_file(self, file_name):
        self.file_name = file_name
        file_size = os.path.getsize(file_name)
        parameters = '{} {}'.format(file_size, os.path.basename(file_name))
        self.protocol.send_command('PUT', parameters)

    def send_file_data(self):
        fh = open(self.file_name, 'rb')

        def file_transferred(_):
            self.gui.write_own_file(self.username,
                                    os.path.basename(self.file_name))
            fh.close()

        def finish(_):
            if not fh.closed:
                fh.close()

        def error(e):
            self.gui.print_debug_info('Error sending the file')

        sender = FileSender()
        d = sender.beginFileTransfer(fh, self.protocol.transport)
        d.addCallbacks(file_transferred, finish)
        d.addErrback(error)

    def ask_file(self, code):
        self.protocol.send_command("GET", code)

    def close_connection(self):
        self.protocol.transport.loseConnection()
        self.gui.close_connection()

    def user_in(self, username):
        self.users.append(username)
        self.gui.add_user_to_list(username)
        self.gui.print_info(username + ' entered the room.')

    def user_out(self, username):
        self.users.remove(username)
        self.gui.clear_user_list()
        for user in self.users:
            self.gui.add_user_to_list(user)
        self.gui.print_info(username + ' left the room.')

    def user_list_received(self, usernames):
        self.users = usernames
        for username in usernames:
            self.gui.add_user_to_list(username)

    def features_received(self, features):
        self.features = {}
        self.features['FILE'] = features[0]
        self.features['CEN'] = features[1]
        self.features['NOP'] = features[2]
        self.features['TLS'] = features[3]
        self.gui.enable_features(self.features)

    def message_received(self, sender, msg):
        self.gui.write_message(sender, msg)

    def nop_received(self):
        if self.features['NOP']:
            self.gui.set_nop()

    def wrt_received(self, username):
        if self.features['CEN']:
            self.gui.print_info(username + ' is typing.')

    def fil_received(self, sender, file_code, file_name):
        if self.features['FILE']:
            self.gui.write_file(sender, file_name, file_code)

    def file_data_received(self, data):
        self.gui.file_received(data)

    def set_tls(self):
        if self.features['TLS']:
            # Imports are here so the libraries aren't needed unless the
            # server implements the functionallity.
            from twisted.internet import ssl
            from OpenSSL import SSL

            class ClientTLSContext(ssl.ClientContextFactory):
                def getContext(self):
                    return SSL.Context(SSL.TLSv1_METHOD)

            ctx = ClientTLSContext()
            self.protocol.transport.startTLS(ctx, self)
            self.gui.set_tls()
            self.gui.print_info('Changed to TLS secure communication.')

    def error_received(self, error_code):
        if error_code < len(self.ERROR_STRINGS):
            self.gui.print_info(self.ERROR_STRINGS[error_code])
            if error_code == 3 or error_code == 4:
                self.close_connection()
        else:
            self.factory.gui.print_debug_info('Unknown error code')

    def buildProtocol(self, addr):
        self.protocol = ChatProtocol(self)
        return self.protocol

    # def clientConnectionLost(self, connector, reason):
    #     connector.connect()
    #
    # def clientConnectionFailed(self, connector, reason):
    #     reactor.stop()
