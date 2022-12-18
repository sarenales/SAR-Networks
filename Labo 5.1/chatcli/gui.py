import os
import configparser
from datetime import datetime
from tkinter import filedialog, Frame, Toplevel, Button, Label, Listbox
from tkinter import StringVar, Entry, scrolledtext, messagebox
from tkinter import SOLID, BOTH, SUNKEN, FLAT, W, E, N, S, DISABLED, END, \
                    NORMAL, ACTIVE, LEFT, RIGHT, CENTER, INSERT
from PIL import Image, ImageTk

import network


class Configuration():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('cfg/config.ini')

    def get_values(self):
        if not self.config['DEFAULT']['server'] or \
           not self.config['DEFAULT']['port'] or \
           not self.config['DEFAULT']['username'] or \
           not self.config['DEFAULT']['icon']:
            return(self.create_default())
        else:
            return(self.config['DEFAULT'])

    def create_default(self):
        path = './cfg'

        try:
            os.mkdir(path)
        except OSError:
            pass

        self.config['DEFAULT'] = {'server': 'localhost',
                                  'port': '8000',
                                  'username': 'szasar',
                                  'icon': 'cfg/default.jpg'}
        with open('cfg/config.ini', 'w') as configfile:
            self.config.write(configfile)

        return(self.config['DEFAULT'])

    def change_icon(self):
        path = filedialog.askopenfilename(title='Select file',
                                          filetypes=(('jpeg files', '*.jpg'),
                                                     ('all files', '*.*')))
        self.config['DEFAULT']['icon'] = os.path.relpath(path)

    def apply_conf(self):
        self.config['DEFAULT']['server'] = self.server.get()
        self.config['DEFAULT']['port'] = self.port.get()
        self.config['DEFAULT']['username'] = self.username.get()
        with open('cfg/config.ini', 'w') as configfile:
            self.config.write(configfile)
        self.conf_window.destroy()

    def close_window(self):
        self.conf_window.destroy()

    def ask_config(self, root):
        root.update()
        self.conf_window = Toplevel()
        w = root.winfo_width()
        h = root.winfo_height()
        x = root.winfo_x()
        y = root.winfo_y()
        x = x + (w/4)
        y = y + (h/4)
        self.conf_window.geometry('+%d+%d' % (x, y))
        self.conf_window.wm_title('Configuration')
        self.conf_window.config(bg='black')

        frame = Frame(self.conf_window, bg='black')
        frame.pack(fill=BOTH, expand=True)

        Frame(frame, width=1, bd=1, relief=SUNKEN)
        Frame(frame, width=1, bd=1, relief=SUNKEN)
        fr_config = Frame(frame, bg='black', borderwidth=1,
                          highlightbackground='white', relief=FLAT)
        fr_config.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)
        fr_conf = Frame(frame, bg='black', borderwidth=1,
                        highlightcolor='gray40', bd=0,
                        highlightbackground='gray40',
                        highlightthickness=1, relief=SOLID)
        fr_conf.grid(row=1, column=0, rowspan=2, padx=5, pady=5)
        fr_bt = Frame(frame, bg='black', borderwidth=1,
                      highlightbackground='white')
        fr_bt.grid(row=0, column=1, rowspan=2, padx=1, pady=5, sticky=N)

        bt_apply = Button(fr_bt, text='Apply', width=6,
                          command=self.apply_conf)
        bt_apply.grid(row=1, column=1, sticky=N+E, pady=2, padx=1)
        bt_apply.config(relief=FLAT, bg='gray20', fg='white', borderwidth=0,
                        highlightthickness=0)

        bt_cancel = Button(fr_bt, text='Cancel', width=6,
                           command=self.close_window)
        bt_cancel.grid(row=2, column=1, sticky=S+E, pady=2, padx=1)
        bt_cancel.config(relief=FLAT, bg='gray20', fg='white', borderwidth=0,
                         highlightthickness=0)

        conf_values = self.get_values()
        image = Image.open(conf_values['icon'])
        image = image.resize((50, 50), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        lbl_img = Label(fr_config, image=image)
        lbl_img.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=W)
        lbl_username = Label(fr_config, text=conf_values['username'],
                             bg='black', fg='red')
        lbl_username.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        server_port = conf_values['server'] + ':' + conf_values['port']
        lbl_server = Label(fr_config, text=server_port, bg='black', fg='red')
        lbl_server.grid(row=1, column=1, padx=5, pady=5)

        lbl_server = Label(fr_conf, text='Server:', fg='white', bg='black')
        lbl_server.grid(row=1, column=0, padx=5, pady=5, sticky=E)

        self.server = StringVar()
        txt_server = Entry(fr_conf, textvariable=self.server)
        self.server.set(conf_values['server'])
        txt_server.grid(row=1, column=1, padx=5)
        txt_server.config(bg='gray13', fg='white', borderwidth=0,
                          highlightthickness=0, insertbackground='white')

        lbl_port = Label(fr_conf, text='Port:', fg='white', bg='black')
        lbl_port.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.port = StringVar()
        txt_port = Entry(fr_conf, width=5, textvariable=self.port)
        self.port.set(conf_values['port'])
        txt_port.grid(row=2, column=1, padx=5, sticky=W)
        txt_port.config(bg='gray13', fg='white', borderwidth=0,
                        highlightthickness=0, insertbackground='white')

        lbl_username = Label(fr_conf, text='Default username:', fg='white',
                             bg='black')
        lbl_username.grid(row=3, column=0, padx=5, pady=5,  sticky=E)

        self.username = StringVar()
        txt_user = Entry(fr_conf, textvariable=self.username)
        self.username.set(conf_values['username'])
        txt_user.grid(row=3, column=1, padx=5)
        txt_user.config(bg='gray13', fg='white', borderwidth=0,
                        highlightthickness=0, insertbackground='white')

        lbl_image = Label(fr_conf, text='Image:', bg='black')
        lbl_image.grid(row=4, column=0, padx=5, pady=5,  sticky=E)
        lbl_image.config(bg='gray13', fg='white', borderwidth=0,
                         highlightthickness=0)
        bt_choose = Button(fr_conf, text='Choose',  width=6, height=1,
                           command=self.change_icon)
        bt_choose.grid(row=4, column=1, sticky=W, pady=2, padx=5)
        bt_choose.config(relief=FLAT, bg='gray20', fg='white', borderwidth=0,
                         highlightthickness=0)

        self.conf_window.resizable(False, False)
        self.conf_window.transient(root)
        self.conf_window.grab_set()
        self.conf_window.focus_set()
        root.wait_window(self.conf_window)
        return(self.get_values())


