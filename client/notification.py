import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time
import threading


class Notification (tk.Frame):

    def __init__(self, master, width, height, bg, image, text, close_img, img_pad,
                 text_pad, font, y_pos):

        super().__init__(master, bg=bg, width=width, height=height)

        threading.Thread(target=self.checkTimeout).start()

        self.pack_propagate(0)
        self.y_pos = y_pos
        self.master = master
        self.width = width
        right_offset = 8
        self.cur_x = self.master.winfo_width()
        self.x = self.cur_x - (self.width + right_offset)
        img_label = tk.Label(self, image=image, bg=bg)
        img_label.image = image
        img_label.pack(side="left", padx=img_pad[0])
        message = tk.Label(self, text=text, font=font, bg=bg, fg="black")

        message.pack(side="left", padx=text_pad[0])
        close_btn = tk.Button(self, image=close_img, bg=bg, relief="flat",
                              command=self.hide_animation, cursor="hand2")
        close_btn.image = close_img
        close_btn.pack(side="right", padx=5)
        self.place(x=self.cur_x, y=y_pos)

    def show_animation(self):
        if self.cur_x > self.x:
            self.cur_x -= 1
            self.place(x=self.cur_x, y=self.y_pos)
            self.after(1, self.show_animation)

    def hide_animation(self):
        if self.cur_x < self.master.winfo_width():
            self.cur_x += 1
            self.place(x=self.cur_x, y=self.y_pos)
            self.after(1, self.hide_animation)

    def checkTimeout(self):

        try:
            time.sleep(4)
            self.destroy()

        except:
            pass


def showNotif(root, message, type):

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
        root, 350, 55, "white", im, message, cim, img_pad, text_pad, "cambria 11", 8)

    notification.show_animation()
