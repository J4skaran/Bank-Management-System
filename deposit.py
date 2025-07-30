import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime

from transactions import run_transactions  # Assumes you have transactions.py
from db import get_db_connection  # Your working DB connection function


class DepositApp:
    def __init__(self, root, pin):
        self.root = root
        self.pin = pin
        self.root.title("Deposit")

        try:
            img = Image.open("C:/Users/91700/OneDrive/Documents/BANK PROJECT/icons/atm.jpg").resize((1000, 1180))
            self.bg_img = ImageTk.PhotoImage(img)
            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0)
        except Exception as e:
            print("Image load error:", e)
            self.bg_label = tk.Label(self.root, bg="gray")
            self.bg_label.place(x=0, y=0, width=960, height=1080)

        self.label = tk.Label(self.bg_label, text="ENTER AMOUNT YOU WANT TO DEPOSIT", font=("System", 16), fg="white", bg="black")
        self.label.place(x=190, y=350)

        self.amount_entry = tk.Entry(self.bg_label, font=("Raleway", 22))
        self.amount_entry.place(x=190, y=420, width=320)

        self.deposit_btn = tk.Button(self.bg_label, text="DEPOSIT", command=self.deposit, width=15, height=1)
        self.deposit_btn.place(x=390, y=588)

        self.back_btn = tk.Button(self.bg_label, text="BACK", command=self.go_back, width=15, height=1)
        self.back_btn.place(x=390, y=633)

    def deposit(self):
        amount = self.amount_entry.get()
        if not amount:
            messagebox.showwarning("Warning", "Please enter the Amount you want to Deposit")
            return
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO bank (pin, date, type, amount) VALUES (%s, %s, %s, %s)"
            values = (self.pin, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Deposit", amount)
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Rs. {amount} Deposited Successfully")
            self.root.destroy()
            run_transactions(self.pin)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.root.destroy()
        run_transactions(self.pin)


def run_deposit(pin):
    root = tk.Tk()
    root.geometry("960x1080+500+0")
    root.resizable(False, False)
    app = DepositApp(root, pin)
    root.mainloop()
