import datetime
import socket
from tkinter import *
from tkinter import messagebox
from validate_email import validate_email
import rsaidnumber
from dateutil import relativedelta
import random
import uuid
import requests
import tkinter.ttk as ttk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import DNS
from playsound import playsound

class LottoFunction:
    def __init__(self):
        self.counter = 0

    def compare(self, list1, list2):
        try:
            self.counter = 0
            if len(list1) != len(list2):
                raise IndexError
            else:
                for i in range(len(list1)):
                    if list1[i] == list2[i]:
                        self.counter += 1

            return self.counter

        except IndexError:
            print("Lists must be of same length")


class EmailError(Exception):
    pass


class IdLengthError(Exception):
    pass


class FirstNameError(Exception):
    pass


class EmptyError(Exception):
    pass


class LottoGUI(LottoFunction):
    def __init__(self, master):
        # Window set up
        super().__init__()
        self.master = master
        self.master.title("Login")
        self.master.geometry("500x400")
        self.master.config(bg="#171717")

        # variables needed multiple places in class
        self.name = ""
        self.email = ""
        self.set_count = 0
        self.play_win = None
        self.claim_win = None
        self.total_win = 0
        self.win_nums = []
        self.game_no = 0
        self.results = []
        self.img2 = PhotoImage(file='images/klipartz2.png')  # lotto ball image
        self.img2 = self.img2.subsample(16)

        # login frame
        self.frame = Frame(self.master, width=450, height=200, bg="#131313")
        self.frame.place(x=25, y=95)

        # login labels
        self.lbl_subhead = Label(self.frame, text="Enter your details", font="Garuda 12 bold", bg="#131313",
                                 fg="#f9d914")
        self.lbl_subhead.place(x=150, y=12)
        img = PhotoImage(file='images/lotto.png')  # lotto ball image
        img = img.subsample(16)
        lbl_image = Label(self.master, image=img, bg="#171717")
        lbl_image.place(x=240, y=1)

        # name, email and id labels
        self.lbl_name = Label(self.frame, text="Name", font="Garuda 12", bg="#131313", fg="white")
        self.lbl_email = Label(self.frame, text="Email", font="Garuda 12", bg="#131313", fg="white")
        self.lbl_id = Label(self.frame, text="South African ID", font="Garuda 12", bg="#131313", fg="white")
        self.lbl_name.place(x=40, y=60)
        self.lbl_email.place(x=40, y=100)
        self.lbl_id.place(x=40, y=140)

        # login entry widgets
        self.entry_email = Entry(self.frame, borderwidth="0")
        self.entry_name = Entry(self.frame, borderwidth="0")
        self.entry_id = Entry(self.frame, borderwidth="0")
        self.entry_name.place(x=245, y=67)
        self.entry_email.place(x=245, y=107)
        self.entry_id.place(x=245, y=147)

        # validate button
        self.btn_validate = Button(self.master, text="Validate", bg="#171717", fg="#f9d914", borderwidth="0",
                                   highlightbackground="#f9d914", activebackground="#f9d914",
                                   activeforeground="#171717", command=self.validate)
        self.btn_validate.place(x=25, y=330)

        # clear button
        self.btn_clear = Button(self.master, text="Clear", bg="#171717", fg="#f9d914", borderwidth="0",
                                highlightbackground="#f9d914", activebackground="#f9d914", activeforeground="#171717",
                                command=self.clear)
        self.btn_clear.place(x=350, y=330)

        # exit button
        self.btn_exit = Button(self.master, text="Exit", bg="#171717", fg="#f9d914", borderwidth="0",
                               highlightbackground="#f9d914", activebackground="#f9d914",
                               activeforeground="#171717", command=exit)
        self.btn_exit.place(x=425, y=330)

        self.master.mainloop()

    # function to clear log entry fields
    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_id.delete(0, 'end')

    # validates details and traps incorrect data
    def validate(self):
        try:
            # Makes sure fields aren't empty
            if self.entry_email.get() == "" or self.entry_id == "" or self.entry_name == "":
                raise EmptyError

            # Ensures email exists
            if not validate_email(self.entry_email.get(), verify=True):
                raise EmailError

            int(self.entry_id.get())  # makes sure ID is only integers. If not, raises value error
            _id = (self.entry_id.get())
            date_of_birth = rsaidnumber.parse(_id).date_of_birth
            if len(_id) < 13 or len(_id) > 13:  # ID entry only allows 13 digit entry
                raise IdLengthError

            # If age < 18, error message
            elif relativedelta.relativedelta(datetime.datetime.today(), date_of_birth).years < 18:
                playsound("sounds/denied.wav")
                messagebox.showerror("Error", "You are underage and unable to participate")

            else:  # If validation process successful, move on to next screen and entries saved to variables
                self.name = self.entry_name.get()
                self.email = self.entry_email.get()
                messagebox.showinfo("Welcome", "Let's play!")
                root.withdraw()
                self.play_window(self.play_win)
                playsound("sounds/granted.wav")

        except EmptyError:
            messagebox.showerror(message="Make sure all entry fields are filled")

        except EmailError:
            messagebox.showerror("Error", "Invalid email")

        except DNS.Base.TimeoutError:
            messagebox.showerror("Timeout", "Check your internet connection")

        except ValueError:
            messagebox.showerror("Error", "Invalid ID number")

        except IdLengthError:
            messagebox.showerror("Error", "ID number must have 13 digits only")

    def play_window(self, window):
        # window set up
        self.master.withdraw()
        window = Toplevel()
        result_text = ""
        window.title("rt Play")
        window.geometry("900x350")
        window.config(bg="#171717")

        def submit():
            # saves lotto numbers in list
            try:
                results = [int(spin1.get()), int(spin2.get()), int(spin3.get()), int(spin4.get()),
                           int(spin5.get()), int(spin6.get())]
                for num in results:
                    if num > 49 or num <= 0:  # raise ValueError if number entry < 0 or > 49
                        raise ValueError

                self.results.append(results)  # append lotto numbers to list
                m = messagebox.askyesno(message="Would you like to submit another ticket?")
                if m:  # if yes, another ticket can be submitted
                    reset()

                else:
                    print_result(result_text)  # if no, move on to obtaining results
                    btn_submit.config(state='disabled')
                    btn_play_again.config(state='normal')
                    btn_claim.config(state='normal')

            except ValueError:
                messagebox.showerror(message="Number choices should be positive integers from 1 to 49")

        def reset():  # resets lotto number spin boxes
            spin1.delete(0, "end")
            spin2.delete(0, "end")
            spin3.delete(0, "end")
            spin4.delete(0, "end")
            spin5.delete(0, "end")
            spin6.delete(0, "end")

            spin1.insert(0, 1)
            spin2.insert(0, 1)
            spin3.insert(0, 1)
            spin4.insert(0, 1)
            spin5.insert(0, 1)
            spin6.insert(0, 1)

        def play_again():  # function to play another game
            # gets new winning numbers
            reset()
            self.win_nums.clear()
            for i in range(6):
                rand_num = random.randint(1, 49)
                while rand_num in self.win_nums:
                    rand_num = random.randint(1, 49)
                self.win_nums.append(rand_num)
            print(self.win_nums)
            btn_submit.config(state="normal")
            btn_play_again.config(state='disabled')
            btn_claim.config(state='disabled')

        def print_result(result_txt_var):  # Compares sets to winning numbers and prints results
            self.game_no += 1
            result_txt_var += "Game {}\n".format(self.game_no)  # Game number
            # winnings corresponding to matching numbers (keys) and values in rand
            winnings = {0: 0, 1: 0, 2: 20, 3: 100.50, 4: 2384, 5: 8584, 6: 10000000}
            self.set_count += len(self.results)  # count number of sets for that game
            for i in range(len(self.results)):
                # for each set per game, count matching numbers by calling compare function
                print(self.results)
                print(self.win_nums)
                count = self.compare(self.results[i], self.win_nums)
                result_txt_var += "Set {}\n" \
                                  "Number of winning numbers: {}\n" \
                                  "Winnings: R{}\n\n".format(i + 1, count, winnings[count])  # save results in text form
                self.total_win = self.total_win + winnings[count]

                # sounds for winning and losing
                if winnings[count] == 0:
                    playsound("sounds/lose.wav")
                else:
                    playsound("sounds/win.wav")

            # send results text to text widget to be seen by player
            text.config(state='normal')
            text.insert(END, result_txt_var)
            text.config(state='disabled')

        def claim():  # saves player details and results in text file
            if len(self.results) == 0:
                pass
            else:
                day = datetime.datetime.today().day
                month = datetime.datetime.today().month
                year = datetime.datetime.today().year
                with open('track.txt', 'a') as f:
                    f.write('Date: {}/{}/{}\n'.format(day, month, year))
                    f.write("Name: {}\n".format(self.name))
                    f.write("   PlayerID: {}\n".format(player_id))
                    f.write("   Email: {}\n".format(self.email))
                    f.write("   Winning combination: {}\n".format(self.win_nums))
                    f.write("   Total sets played for all games: {}\n".format(self.set_count))
                    f.write("   Total winnings due: R{}\n\n".format(self.total_win))

        lbl_head = Label(window, text="Test\n your\n luck", width=10, font="monospace 12 bold", bg="#171717",
                         fg="#f9d914")
        lbl_head.place(x=150, y=10)

        lbl_image2 = Label(window, image=self.img2, bg="#171717")
        lbl_image2.place(x=240, y=1)

        # player ID
        player_id = uuid.uuid1()
        player_id_text = "Player ID: {}".format(player_id)
        lbl_player = Label(window, text=player_id_text, bg="#131313", fg="white", font="Garuda 12")
        lbl_player.place(x=60, y=100)

        # Number selection widgets
        lbl_select = Label(window, text="Select your numbers:", font="Garuda 12 bold", bg="#171717",
                           fg="#f9d914")
        lbl_select.place(x=175, y=180)

        # spin boxes for set entry
        spin1 = Spinbox(window, from_=1, to=49, width=5)
        spin2 = Spinbox(window, from_=1, to=49, width=5)
        spin3 = Spinbox(window, from_=1, to=49, width=5)
        spin4 = Spinbox(window, from_=1, to=49, width=5)
        spin5 = Spinbox(window, from_=1, to=49, width=5)
        spin6 = Spinbox(window, from_=1, to=49, width=5)
        spin1.place(x=45, y=235)
        spin2.place(x=115, y=235)
        spin3.place(x=185, y=235)
        spin4.place(x=255, y=235)
        spin5.place(x=325, y=235)
        spin6.place(x=405, y=235)

        # submit button
        btn_submit = Button(window, text="Submit", bg="#171717", fg="#f9d914", borderwidth="0",
                            highlightbackground="#f9d914", activebackground="#f9d914", activeforeground="#171717",
                            command=submit)
        btn_submit.place(x=215, y=280)

        # gets first set of winning numbers
        for x in range(6):
            rand_num = random.randint(1, 49)
            while rand_num in self.win_nums:
                rand_num = random.randint(1, 49)
            self.win_nums.append(rand_num)
        print(self.win_nums)

        # result widgets
        head_result = Label(window, text="Were you lucky?", font="Garuda 12 bold", bg="#171717", fg="#f9d914")
        head_result.place(x=620, y=10)
        frame = Frame(window, height=50)  # frame for text widget and scrollbar
        frame.place(x=510, y=50)
        text = Text(frame)
        text.config(height=12.4, width=40)
        text.config(state='disabled')
        scroll = Scrollbar(frame)
        text.config(yscrollcommand=scroll.set)
        scroll.config(command=text.yview)
        scroll.pack(side=RIGHT, fill=Y)
        text.pack(fill=Y)

        # play again button
        btn_play_again = Button(window, text="Play Again", bg="#171717", fg="#f9d914", borderwidth="0",
                                highlightbackground="#f9d914", activebackground="#f9d914",
                                activeforeground="#171717", state='disabled', command=lambda: [self.results.clear(),
                                                                                               play_again()])
        btn_play_again.place(x=510, y=280)

        # claim button - destroys play window, `
        btn_claim = Button(window, text="Claim", bg="#171717", fg="#f9d914", borderwidth="0",
                           highlightbackground="#f9d914", activebackground="#f9d914",
                           activeforeground="#171717", state='disabled', command=lambda: [claim(), self.claim_window(self.claim_win),
                                                                        window.destroy()])
        btn_claim.place(x=620, y=280)
        btn_exit = Button(window, text="Exit", bg="#171717", fg="#f9d914", borderwidth="0",
                          highlightbackground="#f9d914", activebackground="#f9d914",
                          activeforeground="#171717", command=exit)
        btn_exit.place(x=800, y=280)

    @staticmethod
    def claim_window(window):  # claim window initialisation function
        window = Toplevel()
        window.title("Claim your prize")
        window.geometry("485x350")
        window.config(bg="#171717")

        def convert_currency():
            try:
                # to prevent empty strings being parsed through currency converter
                if entry_currency.get() == "":
                    raise EmptyError

                cur_api = requests.get("https://v6.exchangerate-api.com/v6/b8b53279722ad58c70d2a2de/latest/ZAR")
                cur_data = cur_api.json()

                # get converted amount from zar to currency chosen
                amount = prize * cur_data["conversion_rates"][entry_currency.get().upper()]

                # create converted amount string and send it to entry widget
                amount_text = '{} ({})'.format(round(amount, 2), entry_currency.get().upper())
                entry_winning_amount.config(state='normal')
                entry_winning_amount.delete("1.0", "end")
                entry_winning_amount.insert(END, amount_text)
                entry_winning_amount.tag_configure('center', justify=RIGHT)
                entry_winning_amount.tag_add('center', 1.0, 'end')
                entry_winning_amount.config(state='disabled')

            except EmptyError:
                messagebox.showerror(message="Currency field is empty")

            except KeyError:
                messagebox.showerror("Error", "Currency does not exist")

            except requests.exceptions.ConnectionError:
                messagebox.showerror(message="Check internet connection")

        def email():
            try:
                # fetch data needed by email, ie name email and player id
                with open('track.txt', 'r') as file:
                    for _line in file:
                        if "Name" in _line:
                            name = _line[6:-1]
                        if "Email" in _line:
                            email_id = _line[10:-1]
                        if "ID" in _line:
                            player_id = _line[14:-1]

                # Following is to make sure account holder name entered is alphabetic
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
                for num in numbers:
                    if str(num) in entry_account_holder_name.get():
                        raise NameError

                # make sure converted number is an integer. Only number string can be converted to integer
                int(entry_account_num.get())

                if entry_account_holder_name.get() == "":
                    raise EmptyError

                if entry_account_num.get() == "":
                    raise EmptyError

                if selection_bank.get() == "select an option":
                    raise EmptyError

                # Send results and and details to player
                sender_email_id = 'rtplaylotto@gmail.com'
                receiver_email_id = email_id
                password = "SFUqK9E3mvkcrR7"
                subject = "Congratulations"
                msg = MIMEMultipart()
                msg['From'] = sender_email_id
                msg['To'] = ", ".join(receiver_email_id)
                msg['Subject'] = subject
                body = "Congratulations {} on winning {}\n" \
                       "Please find details below\n\n" \
                       "Bank: {}\n" \
                       "Account holder: {}\n" \
                       "Account number: {}\n" \
                       "Player ID: {}\n\n" \
                       "Winnings, if any, should reflect in your account in 3-5 business days\n\n" \
                       "Best regards\n" \
                       "rtplay Team".format(name, entry_winning_amount.get(1.0, END), selection_bank.get(),
                                            entry_account_holder_name.get(), entry_account_num.get(), player_id)
                msg.attach(MIMEText(body, 'plain'))
                text = msg.as_string()
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(sender_email_id, password)
                s.sendmail(sender_email_id, receiver_email_id, text)
                s.quit()

                # messagebox prompting player to check email then close program
                messagebox.showinfo("Goodbye", "Check your email for further details. Application will now close")
                window.destroy()
                root.destroy()

            except NameError:
                messagebox.showerror(message="Account holder name must be alphabetic")

            except EmptyError:
                messagebox.showerror(message="Make sure to fill in all bank details")

            except ValueError:
                messagebox.showerror(message="Account number must be an integer")

            except socket.gaierror:
                messagebox.showerror(message="Failed to send email. Check internet connection")

        # subheading label
        lbl_head = Label(window, text="Enter your bank details", font="Garuda 12 bold", bg="#171717", fg="#f9d914")
        lbl_head.place(x=150, y=10)

        # Account holder name label and entry widgets
        lbl_account_holder = Label(window, text="Account holder name", font="Garuda 12", bg="#171717", fg="#fff")
        entry_account_holder_name = Entry(window)
        lbl_account_holder.place(x=20, y=80)
        entry_account_holder_name.place(x=300, y=85)

        # Bank account number label and entry widgets
        lbl_account_num = Label(window, text="Bank account number", font="Garuda 12", bg="#171717", fg="#fff")
        entry_account_num = Entry(window)
        lbl_account_num.place(x=20, y=110)
        entry_account_num.place(x=300, y=115)

        # currency code label and entry widgets
        lbl_currency = Label(window, text="Currency code(if not ZAR)", font="Garuda 12", bg="#171717", fg="#fff")
        entry_currency = Entry(window)
        btn_currency = Button(window, text="change currency", font="Garuda 11", pady=0, padx=13, width=52, bg="#171717",
                              fg="#f9d914", borderwidth="0", highlightbackground="#f9d914", activebackground="#f9d914",
                              activeforeground="#171717", command=convert_currency)
        btn_currency.place(x=20, y=190)
        lbl_currency.place(x=20, y=160)
        entry_currency.place(x=300, y=163)

        # Fetches winnings from text file
        with open("track.txt", "r") as f:
            for line in f:
                if "winnings" in line:
                    prize = round(float(line[24:-1]), 2)

        # Winning amount label and entry( contains winnings in zar then in chosen currency code) widgets
        lbl_winning_amount_head = Label(window, text="Total winnings", font="Garuda 12", bg="#171717", fg="#f9d914")
        entry_winning_amount = Text(window, borderwidth="0", bg="#fff", height=1, width=20)
        entry_winning_amount.insert(END, "{} (ZAR)".format(prize))
        entry_winning_amount.tag_configure('center', justify=RIGHT)
        entry_winning_amount.tag_add('center', 1.0, 'end')
        lbl_winning_amount_head.place(x=20, y=240)
        entry_winning_amount.place(x=300, y=247)

        # Bank selection label and option menu widgets
        lbl_bank = Label(window, text="Select bank", font="Garuda 12", bg="#171717", fg="#fff")
        selection_bank = StringVar()
        options_banks = ['ABSA', 'Nedbank', 'FNB', 'Standard Bank']
        option_menu_banks = ttk.OptionMenu(window, selection_bank, "select an option", *options_banks)
        lbl_bank.place(x=20, y=50)
        option_menu_banks.place(x=300, y=50)

        # confirm button widget to validate details, send email and close program
        btn_confirm = Button(window, text='Confirm', font="Garuda 11", pady=0, padx=12, width=52, bg="#171717", fg="#f9d914",
                             borderwidth="0", highlightbackground="#f9d914", activebackground="#f9d914",
                             activeforeground="#171717", command=email)
        btn_confirm.place(x=20, y=280)


# Tk initialises and gui loaded only if run from this file. Used in order to fetch class of function for unit testing
if __name__ == '__main__':
    root = Tk()
    LottoGUI(root)
