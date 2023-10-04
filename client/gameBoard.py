from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import socket
import threading
import time
from askWindow import popup
from notification import Notification
import tkinter as tk
from PIL import Image
from PIL import ImageTk

sockets = []
sockIndex = 0


class GameBoard(Toplevel):

    def __init__(self, username, sock, root=None, type=""):
        self.multiple = PhotoImage(file=('.\\client\\pictures\\multiple.png'))
        self.circle = PhotoImage(file=('.\\client\\pictures\\circle.png'))
        self.username = username
        self.squars = [""] * 9
        self.tern = "client"
        self.sock = sock
        self.image = PhotoImage()
        self.connectionStatus = True

        if type != "":
            self.type = "server"

        else:
            self.type = "client"

        super().__init__(master=root)
        self.protocol("WM_DELETE_WINDOW", self.quitButton_command)

        self.title("Morabaraba Game")
        width = 623
        height = 337
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.config(bg="#00a6ff")

        self.square1Button = Button(self)
        self.square1Button["bg"] = "#ffffff"
        self.square1Button["cursor"] = "arrow"
        ft = tkFont.Font(family='Times', size=58)
        self.square1Button["font"] = ft
        self.square1Button["fg"] = "#ff0f0f"
        self.square1Button["justify"] = "center"
        self.square1Button["text"] = ""
        self.square1Button.place(x=10, y=10, width=80, height=80)
        self.square1Button["command"] = self.square1Button_command

        self.square2Button = Button(self)
        self.square2Button["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.square2Button["font"] = ft
        self.square2Button["fg"] = "#ffffff"
        self.square2Button["justify"] = "center"
        self.square2Button["text"] = ""
        self.square2Button.place(x=100, y=10, width=80, height=80)
        self.square2Button["command"] = self.square2Button_command

        self.square4Button = Button(self)
        self.square4Button["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.square4Button["font"] = ft
        self.square4Button["fg"] = "#ffffff"
        self.square4Button["justify"] = "center"
        self.square4Button["text"] = ""
        self.square4Button.place(x=10, y=100, width=80, height=80)
        self.square4Button["command"] = self.square4Button_command

        self.square3Button = Button(self)
        self.square3Button["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.square3Button["font"] = ft
        self.square3Button["fg"] = "#ffffff"
        self.square3Button["justify"] = "center"
        self.square3Button["text"] = ""
        self.square3Button.place(x=190, y=10, width=80, height=80)
        self.square3Button["command"] = self.square3Button_command

        self.square5Button = Button(self)
        self.square5Button["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.square5Button["font"] = ft
        self.square5Button["fg"] = "#ffffff"
        self.square5Button["justify"] = "center"
        self.square5Button["text"] = ""
        self.square5Button.place(x=100, y=100, width=80, height=80)
        self.square5Button["command"] = self.square5Button_command

        self.square6Button = Button(self)
        self.square6Button["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.square6Button["font"] = ft
        self.square6Button["fg"] = "#ffffff"
        self.square6Button["justify"] = "center"
        self.square6Button["text"] = ""
        self.square6Button.place(x=190, y=100, width=80, height=80)
        self.square6Button["command"] = self.square6Button_command

        self.square8Button = Button(self)
        self.square8Button["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.square8Button["font"] = ft
        self.square8Button["fg"] = "#ffffff"
        self.square8Button["justify"] = "center"
        self.square8Button["text"] = ""
        self.square8Button.place(x=100, y=190, width=80, height=80)
        self.square8Button["command"] = self.square8Button_command

        self.square9Button = Button(self)
        self.square9Button["bg"] = "#fefefe"
        ft = tkFont.Font(family='Times', size=10)
        self.square9Button["font"] = ft
        self.square9Button["fg"] = "#ffffff"
        self.square9Button["justify"] = "center"
        self.square9Button["text"] = ""
        self.square9Button.place(x=190, y=190, width=80, height=80)
        self.square9Button["command"] = self.square9Button_command

        self.square7Button = Button(self)
        self.square7Button["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.square7Button["font"] = ft
        self.square7Button["fg"] = "#ffffff"
        self.square7Button["justify"] = "center"
        self.square7Button["text"] = ""
        self.square7Button.place(x=10, y=190, width=80, height=80)
        self.square7Button["command"] = self.square7Button_command

        frm1 = Frame(self)
        frm1.place(x=290, y=40, width=320, height=180)
        scrollbar = Scrollbar(frm1, orient=VERTICAL)
        self.chatBox = tk.Listbox(
            frm1, yscrollcommand=scrollbar.set, width=50)
        self.chatBox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=14)
        self.chatBox["font"] = ft
        self.chatBox["fg"] = "#333333"
        self.chatBox["justify"] = "center"
        scrollbar.config(command=self.chatBox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.chatBox.pack(fill=BOTH, expand=YES)

        for i in range(8):
            self.chatBox.insert(END, " ")

        GLabel_575 = Label(self, bg="#00a6ff")
        ft = tkFont.Font(family='Times', size=14)
        GLabel_575["font"] = ft
        GLabel_575["fg"] = "#ffffff"
        GLabel_575["justify"] = "center"
        GLabel_575["text"] = "Chat Box"
        GLabel_575.place(x=290, y=10, width=84, height=30)

        self.MessageLineEdit = Entry(self)
        self.MessageLineEdit["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.MessageLineEdit["font"] = ft
        self.MessageLineEdit["fg"] = "#333333"
        self.MessageLineEdit["justify"] = "center"
        self.MessageLineEdit.place(x=290, y=235, width=270, height=35)

        self.sendButton = Button(self)
        self.sendButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        self.sendButton["font"] = ft
        self.sendButton["fg"] = "#000000"
        self.sendButton["justify"] = "center"
        self.sendButton["text"] = "send"
        self.sendButton.place(x=572, y=235, width=40, height=35)
        self.sendButton["command"] = self.sendButton_commands

        quitButton = Button(self)
        quitButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        quitButton["font"] = ft
        quitButton["fg"] = "#000000"
        quitButton["justify"] = "center"
        quitButton["text"] = "Quit"
        quitButton.place(x=510, y=290, width=100, height=30)
        quitButton["command"] = self.quitButton_command

        self.againButton = Button(self)
        self.againButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        self.againButton["font"] = ft
        self.againButton["fg"] = "#000000"
        self.againButton["justify"] = "center"
        self.againButton["text"] = "Play again"
        self.againButton["command"] = self.againButton_command

        self.square1 = Label(self)
        self.square2 = Label(self)
        self.square3 = Label(self)
        self.square4 = Label(self)
        self.square5 = Label(self)
        self.square6 = Label(self)
        self.square7 = Label(self)
        self.square8 = Label(self)
        self.square9 = Label(self)

        self.bind('<Return>', self.sendButton_command)
        self.sock.send(b"init")
        threading.Thread(target=self.recive).start()

    def showNotif(self, message, type):

        if type == "suc":
            im = Image.open("./client/pictures/true.png")

        elif type == "warn":
            im = Image.open("./client/pictures/warning.png")

        elif type == "fail":
            im = Image.open("./client/pictures/false.png")

        else:
            im = Image.open("./client/pictures/info.png")

        im = im.resize((25, 25), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(im)

        cim = Image.open("./client/pictures/multiple.png")
        cim = cim.resize((10, 10), Image.ANTIALIAS)
        cim = ImageTk.PhotoImage(cim)

        img_pad = (5, 0)
        text_pad = (5, 0)

        notification = Notification(
            self, 230, 55, "white", im, message, cim, img_pad, text_pad, "cambria 11", 8)

        notification.show_animation()

    def addMessage(self, message, type):

        if self.chatBox.size() >= 8 and self.chatBox.get(0) == " ":
            self.chatBox.delete(0)

        self.chatBox.insert(END, message)

        if type == "r":
            self.chatBox.itemconfig(END, bg="#adfff0")

        else:
            self.chatBox.itemconfig(END, bg="#d9ffad")

        self.chatBox.see(END)

    def recive(self):
        try:
            while True:
                recv_data = self.sock.recv(1024)

                if recv_data is not None:
                    message = recv_data.decode("utf-8").split()

                    if len(message) == 0:
                        continue

                    if message[0] == "init":
                        self.showNotif("Game started", "suc")

                    elif message[0] == "chat":
                        messages = " ".join(message).split("chat ")

                        for m in messages:
                            if m != "":
                                self.addMessage(m, "r")

                    elif message[0] == "new":
                        self.againButton.place_forget()
                        self.newGame()
                        self.showNotif("New game started", "suc")
                        self.againButton["state"] = NORMAL

                    elif message[0] == "end":

                        self.disabling()
                        self.againButton["state"] = DISABLED
                        self.sendButton["state"] = DISABLED
                        self.MessageLineEdit["state"] = DISABLED
                        self.sock.close()
                        self.connectionStatus = False

                        messagebox.showwarning(
                            "Warning", "The opposite player is out of the game!", parent=self)

                    elif message[0] == "again":
                        ans = popup(self, "Play Again",
                                    "Are you want to play again?")

                        if ans == "None" or ans == "No":
                            self.sock.send(b"reject")

                        else:
                            self.sock.send(b"new")
                            self.newGame()
                            self.showNotif("New game started", "suc")
                            self.againButton.place_forget()

                    elif message[0] == "reject":
                        self.showNotif("Your request not accepted!", "info")
                        self.againButton["state"] = NORMAL

                    else:

                        index = int(message[1])-1
                        self.squars[index] = message[0]
                        self.chooseSquares(index, message[0])

        except OSError:
            return

    def disabling(self):

        self.square1Button["state"] = DISABLED
        self.square2Button["state"] = DISABLED
        self.square3Button["state"] = DISABLED
        self.square4Button["state"] = DISABLED
        self.square5Button["state"] = DISABLED
        self.square6Button["state"] = DISABLED
        self.square7Button["state"] = DISABLED
        self.square8Button["state"] = DISABLED
        self.square9Button["state"] = DISABLED

    def newGame(self):

        self.squars = [""] * 9

        self.square1.place_forget()
        self.square2.place_forget()
        self.square3.place_forget()
        self.square4.place_forget()
        self.square5.place_forget()
        self.square6.place_forget()
        self.square7.place_forget()
        self.square8.place_forget()
        self.square9.place_forget()

        self.square1Button["state"] = NORMAL
        self.square2Button["state"] = NORMAL
        self.square3Button["state"] = NORMAL
        self.square4Button["state"] = NORMAL
        self.square5Button["state"] = NORMAL
        self.square6Button["state"] = NORMAL
        self.square7Button["state"] = NORMAL
        self.square8Button["state"] = NORMAL
        self.square9Button["state"] = NORMAL

    def changeTern(self):
        if self.tern == "server":
            self.tern = "client"

        else:
            self.tern = "server"

    def chooseSquares(self, index, type=""):

        if type == "":
            type = self.type
            self.sock.send((f"{self.tern} {index+1}").encode())

        if type == "server":
            self.image = self.multiple

        else:
            self.image = self.circle

        self.squars[index] = self.tern

        if index == 0:
            self.square1Button["state"] = DISABLED
            self.square1.place(x=15, y=15, width=70, height=70)
            self.square1.config(image=self.image)

        elif index == 1:
            self.square2Button["state"] = DISABLED
            self.square2.place(x=104, y=15, width=70, height=70)
            self.square2.config(image=self.image)

        elif index == 2:
            self.square3Button["state"] = DISABLED
            self.square3.place(x=195, y=15, width=70, height=70)
            self.square3.config(image=self.image)

        elif index == 3:
            self.square4Button["state"] = DISABLED
            self.square4.place(x=15, y=104, width=70, height=70)
            self.square4.config(image=self.image)

        elif index == 4:
            self.square5Button["state"] = DISABLED
            self.square5.place(x=104, y=104, width=70, height=70)
            self.square5.config(image=self.image)

        elif index == 5:
            self.square6Button["state"] = DISABLED
            self.square6.place(x=195, y=104, width=70, height=70)
            self.square6.config(image=self.image)

        elif index == 6:
            self.square7Button["state"] = DISABLED
            self.square7.place(x=15, y=195, width=70, height=70)
            self.square7.config(image=self.image)

        elif index == 7:
            self.square8Button["state"] = DISABLED
            self.square8.place(x=104, y=195, width=70, height=70)
            self.square8.config(image=self.image)

        elif index == 8:
            self.square9Button["state"] = DISABLED
            self.square9.place(x=195, y=195, width=70, height=70)
            self.square9.config(image=self.image)

        self.changeTern()
        self.checkGameEnded()

    def checkGameEnded(self):
        winner = ""

        if (self.squars[0] == self.squars[1] == self.squars[2] != ""):
            winner = self.squars[0]

        elif (self.squars[3] == self.squars[4] == self.squars[5] != ""):
            winner = self.squars[3]

        elif (self.squars[6] == self.squars[7] == self.squars[8] != ""):
            winner = self.squars[6]

        elif (self.squars[0] == self.squars[3] == self.squars[6] != ""):
            winner = self.squars[0]

        elif (self.squars[1] == self.squars[4] == self.squars[7] != ""):
            winner = self.squars[1]

        elif (self.squars[2] == self.squars[5] == self.squars[8] != ""):
            winner = self.squars[2]

        elif (self.squars[0] == self.squars[4] == self.squars[8] != ""):
            winner = self.squars[0]

        elif (self.squars[2] == self.squars[4] == self.squars[6] != ""):
            winner = self.squars[4]

        for i in self.squars:
            if i == "":
                break

        else:
            self.showNotif("The game was tied", "info")
            self.againButton.place(x=390, y=290, width=100, height=30)
            self.disabling()

        if winner != "":

            if winner == self.type:
                message = "You win :)"
                type = "suc"

            else:
                message = "You lost :("
                type = "fail"

            self.showNotif(message, type)
            self.againButton.place(x=390, y=290, width=100, height=30)
            self.disabling()

    def square1Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(0)

    def square2Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(1)

    def square3Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(2)

    def square4Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(3)

    def square5Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(4)

    def square6Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(5)

    def square7Button_command(self):
        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(6)

    def square8Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(7)

    def square9Button_command(self):

        if self.tern != self.type:
            self.showNotif("Not your turn now", "warn")
            return

        self.chooseSquares(8)

    def sendButton_command(self, event):
        message = self.MessageLineEdit.get()

        if message != "":
            self.sock.send((f"chat {message}").encode())
            self.MessageLineEdit.delete(0, END)
            self.MessageLineEdit.insert(0, "")
            self.addMessage(message, "s")

    def sendButton_commands(self):
        message = self.MessageLineEdit.get()

        if message != "":
            self.sock.send((f"chat {message}").encode())
            self.MessageLineEdit.delete(0, END)
            self.MessageLineEdit.insert(0, "")
            self.addMessage(message, "s")

    def againButton_command(self):
        self.sock.send(b"again")
        self.againButton["state"] = DISABLED

    def quitButton_command(self):

        if self.connectionStatus:
            self.sock.send(b"end")

        self.sock.close()
        self.destroy()
