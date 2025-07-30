import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import get_db_connection  # Make sure this connects to your MySQL database

class BalanceEnquiryApp:
    def __init__(self, root, pin):
        self.root = root
        self.pin = pin
        self.root.title("Balance Enquiry")
        self.root.geometry("960x1080")
        self.root.configure(bg='black')
        self.root.overrideredirect(True)  # Removes title bar
        self.root.resizable(False, False)

        # Load background image
        try:
            atm_img = Image.open("C:/Users/91700/OneDrive/Documents/BANK PROJECT/icons/atm.jpg").resize((960, 1080))
            self.bg_img = ImageTk.PhotoImage(atm_img)
            bg_label = tk.Label(root, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Error loading background image:", e)

        # Balance label
        self.balance_label = tk.Label(root, text="", font=("System", 16, "bold"),
                                      bg="#000000", fg="white")
        self.balance_label.place(x=190, y=350)

        # Back button
        self.back_button = tk.Button(root, text="BACK", font=("System", 14),
                                     bg="white", fg="black", command=self.go_back)
        self.back_button.place(x=390, y=633, width=150, height=35)

        # Display balance
        self.display_balance()

    def display_balance(self):
        balance = 0
        try:
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("SELECT type, amount FROM bank WHERE pin = %s", (self.pin,))
            rows = cur.fetchall()
            for txn_type, amount in rows:
                if txn_type.lower() == "deposit":
                    balance += int(amount)
                elif txn_type.lower() == "withdraw":
                    balance -= int(amount)
            con.close()
            self.balance_label.config(text=f"Your Current Account Balance is Rs {balance}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching balance: {e}")

    def go_back(self):
        self.root.destroy()
        from transactions import run_transactions
        run_transactions(self.pin)

def run_balance_enquiry(pin):
    root = tk.Tk()
    app = BalanceEnquiryApp(root, pin)
    root.mainloop()

# For testing standalone
if __name__ == "__main__":
    run_balance_enquiry("1234")
