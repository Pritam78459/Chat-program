import socket
import select
import errno
import sys
import threading
import mysql.connector
import datetime

HEADER_LENGTH = 10

IP = "127.0.0.1"
port = 1234
currentDT = datetime.datetime.now()
mydb = mysql.connector.connect(host = "localhost",user = 'root',password = 'pritam.1234',database = 'mydatabase')
my_cursor = mydb.cursor()

my_username = input("username: ")
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,port))
client_socket.setblocking(False)

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


                print(f">{message}")
                return message
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error',str(e))
                sys.exit()
            

        except Exception as e:
            print('General error',str(e))
            sys.exit()
    
    def message_send():
        threading.Timer(0.5,message_send).start()
        message = input(f"> ")
        #message = ""
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
            return message.decode('utf-8')
    rec_msg = msg_recv()
    send_msg = message_send()

    if not rec_msg:
        msql = f"INSERT INTO chatdatabase value('{username.decode('utf-8')}','no message','{send_msg}')"
        my_cursor.execute(msql)
        mydb.commit()
    else:
        msql = f"INSERT INTO chatdatabase value('{username.decode('utf-8')}','{rec_msg}','{send_msg}')"
        my_cursor.execute(msql)
        mydb.commit()

    
