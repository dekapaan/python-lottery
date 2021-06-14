from tkinter import *
from tkinter import messagebox
import uuid


class PlayGUI:
    def __init__(self, master):
        # window set up
        self.master = master
        self.master.title("rt Play")
        self.master.geometry("500x350")
        self.master.config(bg="#171717")

        self.lbl_head = Label(self.master, text="Test\n your\n luck", width=10, font="monospace 12 bold", bg="#171717",
                              fg="#FA003F")
        self.lbl_head.place(x=150, y=10)

        # player ID
        self.player_id = uuid.uuid1()
        player_id_text = "Player ID: {}".format(self.player_id)
        self.lbl_player = Label(self.master, text=player_id_text, bg="#131313", fg="white", font="Garuda 12")
        self.lbl_player.place(x=60, y=100)

        # Number selection widgets
        self.lbl_select = Label(self.master, text="Select your numbers:", font="Garuda 12 bold", bg="#171717",
                                fg="#FA003F")
        self.lbl_select.place(x=175, y=180)

        self.spin1 = Spinbox(self.master, from_=1, to=49, width=5)
        self.spin2 = Spinbox(self.master, from_=1, to=49, width=5)
        self.spin3 = Spinbox(self.master, from_=1, to=49, width=5)
        self.spin4 = Spinbox(self.master, from_=1, to=49, width=5)
        self.spin5 = Spinbox(self.master, from_=1, to=49, width=5)
        self.spin6 = Spinbox(self.master, from_=1, to=49, width=5)
        self.spin1.place(x=45, y=235)
        self.spin2.place(x=115, y=235)
        self.spin3.place(x=185, y=235)
        self.spin4.place(x=255, y=235)
        self.spin5.place(x=325, y=235)
        self.spin6.place(x=405, y=235)

        self.btn_submit = Button(self.master, text="Submit", bg="#171717", fg="#FA003F", borderwidth="0",
                                 highlightbackground="#FA003F", activebackground="#FA003F", activeforeground="#171717",
                                 command=self.submit)
        self.btn_submit.place(x=215, y=280)

        self.results = []

    def submit(self):
        self.results.append([self.spin1.get(), self.spin2.get(), self.spin3.get(), self.spin4.get(), self.spin5.get(),
                            self.spin6.get()])
        print(self.results)
        x = messagebox.askyesno(message="Would you like to submit another ticket?")
        if x:
            self.spin1.delete(0, "end")
            self.spin2.delete(0, "end")
            self.spin3.delete(0, "end")
            self.spin4.delete(0, "end")
            self.spin5.delete(0, "end")
            self.spin6.delete(0, "end")

            self.spin1.insert(0, 1)
            self.spin2.insert(0, 1)
            self.spin3.insert(0, 1)
            self.spin4.insert(0, 1)
            self.spin5.insert(0, 1)
            self.spin6.insert(0, 1)


play = Tk()
PlayGUI(play)
img = PhotoImage(file='images/klipartz2.png', master=play)
img = img.subsample(16)
lbl_image = Label(play, image=img, bg="#171717")
lbl_image.image = img
lbl_image.place(x=240, y=1)
play.mainloop()
