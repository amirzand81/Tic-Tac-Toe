import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import types
from askWindow import popup
import getpass
from notification import showNotif
import time
from gameBoard import GameBoard
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import socket
import threading
import time
from askWindow import popup
from notification import Notification
import sys

sockets = []
sockIndex = 0

server_addr = (sys.argv[1], 40123)

userName = getpass.getuser()
bgcolor = "#00a6ff"
notifes = []
sockets = []
sockIndex = 0
serverSocket = socket.socket()


def isServerEnable():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_addr)

    except OSError:
        messagebox.showerror("Error", "Server is not connected")
        exit(0)

    sock.close()


def send(message):

    sock.send(message.encode())

    if (message[0:3] == "off"):
        time.sleep(0.2)
        sock.close()
        return


def getRequestGame():

    global sockIndex

    message = sockets[sockIndex].recv(1024).decode()

    ans = popup(root, "Request Game",
                f"from \"{sockets[sockIndex].getpeername()}\"?")
    sockIndex += 1

    if ans == "No":
        sockets[sockIndex-1].send(b"reject")
        app.updateNotif(
            f'Request of "{message}" was rejected.')
        sockets[sockIndex-1].close()
        return

    if ans == "None":
        sockets[sockIndex-1].send(b"freeze")
        app.updateNotif(
            f'Request of "{message}" was not answered.')
        sockets[sockIndex-1].close()
        return

    sockets[sockIndex-1].send(b"accept")
    GameBoard(userName, sockets[sockIndex-1], root, "server")
    app.updateNotif(f'Request of "{message}" is accepted.')


def server():
    global sockIndex, sockets, serverSocket

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ip_address, port))
    serverSocket.listen(100)

    try:

        while True:
            sockets.append(serverSocket.accept()[0])
            app.updateNotif(
                f"get request from {sockets[sockIndex].getpeername()}")
            requestThread = threading.Thread(target=getRequestGame)
            requestThread.start()

    except OSError:
        exit(0)


def waitToAnswer(s):
    ans = s.recv(1024).decode()

    if ans == "reject":
        showNotif(root, "your request was rejected", "warn")
        app.updateNotif(f'your request rejected by {s.getpeername()}.')
        s.close()
        return

    if ans == "freeze":
        showNotif(root, f"{s.getpeername()} not responsed", "warn")
        app.updateNotif(f'{s.getpeername()} this player not responsed')
        s.close()
        return

    app.updateNotif(f'{s.getpeername()} accepts your invation')

    GameBoard(userName, s, root=root)


