import random
from tkinter import *
from tkinter import messagebox
import uuid


class PlayGUI:
    def __init__(self, master):
        # window set up
        self.results = []
        self.text = ""
        self.total_win = 0
        self.game_no = 0
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

        # if len(id,get()) !== 13

        self.btn_submit = Button(self.master, text="Submit", bg="#171717", fg="#FA003F", borderwidth="0",
                                 highlightbackground="#FA003F", activebackground="#FA003F", activeforeground="#171717",
                                 command=self.submit)
        self.btn_submit.place(x=215, y=280)
        self.win_nums = []
        for x in range(6):
            rand_num = random.randint(1, 49)
            while rand_num in self.win_nums:
                rand_num = random.randint(1, 49)
            self.win_nums.append(rand_num)
        print(self.win_nums)

    def submit(self):
        self.results.append([int(self.spin1.get()), int(self.spin2.get()), int(self.spin3.get()), int(self.spin4.get()),
                             int(self.spin5.get()), int(self.spin6.get())])
        print(self.results)
        x = messagebox.askyesno(message="Would you like to submit another ticket?")
        if x:
            self.reset()

        else:
            self.results_window()

    def reset(self):
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

    def play_again(self):
        self.reset()
        self.win_nums.clear()
        for x in range(6):
            rand_num = random.randint(1, 49)
            while rand_num in self.win_nums:
                rand_num = random.randint(1, 49)
            self.win_nums.append(rand_num)
        print(self.win_nums)

    def results_window(self):
        result = Toplevel()
        result.title("Results")
        result.geometry("400x500")
        result.config(bg="#171717")

        head_result = Label(result, text="Were you lucky?", font="Garuda 12 bold", bg="#171717", fg="#FA003F")
        head_result.place(x=140, y=10)
        frame = Frame(result, height=50)
        frame.place(x=30, y=50)
        text = Text(frame)
        text.config(height=20, width=40)
        self.print_result()
        text.insert(END, self.text)
        text.config(state='disabled')
        scroll = Scrollbar(frame)
        text.config(yscrollcommand=scroll.set)
        scroll.config(command=text.yview)
        scroll.pack(side=RIGHT, fill=Y)
        text.pack(fill=Y)

        btn_play_again = Button(result, text="Play Again", bg="#171717", fg="#FA003F", borderwidth="0",
                                highlightbackground="#FA003F", activebackground="#FA003F",
                                activeforeground="#171717", command=lambda: [self.results.clear(), self.play_again(),
                                                                             text.delete(0, 'end'), result.destroy()])
        btn_play_again.place(x=30, y=430)
        btn_claim = Button(result, text="Claim", bg="#171717", fg="#FA003F", borderwidth="0",
                           highlightbackground="#FA003F", activebackground="#FA003F",
                           activeforeground="#171717", command=lambda: [result.destroy(), self.claim()])
        btn_claim.place(x=140, y=430)
        btn_exit = Button(result, text="Exit", bg="#171717", fg="#FA003F", borderwidth="0",
                          highlightbackground="#FA003F", activebackground="#FA003F",
                          activeforeground="#171717", command=exit)
        btn_exit.place(x=320, y=430)

    def print_result(self):
        self.game_no += 1
        self.text += "Game {}\n".format(self.game_no)
        winnings = {0: 0, 1: 0, 2: 20, 3: 100.50, 4: 2384, 5: 8584, 6: 10000000}
        for x in range(len(self.results)):
            count = 0
            for y in range(6):
                if self.results[x][y] == self.win_nums[y]:
                    count += 1
            self.text += "Set {}\n" \
                         "Number of winning numbers: {}\n" \
                         "Winnings: R{}\n\n".format(x + 1, count, winnings[count])

    def claim(self):
        self.master.withdraw()
        import claim


play = Tk()
PlayGUI(play)
img = PhotoImage(file='images/klipartz2.png', master=play)
img = img.subsample(16)
lbl_image = Label(play, image=img, bg="#171717")
lbl_image.image = img
lbl_image.place(x=240, y=1)
play.mainloop()
