#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        if len(self.users)>=MAX_USER: 
            message = "1\r\n"
            self.sendLine(message.encode())
            self.transport.loseConnection()
        else:
            message = "FTR0 0 0 0\r\n"
            self.sendLine(message.encode())
            message = "USR" + self.users
            for key in self.factory.users.keys():
                users += self.factory.users[key].name + " "
            self.sendLine(users.encode())             

    def connectionLost(self, reason):
        if self.name != None:
            del self.factory.users[self.name]
            
        message = "OUT" + self.name
        for user in self.factory.users.values():
            user.sendLine(message.encode())

    def lineReceived(self, line):
        line = line.decode()
        if line.startwith("NME") and not self.name:
            name = line[3:]
            # Nombre no adecuado
            # Caracteres prohubidos
            caracteres_prohibidos="# | & | $ | < | >"
            if caracteres_prohibidos in name:
                message="2. Contiene caracteres prohubidos \r\n "
                self.sendLine(message.encode())
                #self.transport.loseConnection()
            # Nombre demasiado largo
            elif len(name)>MAX_USER_LENGTH:
                message="3. Nombre demasiado largo \r\n "
                self.sendLine(message.encode())
                #self.transport.loseConnection()
            # Si ya hay alguien 
            elif name in self.factory.users.keys() :
                message="4. Ya hay alguien con ese nombre \r\n "
                self.sendLine(message.encode())
                #self.transport.loseConnection()
            else:
                self.name = name
                # features['nueva']=1
                # users[usuario] = self
                self.factory.users[self.name] = self
                
            
                message = "INN" + self.name
                for user in self.factory.users.values():
                    if user != self:
                        user.sendLine(message.encode())
                        
                self.sendLine("+".encode())
            
                
                
                
        elif line.startswith("MSG") and self.name:
            message = line[3:]
            if len(message) > MAX_MSG_LENGTH:
                    message="5. mensaje demasiado largo \r\n "
                    self.sendLine(message.encode())
                    # self.transport.loseConnection()
            else:
                message = "MSG{} {}".format(self.name,message)
                for user in self.factory.users.values():
                    if user != self:
                        user.sendLine(message.encode())
                self.sendLine("+".encode())
            
           

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}
        self.features = { 'FILES':'0' , 'CEN':'0', 'NOP':'0', 'SSL':'0' }

    def buildProtocol(self, addr):
        return ChatProtocol(self)

if __name__ == "__main__":
    reactor.listenTCP(PORT, ChatFactory())
    reactor.run()

 