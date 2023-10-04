from tkinter import *
import time


class askWindow(Toplevel):
    def __init__(self, parent, text):

        Toplevel.__init__(self, parent)
        Label(self, text=text).grid(
            row=0, column=0, columnspan=2, padx=50, pady=10)

        b_yes = Button(self, text="Yes", command=self.yes, width=8)
        b_yes.grid(row=1, column=0, padx=10, pady=10)
        b_no = Button(self, text="No", command=self.no, width=8)
        b_no.grid(row=1, column=1, padx=10, pady=10)

        self.answer = None
        self.protocol("WM_DELETE_WINDOW", self.no)

    def yes(self):
        self.answer = "Yes"
        self.destroy()

    def no(self):
        self.answer = "No"
        self.destroy()

    def notAnswer(self):
        self.answer = "None"
        self.destroy()


def popup(root, title, message):
    w = 270
    h = 100

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    d = askWindow(root, message)
    d.title(title)

    d.geometry('%dx%d+%d+%d' % (w, h, x, y))

    root.after(10000, d.notAnswer)
    root.wait_window(d)
    return d.answer