class App:
    def __init__(self, root):

        # set window title and size
        root.title(f"{userName} - {ip_address}")
        root.protocol("WM_DELETE_WINDOW", self.quitButtun_command)

        width = 431
        height = 375

        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()

        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg=bgcolor)
        self.requestButton = tk.Button(root)
        self.requestButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        self.requestButton["font"] = ft
        self.requestButton["fg"] = "#000000"
        self.requestButton["justify"] = "center"
        self.requestButton["text"] = "Request"
        self.requestButton.place(x=310, y=120, width=100, height=25)
        self.requestButton["command"] = self.requestButton_command
        self.requestButton["state"] = DISABLED
        self.requestButton.bind('<ButtonPress-1>', self.requestButton_command)

        frm1 = Frame(root)
        frm1.place(x=20, y=60, width=268, height=126)
        scrollbar = Scrollbar(frm1, orient=VERTICAL)
        self.onlineUsersBox = tk.Listbox(
            frm1, yscrollcommand=scrollbar.set, width=50)
        self.onlineUsersBox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.onlineUsersBox["font"] = ft
        self.onlineUsersBox["fg"] = "#333333"
        self.onlineUsersBox["justify"] = "center"
        self.previous_selected = None
        root.bind('<ButtonPress-1>', self.deselect_item)

        scrollbar.config(command=self.onlineUsersBox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.onlineUsersBox.pack(fill=BOTH, expand=YES)

        scanButton = tk.Button(root)
        scanButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        scanButton["font"] = ft
        scanButton["fg"] = "#000000"
        scanButton["justify"] = "center"
        scanButton["text"] = "Scan"
        scanButton.place(x=310, y=70, width=100, height=25)
        scanButton["command"] = self.scanButton_command

        onlineUsersLabel = tk.Label(root, text='Online Users')
        ft = tkFont.Font(family='Times', size=12)
        onlineUsersLabel["font"] = ft
        onlineUsersLabel["fg"] = "white"
        onlineUsersLabel["justify"] = "center"
        onlineUsersLabel.place(x=20, y=30, width=91, height=30)
        onlineUsersLabel.config(bg=bgcolor)

        self.waitLabel = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        self.waitLabel["font"] = ft
        self.waitLabel["fg"] = "red"
        self.waitLabel["justify"] = "center"
        self.waitLabel["text"] = "Please Wait ..."
        self.waitLabel.config(bg=bgcolor)

        frm = Frame(root)
        frm.place(x=20, y=220, width=390, height=95)
        scrollbar = Scrollbar(frm, orient=VERTICAL)
        self.notifBox = tk.Listbox(frm, yscrollcommand=scrollbar.set, width=50)
        self.notifBox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=11)
        self.notifBox["font"] = font = ft
        self.notifBox["fg"] = "#333333"
        self.notifBox["justify"] = "left"

        scrollbar.config(command=self.notifBox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.notifBox.pack(fill=BOTH, expand=YES)

        notifLabel = tk.Label(root)
        ft = tkFont.Font(family='Times', size=12)
        notifLabel["font"] = ft
        notifLabel["fg"] = "white"
        notifLabel["justify"] = "center"
        notifLabel["text"] = "Notifications"
        notifLabel.place(x=20, y=190, width=100, height=30)
        notifLabel.config(bg=bgcolor)

        quitButtun = tk.Button(root)
        quitButtun["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        quitButtun["font"] = ft
        quitButtun["fg"] = "#000000"
        quitButtun["justify"] = "center"
        quitButtun["text"] = "Quit"
        quitButtun.place(x=310, y=330, width=100, height=25)
        quitButtun["command"] = self.quitButtun_command

    def deselect_item(self, event):
        if self.onlineUsersBox.curselection() == self.previous_selected:
            self.onlineUsersBox.selection_clear(0, tk.END)

        if self.onlineUsersBox.curselection() == ():
            self.requestButton["state"] = DISABLED

        else:
            self.requestButton["state"] = NORMAL

        self.previous_selected = self.onlineUsersBox.curselection()
        self.notifBox.selection_clear(0, tk.END)

    def recive(self):
        try:
            recv_data = sock.recv(1024)

            if recv_data:
                recived_message = recv_data.decode("utf-8")

                if recived_message == "online":
                    showNotif(root, "There's no online player!", "info")
                    return

                onliens = recived_message[7:].split("+")

                for i in onliens:
                    app.updateOnlineUsers(i)

        except OSError:
            messagebox.showerror("Error", "server is not connected")
            exit(1)
            root.destroy()

    def scanButton_command(self):

        app.updateNotif(f"Scan online users")
        send(f"list {userName}")
        self.onlineUsersBox.delete(0, tk.END)
        self.recive()

    def updateOnlineUsers(self, onlineUser):
        self.onlineUsersBox.insert(END, onlineUser)

    def updateNotif(self, newMessage):

        t = time.strftime("%H:%M:%S", time.localtime())
        notifes.append(f" {t} - " + newMessage)

        i = len(notifes)

        self.notifBox.delete(0, tk.END)
        colorCount = 0

        while i < 5:
            self.notifBox.insert(END, "")
            i += 1

            self.notifBox.itemconfig(colorCount, bg='#bae7ff')
            colorCount += 1

        for i in notifes:
            self.notifBox.insert(END, i)

            if colorCount % 2:
                self.notifBox.itemconfig(colorCount, bg='#bae7ff')
                self.notifBox.itemconfig(colorCount, foreground='#030773')

            else:
                self.notifBox.itemconfig(colorCount, bg='#bae7ff')
                self.notifBox.itemconfig(colorCount, foreground="#030773")

            colorCount += 1

        self.notifBox.see(END)

    def requestButton_command(self, event):

        global sockIndex

        try:
            if (self.onlineUsersBox.curselection() == ()):
                return

            destIp = self.onlineUsersBox.get(
                list(self.onlineUsersBox.curselection())[0])

            app.updateNotif(f"Send request to {destIp}")
            destIp = eval(destIp.split(" - ")[-1])

            sockets.append(socket.socket())
            sockets[sockIndex].connect((destIp[0], int(destIp[1])+1))
            sockets[sockIndex].send(("start " + userName).encode())

            threading.Thread(target=waitToAnswer, args=(
                sockets[sockIndex],)).start()

            sockIndex += 1

        except OSError:
            showNotif(root, "Ofline user", "warn")
            self.scanButton_command()

    def quitButtun_command(self):
        global serverSocket

        send(f"off {userName}")
        serverSocket.close()
        root.destroy()


if __name__ == "__main__":

    isServerEnable()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    send("start " + userName)

    ip_address = sock.getsockname()[0]
    port = int(sock.getsockname()[1]) + 1

    serverThread = threading.Thread(target=server)
    serverThread.start()

    time.sleep(1)

    root = tk.Tk()
    app = App(root)

    app.updateNotif(f"Start connection\n")

    root.mainloop()
    sock.close()
