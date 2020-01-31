import socket
import select
import errno
import sys
import threading
import datetime
from tkinter import *
#import login_sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
port = 1234
currentDT = datetime.datetime.now()

def client():
    my_username = 'user1'
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((IP,port))
    client_socket.setblocking(False)
    win = Tk()
    win.configure(background='light blue')
    message1 = 0
    frame1 = Frame(win)
    frame1.pack(side = RIGHT)
    frame2 = Frame(win)
    frame2.pack(side = LEFT)
    msg_inpt = Entry(win,width = 50)
    msg_inpt.pack(side = BOTTOM)
    win.geometry('500x400')



    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    while True:
        def msg_recv():
            threading.Timer(0.5, msg_recv).start()
            message = ""
            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
            try:
                while True:
                    # recieve stuff
                    username_header = client_socket.recv(HEADER_LENGTH)
                    if not len(username_header):
                        print("conection closed by the server")
                        
                    username_length = int(username_header.decode('utf-8').strip())
                    username = client_socket.recv(username_length).decode('utf-8')

                    message_header = client_socket.recv(HEADER_LENGTH)

                    message_length = int(message_header.decode('utf-8').strip())
                    message = client_socket.recv(message_length).decode('utf-8')
                    msg_disp = Label(frame2,bg = 'green',fg= 'red',text = message)
                    msg_disp.pack(side = TOP, fill = 'x')
                    empty_space1 = Label(frame2,bg = 'light blue',text = "")
                    empty_space1.pack(side = TOP, fill = 'x')
                    empty_space2 = Label(frame1,bg = 'light blue',text = "")
                    empty_space2.pack(side = TOP, fill = 'x')
                    print(f">{message}")
                
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error',str(e))
                    sys.exit()
                

            except Exception as e:
                print('General error',str(e))
                sys.exit()
        
        def message_send():

            message = msg_inpt.get()
            x_pos = message1
            msg_disp = Label(frame1,bg = 'red',fg = 'yellow',text = message)
            msg_disp.pack(side = TOP, fill = 'x')
            empty_space1 = Label(frame1,bg = 'light blue',text = "")
            empty_space1.pack(side = TOP, fill = 'x')
            empty_space2 = Label(frame2,bg = 'light blue',text = "")
            empty_space2.pack(side = TOP, fill = 'x')
            msg_inpt.delete(0, END)
            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
            
            
        send_btn = Button(win,text = "send",command = message_send)
        send_btn.place(x = 410,y = 377)
        msg_recv()
        win.mainloop()

