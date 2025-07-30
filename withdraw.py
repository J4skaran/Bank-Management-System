# withdraw.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from db import get_db_connection  # Ensure this exists and connects correctly
from transactions import run_transactions  # Make sure this module is present

class WithdrawApp:
    def __init__(self, root, pin):
        self.root = root
        self.pin = pin
        self.root.title("Withdraw")
        self.root.geometry("960x1080")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)

        # Background image
        try:
            img = Image.open("C:/Users/91700/OneDrive/Documents/BANK PROJECT/icons/atm.jpg").resize((1000, 1180))
            self.bg_img = ImageTk.PhotoImage(img)
            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0)
        except Exception as e:
            print("Image load error:", e)

        # Instructions
        self.label = tk.Label(self.bg_label, text="ENTER AMOUNT YOU WANT TO WITHDRAW",
                              font=("System", 16, "bold"), fg="white", bg="black")
        self.label.place(x=190, y=350)

        # Amount entry
        self.amount_entry = tk.Entry(self.bg_label, font=("Raleway", 22))
        self.amount_entry.place(x=190, y=420, width=320, height=30)

        # Buttons
        self.withdraw_btn = tk.Button(self.bg_label, text="WITHDRAW", command=self.withdraw_amount,
                                      font=("System", 14, "bold"))
        self.withdraw_btn.place(x=390, y=588, width=150, height=35)

        self.back_btn = tk.Button(self.bg_label, text="BACK", command=self.go_back,
                                  font=("System", 14, "bold"))
        self.back_btn.place(x=390, y=633, width=150, height=35)

    def withdraw_amount(self):
        amount = self.amount_entry.get()
        if not amount.strip().isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid numeric amount")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Corrected: `type` instead of `mode`
            query = "INSERT INTO bank (pin, date, type, amount) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (self.pin, date, 'Withdraw', amount))
            conn.commit()

            messagebox.showinfo("Success", f"Rs. {amount} Withdrawn Successfully")
            self.root.destroy()
            run_transactions(self.pin)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def go_back(self):
        self.root.destroy()
        run_transactions(self.pin)

def run_withdraw(pin):
    root = tk.Tk()
    app = WithdrawApp(root, pin)
    root.mainloop()

# Test independently
if __name__ == "__main__":
    run_withdraw("1234")