class App(object):
    def __init__(self, master):
        self.master = master
        self.network = network.ChatClient(self)
        self.conf = Configuration()
        conf_values = self.conf.get_values()
        self.create_window(master, conf_values)
        self.debug = False

    def config_window(self):
        conf_values = self.conf.ask_config(self.master)
        self.username.set(conf_values['username'])
        self.server.set(conf_values['server'])
        self.port.set(conf_values['port'])
        image = Image.open(conf_values['icon']).resize((40, 40),
                                                       Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.lbl_image.configure(image=self.image)

    def open_connection(self):
        server = self.server.get()
        port = self.port.get()
        username = self.username.get()
        self.network.open_connection(server,
                                     int(port),
                                     username)
        self.disable_connect_button()
        self.disable_conf_button()
        self.disable_conf_info()
        self.enable_message_textbox()

    def close_connection(self):
        self.clear_user_list()
        self.enable_connect_button()
        self.enable_conf_button()
        self.enable_conf_info()
        self.disable_message_textbox()
        self.disable_features()

    def send_message(self, dummy=''):
        '''The dummy parameter ignores the parameter that automatically is
        added when the RETURN is pressed to send a message.'''
        username = self.network.username
        msg = self.txt_msg.get()
        self.txt_msg.delete(0, 'end')
        if not msg.strip():
            return
        self.network.send_message(msg)
        self.write_message(username, msg, True)

    def write_message(self, sender, message, own=False):
        sender_format = 'username' if own else 'sender'
        self.bt_send.config(state=DISABLED)
        now = datetime.now()
        timestamp = now.strftime('%H:%M:%S')
        self.txt_chat.config(state=NORMAL)
        self.txt_chat.insert(END, ' ' + str(sender) + '\n', sender_format)
        self.txt_chat.insert(END, message + ' \n', 'message')
        self.txt_chat.insert(END, timestamp + ' \n', 'timestamp')
        self.txt_chat.insert(END, '\n\n', 'newline')
        self.txt_chat.see(END)
        self.txt_chat.config(state=DISABLED)
        self.txt_chat.focus()

    def write_own_file(self, username, file_name):
        now = datetime.now()
        format = now.strftime('%H:%M:%S')
        self.txt_chat.config(state=NORMAL)
        self.txt_chat.insert(END, ' ' + username + '\n', 'username')
        self.txt_chat.insert(END, 'File sent: ' + file_name + '\n', 'file')
        self.txt_chat.insert(END, format + '  \n', 'timestamp')
        self.txt_chat.insert(END, '\n\n', 'newline')
        self.txt_chat.see(END)
        self.txt_chat.config(state=DISABLED)

    def write_file(self, sender, file_name, code):
        now = datetime.now()
        format = now.strftime('%H:%M:%S')
        self.txt_chat.config(state=NORMAL)
        self.txt_chat.insert(END, ' ' + sender + '\n', 'sender')
        button = Button(self.txt_chat, text='Download', cursor='hand2')
        button.configure(command=(lambda b=button, c=code: self.ask_file(b, c)))
        button.config(relief=FLAT, bg='gray13', fg='white', borderwidth=1,
                      highlightthickness=0)
        self.txt_chat.insert(END, ' ' + file_name + ' ', 'file')
        self.txt_chat.window_create(INSERT, align=CENTER, window=button)
        self.txt_chat.insert(END, '  \n', 'message')
        self.txt_chat.insert(END, format + '  \n', 'timestamp')
        self.txt_chat.insert(END, '\n\n', 'newline')
        self.txt_chat.see(END)
        self.txt_chat.config(state=DISABLED)

    def ask_file(self, button, code):
        self.network.ask_file(code)

    def file_received(self, data):
        with open(self.file_name, 'wb') as fh:
            fh.write(data)

    def enable_send(self, event):
        self.bt_send.config(state=ACTIVE)

    def disable_send(self, event):
        self.bt_send.config(state=DISABLED)

    def add_user_to_list(self, username):
        self.lb_users.insert(END, ' ' + username)

    def clear_user_list(self):
        self.lb_users.delete(0, 'end')

    def enable_features(self, features):
        color = 'green' if features['FILE'] else 'red'
        self.lbl_file['text'] = 'FILE'
        self.lbl_file.config(fg=color)
        if features['FILE']:
            self.bt_file.config(state=NORMAL)

        color = 'green' if features['CEN'] else 'red'
        self.lbl_cen['text'] = 'CEN'
        self.lbl_cen.config(fg=color)

        color = 'green' if features['NOP'] else 'red'
        self.lbl_nop['text'] = 'NOP'
        self.lbl_nop.config(fg=color)

        color = 'green' if features['TLS'] else 'red'
        self.lbl_tls['text'] = 'TLS'
        self.lbl_tls.config(fg=color)
        if features['TLS']:
            self.lbl_tls.bind('<Button-1>', self.request_tls)

    def request_tls(self, event):
        self.network.ask_tls()

    def send_file(self):
        file_name = filedialog.askopenfilename(title='Select file')
        if file_name:
            self.network.send_file(file_name)

    def sizeof_fmt(self, num):
        for unit in ['B', 'KiB', 'MiB', 'GiB']:
            if num < 1024.0:
                return "{:.2f} {}".format(num, unit)
            num /= 1024.0
        return "{:.2f} {}" % (num, 'TiB')

    def get_file_confirmation(self, num_bytes):
        threshold = 2**20 # 1 MiB
        if num_bytes > threshold:
            size = self.sizeof_fmt(num_bytes)
            question = 'The file size is {}. Are you sure you want to '
            question += 'download it?'
            confirmed = messagebox.askyesno('Download confirmation',
                                         question.format(size))
        if num_bytes <= threshold or confirmed:
            file_name = filedialog.asksaveasfilename(title='Select file')
            if file_name:
                self.file_name = file_name
                return True
        return False

    def set_tls(self):
        self.lbl_tls.config(fg='yellow')
        self.lbl_tls.unbind('<Button-1>')

    def disable_features(self):
        self.lbl_file.config(bg='black', fg='black')
        self.lbl_cen.config(bg='black', fg='black')
        self.lbl_nop.config(bg='black', fg='black')
        self.lbl_tls.config(bg='black', fg='black')

    def set_nop(self):
        self.lbl_nop.config(fg='yellow')
        self.master.after(2000, self.unset_nop)

    def unset_nop(self):
        self.lbl_nop.config(fg='green')

    def print_debug(self, info):
        self.debug_info.set(info)
        if self.debug:
            self.lbl_debug.config(fg='green')
            self.master.after(2000, self.reset_debug_color)

    def print_debug_info(self, info):
        original = self.debug_info.get()
        self.debug_info.set(original + ' [' + info + ']')

    def print_info(self, info):
        self.info.set(info)
        self.master.after(2000, self.delete_info)

    def delete_info(self):
        self.info.set('')

    def reset_debug_color(self):
        self.lbl_debug.config(fg='white')

    def toggle_debug(self):
        if self.debug:
            self.lbl_debug.config(background='black', fg='black')
        else:
            self.lbl_debug.config(background='gray13', fg='white')
        self.debug = not self.debug

    def close(self):
        self.network.finish()

    def disable_conf_info(self):
        self.lbl_username.config(fg='green')
        self.txt_username.config(state=DISABLED)
        self.lbl_server.config(fg='green')
        self.txt_server.config(state=DISABLED)
        self.lbl_port.config(fg='green')
        self.txt_port.config(state=DISABLED)

    def enable_conf_info(self):
        self.lbl_username.config(fg='red')
        self.txt_username.config(state=NORMAL)
        self.lbl_server.config(fg='red')
        self.txt_server.config(state=NORMAL)
        self.lbl_port.config(fg='red')
        self.txt_port.config(state=NORMAL)

    def disable_connect_button(self):
        self.bt_connect.config(state=DISABLED)

    def enable_connect_button(self):
        self.bt_connect.config(state=NORMAL)

    def disable_conf_button(self):
        self.bt_config.config(state=DISABLED)

    def enable_conf_button(self):
        self.bt_config.config(state=NORMAL)

    def disable_message_textbox(self):
        self.txt_msg.config(state=DISABLED)

    def enable_message_textbox(self):
        self.txt_msg.config(state=NORMAL)

    def key_pressed(self, event):
        msg = self.txt_msg.get()
        # The pressed key is not appended to msg yet,
        # but can be found in event.char.
        # If a control key is pressed event.char is empty.
        # '\x08' is the backspace character.
        if len(msg) == 0 and event.char and event.char != '\x08':
            self.network.send_typing()

    def create_window(self, master, conf):
        master.geometry('700x500')
        frame = Frame(master)
        frame.config(bg='black')
        master.title('SZA-SAR')
        frame.pack(fill=BOTH, expand=True)

        fr_config = Frame(frame, bg='black', borderwidth=1,
                          highlightbackground='white', relief=FLAT)
        fr_config.grid(row=0, column=0, padx=5, pady=1, sticky=W+E)

        image = Image.open(conf['icon']).resize((40, 40), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.lbl_image = Label(fr_config, image=self.image)
        self.lbl_image.grid(row=0, column=0, rowspan=3, padx=5, pady=5,
                            sticky=W)
        self.username = StringVar()
        self.server = StringVar()
        self.port = StringVar()
        self.lbl_username = Label(fr_config, text='User',
                                  bg='black', fg='red')
        self.lbl_username.grid(row=0, column=1, padx=5, pady=1, sticky=W)
        self.lbl_server = Label(fr_config, text='Server',
                                bg='black', fg='red')
        self.lbl_server.grid(row=1, column=1, padx=5, pady=1, sticky=W)
        self.lbl_port = Label(fr_config, text='Port',
                              bg='black', fg='red')
        self.lbl_port.grid(row=2, column=1, padx=5, pady=1, sticky=W)
        self.txt_username = Entry(fr_config, textvariable=self.username,
                                  bg='black', fg='red', width=10)
        self.txt_username.grid(row=0, column=2, padx=5, pady=1, sticky=W)
        self.txt_server = Entry(fr_config, textvariable=self.server,
                                bg='black', fg='red', width=10)
        self.txt_server.grid(row=1, column=2, padx=5, pady=1, sticky=W)
        self.txt_port = Entry(fr_config, textvariable=self.port,
                              bg='black', fg='red', width=10)
        self.txt_port.grid(row=2, column=2, padx=5, pady=1, sticky=W)
        self.username.set(conf['username'])
        self.server.set(conf['server'])
        self.port.set(conf['port'])

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)
        fr_features = Frame(frame)
        fr_features.config(bg='black')
        fr_features.grid(row=4, column=0, columnspan=1, sticky=W + E,
                         pady=2, padx=5)

        self.lbl_file = Label(fr_features, font='Helvetica 9 bold')
        self.lbl_cen = Label(fr_features, font='Helvetica 9 bold')
        self.lbl_nop = Label(fr_features, font='Helvetica 9 bold')
        self.lbl_tls = Label(fr_features, font='Helvetica 9 bold')
        self.lbl_file.grid(row=0, column=0, columnspan=1, sticky=W + E, pady=2,
                           padx=5)
        self.lbl_file.config(bg='black', fg='white')
        self.lbl_cen.grid(row=0, column=1, columnspan=1, sticky=W + E, pady=2,
                          padx=5)
        self.lbl_cen.config(bg='black', fg='white')
        self.lbl_nop.grid(row=0, column=2, columnspan=1, sticky=W + E, pady=2,
                          padx=5)
        self.lbl_nop.config(bg='black', fg='white')
        self.lbl_tls.grid(row=0, column=3, columnspan=1, sticky=W + E, pady=2,
                          padx=5)
        self.lbl_tls.config(bg='black', fg='white')

        fr_info = Frame(frame, bg='black', borderwidth=1, relief=FLAT)
        fr_info.grid(row=0, column=1, columnspan=2, padx=5, pady=1, sticky=W+E)

        self.info = StringVar()
        self.lbl_info = Label(fr_info, textvariable=self.info, width=80,
                              anchor='w')
        self.lbl_info.grid(row=0, column=0, pady=2, padx=5)
        self.lbl_info.config(background='gray13', fg='white')

        self.debug_info = StringVar()
        self.lbl_debug = Label(fr_info, textvariable=self.debug_info, width=80,
                               anchor='w')
        self.lbl_debug.grid(row=1, column=0, sticky=W+E, pady=2,
                            padx=5)
        self.lbl_debug.config(background='black', fg='black')

        fr_buttons = Frame(frame, bg='black', borderwidth=1,
                           background='black', relief=FLAT)
        fr_buttons.grid(row=0, column=3, columnspan=1, padx=5, pady=1,
                        sticky=W+E)

        self.bt_connect = Button(fr_buttons, text='Connect', width=5,
                                 command=self.open_connection)
        self.bt_connect.grid(row=0, column=0, sticky=E, pady=2, padx=5)
        self.bt_connect.config(relief=FLAT, bg='gray13', fg='white',
                               borderwidth=0, highlightthickness=0)

        self.bt_config = Button(fr_buttons, text='Conf', width=5,
                                command=self.config_window)
        self.bt_config.grid(row=1, column=0, sticky=W+E, pady=2, padx=5)
        self.bt_config.config(relief=FLAT, bg='gray13', fg='white',
                              borderwidth=0, highlightthickness=0)

        self.bt_debug = Button(fr_buttons, text='Debug', width=5,
                               command=self.toggle_debug)
        self.bt_debug.grid(row=0, column=1, sticky=E, pady=2, padx=0)
        self.bt_debug.config(relief=FLAT, bg='gray13',
                             activeforeground='white', fg='white',
                             borderwidth=0, highlightthickness=0)

        self.bt_close = Button(fr_buttons, text='Close', width=5,
                               command=self.close)
        self.bt_close.grid(row=1, column=1, sticky=W+E, pady=2, padx=0)
        self.bt_close.config(relief=FLAT, bg='gray13', fg='white',
                             borderwidth=0, highlightthickness=0)

        self.lb_users = Listbox(frame)
        self.lb_users.grid(row=1, column=0, rowspan=3,  pady=5, padx=5,
                           sticky=S+N+E+W)
        self.lb_users.config(bg='gray18', borderwidth=1,
                             highlightbackground='gray15',
                             highlightthickness=1,
                             fg='white', relief='solid')

        self.txt_chat = scrolledtext.ScrolledText(frame)
        self.txt_chat.grid(row=1, column=1,  columnspan=3, rowspan=3, pady=5,
                           padx=5, sticky=E+W+S+N)
        self.txt_chat.config(bg='gray18',  borderwidth=0,
                             highlightbackground='gray15',
                             highlightthickness=1,
                             relief='solid', padx=10, pady=5,  font=('', 10))
        self.txt_chat.vbar.config(troughcolor='black', bg='gray18')
        self.txt_chat.tag_config('sender', background='gray30',
                                 foreground='brown1',
                                 justify=RIGHT, font=('Bold', 10))
        self.txt_chat.tag_config('username', background='gray30',
                                 foreground='olive drab',
                                 justify=LEFT, font=('Bold', 10))
        self.txt_chat.tag_config('timestamp', background='gray30',
                                 foreground='black',
                                 justify=RIGHT, font=('Bold', 8))
        self.txt_chat.tag_config('message', background='gray30',
                                 foreground='white',
                                 justify=RIGHT, font=('Bold', 10))
        self.txt_chat.tag_config('file', background='red4', foreground='white',
                                 justify=RIGHT, font=('Bold', 10))
        self.txt_chat.tag_config('newline', background='gray18',
                                 foreground='gray18',
                                 justify=RIGHT, font=('Bold', 4))
        self.txt_chat.config(state=DISABLED)

        self.txt_msg = Entry(frame)
        self.txt_msg.grid(row=4, column=1, rowspan=1,  columnspan=1,
                          sticky=E+W+S+N, padx=5, pady=2)
        self.txt_msg.config(bg='gray13', fg='white', borderwidth=0,
                            highlightthickness=0, insertbackground='white',
                            state=DISABLED)
        self.txt_msg.bind('<Key>', self.key_pressed)
        self.txt_msg.bind('<FocusIn>', self.enable_send)
        self.txt_msg.bind('<FocusOut>', self.disable_send)
        self.txt_msg.bind('<Return>', self.send_message)

        fr_buttons_send = Frame(frame, bg='black', borderwidth=1,
                                background='black', relief=FLAT)
        fr_buttons_send.grid(row=4, column=2, columnspan=2, padx=5, pady=1,
                             sticky=W+E)

        self.bt_send = Button(fr_buttons_send, text='Send', width=5,
                              command=self.send_message)
        self.bt_send.grid(row=0, column=0,   sticky=E + W, pady=0, padx=5)
        self.bt_send.config(relief=FLAT, bg='gray13', fg='white',
                            borderwidth=0, highlightthickness=0,
                            state=DISABLED)
        self.bt_file = Button(fr_buttons_send, text='File', width=5,
                              command=self.send_file)
        self.bt_file.grid(row=0, column=1,   sticky=E + W, pady=0, padx=0)
        self.bt_file.config(relief=FLAT, bg='gray13', fg='white',
                            borderwidth=0, highlightthickness=0,
                            state=DISABLED)

        master.protocol('WM_DELETE_WINDOW', self.close)
