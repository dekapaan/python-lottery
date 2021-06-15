from tkinter import *


class ClaimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Claim your prize")
        self.master.geometry("200x200")
        self.master.config(bg="#171717")


root = Tk()
ClaimGUI(root)
root.mainloop()