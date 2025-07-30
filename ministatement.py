# ministatement.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db import get_db_connection

class MiniStatementApp:
    def __init__(self, root, pinnumber):
        self.root = root
        self.root.title("Mini Statement")
        self.root.geometry("400x600")
        self.root.configure(bg="white")

        # Bank name label
        bank_label = tk.Label(root, text="Indian Bank", font=("Arial", 12), bg="white")
        bank_label.place(x=150, y=20)

        # Masked card number label
        self.card_label = tk.Label(root, text="", font=("Arial", 10), bg="white")
        self.card_label.place(x=20, y=80)

        # Transaction history
        self.statement_label = tk.Label(root, text="", font=("Courier", 9), bg="white", justify="left", anchor="nw")
        self.statement_label.place(x=20, y=140, width=360, height=300)

        # Balance
        self.balance_label = tk.Label(root, text="", font=("Arial", 10), bg="white")
        self.balance_label.place(x=20, y=460)

        # Exit Button
        exit_btn = tk.Button(root, text="Exit", command=self.exit)
        exit_btn.place(x=20, y=500, width=100, height=25)

        self.pinnumber = pinnumber
        self.load_data()

    def load_data(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get masked card number
            cursor.execute("SELECT accountType FROM login WHERE cardnumber = %s", (self.pinnumber,))
            result = cursor.fetchone()
            if result:
                acc = result[0]
                masked = acc[:4] + "XXXXXXXX" + acc[-4:]
                self.card_label.config(text=f"Card Number: {masked}")

            # Get transaction history and balance
            cursor.execute("SELECT date, type, amount FROM bank WHERE pin = %s", (self.pinnumber,))
            transactions = cursor.fetchall()

            statement_html = ""
            balance = 0
            for row in transactions:
                date, mode, amount = row
                statement_html += f"{date}   {mode:<10}   {amount}\n\n"
                if mode == "Deposit":
                    balance += int(amount)
                else:
                    balance -= int(amount)

            self.statement_label.config(text=statement_html)
            self.balance_label.config(text=f"Your total Balance is Rs {balance}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def exit(self):
        self.root.destroy()

def run_ministatement(pin):
    root = tk.Tk()
    app = MiniStatementApp(root, pin)
    root.mainloop()

# Run independently
if __name__ == "__main__":
    run_ministatement("1234")
