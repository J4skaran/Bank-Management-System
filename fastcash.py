import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from db import get_db_connection
from transactions import run_transactions

class FastCashApp:
    def __init__(self, root, pin):
        self.root = root
        self.pin = pin
        self.root.title("Fast Cash")
        self.root.geometry("960x1080")
        self.root.overrideredirect(True)

        # Background
        try:
            img = Image.open("C:/Users/91700/OneDrive/Documents/BANK PROJECT/icons/atm.jpg").resize((1000, 1180))
            self.bg_img = ImageTk.PhotoImage(img)
            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0)
        except Exception as e:
            print("⚠️ ATM background not found:", e)

        # Title
        title = tk.Label(self.bg_label, text="SELECT WITHDRAWAL AMOUNT", font=("System", 16, "bold"), fg="white", bg="black")
        title.place(x=235, y=400)

        # Amount buttons
        self.amounts = [100, 500, 1000, 2000, 5000, 10000]
        positions = [(170, 499), (390, 499), (170, 543), (390, 543), (170, 588), (390, 588)]

        for i, amt in enumerate(self.amounts):
            btn = tk.Button(self.bg_label, text=f"Rs {amt}", command=lambda a=amt: self.withdraw(a))
            btn.place(x=positions[i][0], y=positions[i][1], width=150, height=35)

        # BACK button
        back_btn = tk.Button(self.bg_label, text="BACK", command=self.go_back)
        back_btn.place(x=390, y=633, width=150, height=35)

    def withdraw(self, amount):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT type, amount FROM bank WHERE pin = %s", (self.pin,))
            records = cursor.fetchall()

            balance = 0
            for tx_type, amt in records:
                if tx_type == "Deposit":
                    balance += int(amt)
                else:
                    balance -= int(amt)

            if balance < amount:
                messagebox.showwarning("Insufficient Balance", f"❌ Not enough balance. Current: Rs {balance}")
                return

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO bank (pin, date, type, amount) VALUES (%s, %s, %s, %s)",
                           (self.pin, now, "Withdraw", str(amount)))
            conn.commit()

            messagebox.showinfo("Success", f"✅ Rs. {amount} withdrawn successfully.")
            self.root.destroy()
            run_transactions(self.pin)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def go_back(self):
        self.root.destroy()
        run_transactions(self.pin)

def run_fastcash(pin):
    root = tk.Tk()
    FastCashApp(root, pin)
    root.mainloop()

# For standalone test
if __name__ == "__main__":
    run_fastcash("1234")
