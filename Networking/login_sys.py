from tkinter import *
from tkinter import messagebox
import getpass
import os
import re
import smtplib, ssl
import datetime
import sys
import client_config
import mysql.connector as mysql
myConnection = mysql.connect( host='localhost', user='root', passwd='')
cursor = myConnection.cursor()
try:
    cursor.execute("CREATE DATABASE Chats")
except:
    pass
try:
    cursor.execute('use chats')
except:
    pass

try:
    cursor.execute("CREATE TABLE login_details (name VARCHAR(255), email VARCHAR(255), password varchar(255))")
    flag = True
except:
    pass

def login_system():

    win = Tk()
    win.configure(background='light blue')
    win.geometry("1500x1000")
    label = Label(win,text = "Login",bg = 'light green',fg = 'orange',font=("arial bold",50))
    u_email = Label(win,text = "Email-ID:")
    u_email.place(x=640,y=245)
    label.place(x=675,y=150)
    txt = Entry(win,width = 20)
    txt1 = Entry(win,width = 20)
    txt.place(x=700,y=245)
    txt1.place(x=700,y=275)
    password = Label(win,text = "password:")
    password.place(x=635,y=275)
    user_name = Label(win,text = 'username:')
    user_name.place(x = 632, y = 305)
    user_n_input = Entry(win, width = 20)
    user_n_input.place(x = 700, y = 305)


    def email_validation(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showinfo("Email error","Please enter correct email id!")
            return False
        else:
            return True
    def pass_validation(passw):
        if len(passw) < 6:
            messagebox.showinfo("Password error","Password should not be less than 6 characters!")
            return False
        else:
            return True
    def login():
        flag = 0
        e_v_res = email_validation(txt.get())
        p_res = pass_validation(txt1.get())
        username = user_n_input.get()
        if e_v_res and p_res == True:
            cursor.execute('select * from login_details')
            details = cursor.fetchall()
            for user_info in details:
                if user_info[0] == user_n_input and user_info[2] == text1.get():
                    flag += 1
                
            if flag >= 0:
                messagebox.showinfo("Sucssesful","Logged in succesfully")
                client_config.client(user_n_input.get())
            else:
                messagebox.showerror("Error","username or password does'nt match!")
            
    def create_new_account():
        def account_creation_check():
            def con_pass_check(n_pass,n_cpass):
                if n_pass != n_cpass:
                    messagebox.showinfo("Confirmation error","The passwords that you entered didn't matched!")
                    return False
                else:
                    return True
            
            def email_validation(email):
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    messagebox.showinfo("Email error","Please enter correct email id!")
                    return False
                else:
                    return True
            def pass_validation(passw):
                if len(passw) < 6:
                    messagebox.showinfo("Password error","Password should not be less than 6 characters!")
                    return False
                else:
                    return True
            e_v_res = email_validation(n_email1.get())
            p_res = pass_validation(n_pass1.get())
            pass_check = con_pass_check(n_pass1.get(),n_cpass1.get())
            if e_v_res and p_res and pass_check == True:
                return True
                    
                    
                    
            
            
        cna = Tk()
        cna.configure(background='light blue')
        cna.geometry("1500x1000")
        u_name = Label(cna,text = "user name:")
        u_name.place(x = 700,y = 100)
        u_name1 = Entry(cna,width = 20)
        u_name1.place(x = 770,y = 100)
        n_email = Label(cna,text = "Email:")
        n_email.place(x = 726,y=130)
        n_email1 = Entry(cna,width = 20)
        n_email1.place(x = 770,y = 130)
        n_pass = Label(cna,text = "password:")
        n_pass.place(x = 706,y = 160)
        n_pass1 = Entry(cna,width = 20)
        n_pass1.place(x = 770,y = 160)
        n_cpass = Label(cna,text = "confirm password:")
        n_cpass.place(x = 660,y = 190)
        n_cpass1 = Entry(cna,width = 20)
        n_cpass1.place(x = 770,y = 190) 
        def log_in():
            account_creation_check()
            cursor.execute(f"insert into login_details values('{u_name1.get()}','{n_email1.get()}','{n_cpass1.get()}')")
            cursor.execute('commit')
            messagebox.showinfo('info','account created!')
 

        sub1 = Button(cna,text = "Submit",command = log_in)
        sub1.place(x = 770,y = 220)
        cna.mainloop()
        
    def password_alternative():
        pa = Tk()
        pa.configure(background='light blue')
        pa.geometry("1500x1000")
        otp_notice = Label(pa,text = "You will recieve an email with an otp\nDo not share the otp with anyone\nThe otp will be availabel only for 3 minutes.")
        otp_notice.place(x = 650,y = 100)
        otp_email = Entry(pa,width = 20)
        otp_email.place(x = 725,y = 170)
        otp_email1 = Label(pa,text = "Enter email:")
        otp_email1.place(x = 650,y = 170)
        def otp(v_mail):
            global otp
            currentDT = datetime.datetime.now()
            otp = (str(currentDT)[-6:])
            return otp
        otp_code = otp(otp_email)
        def vms():
            
            def verification_mail_sending(otp1,v_email):
                port = 587  
                smtp_server = "smtp.gmail.com"
                sender_email = "emailtesting78459@gmail.com"  
                receiver_email = v_email 
                password = "emailtest123"
                message ="\
                Subject: Hi there\nLooks like you have forgotten your password.\nUse this"+otp+" otp to log in alternatively do not share this otp with anyone."

                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()  
                    server.starttls(context=context)
                    server.ehlo()  
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
            verification_mail_sending(otp1,otp_email.get())
        def otp_check():
            otp_c = Tk()
            currentDT = datetime.datetime.now()
            otp_c.geometry("1500x1000")
            l1 = Label(otp_c,text = "Enter below the 6 digit number that you recieved.")
            l1.place(x = 650,y = 100)
            l2 = Label(otp_c,text = "Enter number:")
            l2.place(x = 670,y = 150)
            ent1 = Entry(otp_c)
            ent1.place(x = 760,y = 150)
            def check():
                while True:
                    if ent1.get() == otp_check:
                        messagebox.showinfo(text = "OTP entered is correct.")
                        break
                    else:
                        messagebox.showerror(text = "OTP entered is wrong!")
                        break
            b1 = Button(otp_c,text = "submit",command = "check")
            b1.place(x = 760,y = 200)

            otp_c.mainloop()
        get_otp = Button(pa,text = "Get OTP",command =lambda otp_code : vms(otp_code))
        get_otp.place(x = 750, y = 200)
        ent_otp = Button(pa,text = "Enter otp",command =lambda otp_code : otp_check(otp_code))
        ent_otp.place(x = 748, y = 240)
        pa.mainloop()
        
    sub = Button(win,text = "Submit",activebackground = 'red',command = login)
    sub.place(x = 730,y=335)
    c_n_a = Button(win,text = "Create new account",activebackground = 'green',command = create_new_account)
    fg_pass = Button(win,text = "Forgot your password?",activebackground = 'yellow',command = password_alternative)
    c_n_a.place(x = 600,y = 400)
    fg_pass.place(x = 800,y = 400)
    win.mainloop()
login_system()
