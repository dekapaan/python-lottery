from tkinter import *


class LottoGUI:
    def __init__(self, master):
        # Window set up
        self.master = master
        self.master.title("Login")
        self.master.geometry("500x400")
        self.master.config(bg="#171717")

        # login frame
        self.frame = Frame(self.master, width=450, height=200, bg="#131313")
        self.frame.place(x=25, y=95)

        # login labels
        self.lbl_head = Label(self.master, text="Test\nyour\nluck", width=10, font="monospace 12 bold", bg="#171717", fg="#FA003F")
        self.lbl_head.place(x=150, y=10)
        self.lbl_subhead = Label(self.frame, text="Enter your details", font="Garuda 12 bold", bg="#131313",
                                 fg="#FA003F")
        self.lbl_subhead.place(x=150, y=12)
        self.lbl_name = Label(self.frame, text="Name", font="Garuda 12", bg="#131313", fg="white")
        self.lbl_email = Label(self.frame, text="Email", font="Garuda 12", bg="#131313", fg="white")
        self.lbl_id = Label(self.frame, text="South African ID", font="Garuda 12", bg="#131313", fg="white")
        self.lbl_name.place(x=40, y=60)
        self.lbl_email.place(x=40, y=100)
        self.lbl_id.place(x=40, y=140)

        # login entries
        self.entry_email = Entry(self.frame, borderwidth="0")
        self.entry_name = Entry(self.frame, borderwidth="0")
        self.entry_id = Entry(self.frame, borderwidth="0")
        self.entry_name.place(x=245, y=67)
        self.entry_email.place(x=245, y=107)
        self.entry_id.place(x=245, y=147)

        # validate button
        self.btn_validate = Button(self.master, text="Validate", bg="#171717", fg="#FA003F", borderwidth="0",
                                   highlightbackground="#FA003F", activebackground="#FA003F",
                                   activeforeground="#171717", command=self.validate)
        self.btn_validate.place(x=25, y=330)

        # clear button
        self.btn_clear = Button(self.master, text="Clear", bg="#171717", fg="#FA003F", borderwidth="0",
                                highlightbackground="#FA003F", activebackground="#FA003F", activeforeground="#171717",
                                command=self.clear)
        self.btn_clear.place(x=350, y=330)

        # exit button
        self.btn_exit = Button(self.master, text="Exit", bg="#171717", fg="#FA003F", borderwidth="0",
                               highlightbackground="#FA003F", activebackground="#FA003F",
                               activeforeground="#171717", command=exit)
        self.btn_exit.place(x=425, y=330)

    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_id.delete(0, 'end')

    def validate(self):
        self.master.destroy()


root = Tk()
LottoGUI(root)
root.mainloop()