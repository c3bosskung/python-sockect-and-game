from tkinter import *
from tkinter import ttk, messagebox
import tkinter.scrolledtext as st
from tkinter import simpledialog
import random

# --------------------------------------
import socket
import threading
import sys

SERVERIP = 'localhost'  # your server ip addr
PORT = 7500
BUFSIZE = 4096

global client

def server_handler(client):
    while True:
        try:
            data = client.recv(BUFSIZE)  # data from server
        except:
            print('ERROR!')
            break

        if (not data) or (data.decode('utf-8') == 'q'):
            print('quit!')
            break

        allmsg.set(allmsg.get() + data.decode('utf-8') + '\n')
        #chatbox.delete(1.0, END)  # clear old msg
        chatbox.insert(INSERT, data.decode('utf-8'))  # insert new msg
        chatbox.yview(END)
        # print('user: ', data.decode('utf-8'))

    client.close()
    messagebox.showerror('Connection Failed', 'ตัดการเชื่อมต่อ')
# --------------------------------------

GUI = Tk()
GUI.geometry('500x700+550+50')
GUI.title('Chat')

FONT1 = ('Angsana New', 35)
FONT2 = ('Angsana New', 20)
#  ----------------ChatBox-------------------
F1 = Frame(GUI)
F1.place(x=8, y=5)

allmsg = StringVar()

chatbox = st.ScrolledText(F1, width=29, height=9, font=FONT1)
chatbox.pack(expand=True, fill='x')

#  --------------------Message---------------------
v_msg = StringVar()

F2 = Frame(GUI)
F2.place(x=10, y=600)

E1 = ttk.Entry(F2, textvariable=v_msg, font=FONT2, width=40)
E1.pack(ipady=20)

#  --------------------Button---------------------
def sendmessage(event=None):
    msg = v_msg.get()
    allmsg.set(allmsg.get() + msg + '\n---\n')
    client.sendall(msg.encode('utf-8'))
    chatbox.delete(1.0, END)  # clear old msg
    chatbox.insert(INSERT, allmsg.get())  # insert new msg
    chatbox.yview(END)
    v_msg.set('') #  clear msg
    E1.focus()

F3 = Frame(GUI)
F3.place(x=380, y=620)

B1 = ttk.Button(F3, text='Send', command=sendmessage)
B1.pack(ipadx=20, ipady=10)

E1.bind('<Return>', sendmessage)

username = StringVar()
getname = simpledialog.askstring('NAME', 'What your name?')

if getname == '':
    num = random.randint(10000, 99999)
    getname = str(num)

username.set(getname)
chatbox.insert(INSERT, 'Hello ' + getname)

# ------------------------------------------
global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    client.connect((SERVERIP, PORT))
    firsttext = 'NAME|' + username.get()
    client.send(firsttext.encode('utf-8'))
    task = threading.Thread(target=server_handler, args=(client,))
    task.start()
except:
    print('ERROR!')
    messagebox.showerror('Connection Failed', 'ไม่สามารถเชื่อมต่อกับ server ได้')
    sys.exit()

# -------------------------------------------

GUI.mainloop()