# transactions.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class TransactionsApp:
    def __init__(self, root, pin):
        self.root = root
        self.pin = pin
        self.root.title("Transaction Menu")
        self.root.geometry("900x900")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)  # remove window bar

        # Background image
        try:
            atm_img = Image.open("C:/Users/91700/OneDrive/Documents/BANK PROJECT/icons/atm.jpg").resize((900, 900))
            self.bg_img = ImageTk.PhotoImage(atm_img)
            self.bg_label = tk.Label(root, image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("ATM image missing or invalid path:", e)

        # Title Text
        self.text_label = tk.Label(root, text="Please select your Transactions",
                                   font=("System", 16, "bold"), bg="black", fg="white")
        self.text_label.place(x=210, y=300)

        # Buttons
        self.create_button("Deposit", self.open_deposit, 170, 415)
        self.create_button("Cash Withdraw", self.open_withdraw, 355, 415)
        self.create_button("Fast Cash", self.open_fastcash, 170, 450)
        self.create_button("Mini Statement", self.open_ministatement, 355, 450)
        self.create_button("Pin Change", self.open_pinchange, 170, 485)
        self.create_button("Balance Enquiry", self.open_balanceenquiry, 355, 485)
        self.create_button("Exit", self.exit_app, 355, 520)

    def create_button(self, text, command, x, y):
        btn = tk.Button(self.root, text=text, font=("System", 12), width=20,
                        command=command)
        btn.place(x=x, y=y, width=150, height=30)

    # Navigation stubs (implement these screens separately)
    def open_deposit(self):
        self.root.destroy()
        from deposit import run_deposit
        run_deposit(self.pin)

    def open_withdraw(self):
        self.root.destroy()
        from withdraw import run_withdraw
        run_withdraw(self.pin)

    def open_fastcash(self):
        self.root.destroy()
        from fastcash import run_fastcash
        run_fastcash(self.pin)

    def open_ministatement(self):
        from ministatement import run_ministatement
        run_ministatement(self.pin)

    def open_pinchange(self):
        self.root.destroy()
        from pinchange import run_pinchange
        run_pinchange(self.pin)

    def open_balanceenquiry(self):
        self.root.destroy()
        from balance_enquiry import run_balance_enquiry
        run_balance_enquiry(self.pin)

    def exit_app(self):
        self.root.destroy()

def run_transactions(pin):
    root = tk.Tk()
    app = TransactionsApp(root, pin)
    root.mainloop()

# For testing
if __name__ == "__main__":
    run_transactions("1234")
