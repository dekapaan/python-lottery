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

        self.lbl_head = Label(self.master, text="Test\nyour\nluck", width=10, font="monospace 12 bold", bg="#171717",
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

        self.spin1 = Spinbox(self.master, from_=0, to=49, width=5)
        self.spin2 = Spinbox(self.master, from_=0, to=49, width=5)
        self.spin3 = Spinbox(self.master, from_=0, to=49, width=5)
        self.spin4 = Spinbox(self.master, from_=0, to=49, width=5)
        self.spin5 = Spinbox(self.master, from_=0, to=49, width=5)
        self.spin6 = Spinbox(self.master, from_=0, to=49, width=5)
        self.spin1.place(x=45, y=235)
        self.spin2.place(x=115, y=235)
        self.spin3.place(x=185, y=235)
        self.spin4.place(x=255, y=235)
        self.spin5.place(x=325, y=235)
        self.spin6.place(x=405, y=235)

        self.btn_submit = Button(self.master, text="Submit", bg="#171717", fg="#FA003F", borderwidth="0",
                                 highlightbackground="#FA003F", activebackground="#FA003F", activeforeground="#171717")
        self.btn_submit.place(x=215, y=280)

        self.results = []
        self.count = 0

    def submit(self):
        self.results[self.count] = [self.spin1, self.spin2, self.spin3, self.spin4, self.spin5, self.spin6]
        self.count += 1
        x = messagebox.askyesno(message="Would you like to submit another ticket?")
        if x:



root = Tk()
PlayGUI(root)
root.mainloop()