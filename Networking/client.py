import socket
import select
import errno
import sys
import threading
#import mysql.connector
import datetime
from tkinter import *

HEADER_LENGTH = 10

IP = "127.0.0.1"
port = 1234
currentDT = datetime.datetime.now()
#mydb = mysql.connector.connect(host = "localhost",user = 'root',password = 'pritam.1234',database = 'mydatabase')
#my_cursor = mydb.cursor()

my_username = input("username: ")
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,port))
client_socket.setblocking(False)
win = Tk()
message1 = 0
#scroll_send = Scrollbar(win)
#scroll_send.pack(side = RIGHT , fill = 'y')
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
                msg_disp = Label(frame2,text = message)
                msg_disp.pack(side = BOTTOM, fill = 'x')
                print(f">{message}")
            
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error',str(e))
                sys.exit()
            

        except Exception as e:
            print('General error',str(e))
            sys.exit()
    
    def message_send():

        #threading.Timer(0.5,message_send,[message1]).start()
        #message = input(f"> ")
        message = msg_inpt.get()
        x_pos = message1
        msg_disp = Label(frame1,text = message)
        #msg_disp.place(x = x_pos,y = (len(message)-400))
        msg_disp.pack(side = BOTTOM, fill = 'x')
        msg_inpt.delete(0, END)
        #msg_inpt.insert(0, "")
        #scroll_send.config( command = msg_disp.yview )
        #msg_disp.grid(row = message1, column = 3)
        #message = ""
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
        
        
    send_btn = Button(win,text = "send",command = message_send)
    send_btn.place(x = 410,y = 377)
    msg_recv()
    #message_send()
    win.mainloop()

    #if not rec_msg:
        #msql = f"INSERT INTO chatdatabase value('{username.decode('utf-8')}','no message','{send_msg}')"
        #my_cursor.execute(msql)
        #mydb.commit()
    #else:
        #msql = f"INSERT INTO chatdatabase value('{username.decode('utf-8')}','{rec_msg}','{send_msg}')"
        #my_cursor.execute(msql)
        #mydb.commit()

    




    
