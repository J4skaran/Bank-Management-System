import tkinter as tk
from tkinter import messagebox
import random
from db import get_db_connection

def run_signup3(formno):
    root = tk.Tk()
    app = Signup3App(root, formno)
    root.mainloop()

class Signup3App:
    def __init__(self, root, formno):
        self.root = root
        self.root.title("New Account Application - Page 3")
        self.root.geometry("850x850")
        self.root.config(bg="white")
        self.formno = formno

        tk.Label(root, text="Form No:", font=("Raleway", 14), bg="white").place(x=700, y=10)
        tk.Label(root, text=formno, font=("Raleway", 14), bg="white").place(x=770, y=10)

        tk.Label(root, text="Page 3: Account Details", font=("Raleway", 22, "bold"), bg="white").place(x=280, y=40)
        tk.Label(root, text="Account Type:", font=("Raleway", 18, "bold"), bg="white").place(x=100, y=140)

        self.account_var = tk.StringVar()
        acc_types = [
            ("Saving Account", 180),
            ("Fixed Deposit Account", 180),
            ("Current Account", 220),
            ("Recurring Deposit Account", 220)
        ]
        for text, y in acc_types:
            x = 100 if "Saving" in text or "Current" in text else 350
            tk.Radiobutton(root, text=text, variable=self.account_var, value=text, font=("Raleway", 16), bg="white").place(x=x, y=y)

        # Generate random 16-digit card number and 4-digit PIN
        self.cardnumber = str(random.randint(5040936000000000, 5040936999999999))
        self.pin = str(random.randint(1000, 9999))

        # Card info
        tk.Label(root, text="Card Number:", font=("Raleway", 18, "bold"), bg="white").place(x=100, y=300)
        tk.Label(root, text=self.cardnumber, font=("Raleway", 18), bg="white").place(x=330, y=300)
        tk.Label(root, text="(Your 16-digit Card number)", font=("Raleway", 12), bg="white").place(x=100, y=330)
        tk.Label(root, text="It would appear on ATM Card/Cheque Book and Statements", font=("Raleway", 12), bg="white").place(x=330, y=330)

        tk.Label(root, text="PIN:", font=("Raleway", 18, "bold"), bg="white").place(x=100, y=370)
        tk.Label(root, text=self.pin, font=("Raleway", 18), bg="white").place(x=330, y=370)
        tk.Label(root, text="(4-digit password)", font=("Raleway", 12), bg="white").place(x=100, y=400)

        # Services
        tk.Label(root, text="Services Required:", font=("Raleway", 18, "bold"), bg="white").place(x=100, y=450)
        self.services = {
            "ATM Card": tk.IntVar(),
            "Internet Banking": tk.IntVar(),
            "Mobile Banking": tk.IntVar(),
            "EMAIL Alerts": tk.IntVar(),
            "Cheque Book": tk.IntVar(),
            "E-Statement": tk.IntVar()
        }

        service_items = list(self.services.items())
        for i, (text, var) in enumerate(service_items):
            x = 100 if i % 2 == 0 else 350
            y = 500 + (i // 2) * 50
            tk.Checkbutton(root, text=text, variable=var, font=("Raleway", 16), bg="white").place(x=x, y=y)

        self.declare = tk.IntVar(value=1)
        tk.Checkbutton(root,
                       text="I hereby declare that the above entered details are correct to the best of my knowledge.",
                       variable=self.declare, font=("Raleway", 12), bg="white").place(x=100, y=680)

        tk.Button(root, text="Submit", command=self.submit, font=("Raleway", 14, "bold"),
                  bg="black", fg="white").place(x=250, y=720, width=100, height=30)
        tk.Button(root, text="Cancel", command=root.quit, font=("Raleway", 14, "bold"),
                  bg="black", fg="white").place(x=420, y=720, width=100, height=30)

    def submit(self):
        atype = self.account_var.get()
        facilities = [text for text, var in self.services.items() if var.get() == 1]
        facility = ', '.join(facilities)

        if not atype:
            messagebox.showerror("Error", "Please select an account type.")
            return

        try:
            con = get_db_connection()
            cur = con.cursor()

            # Insert into signup3 (note: use cardnumber not cardno)
            cur.execute("INSERT INTO signup3 (formno, atype, cardno, pin, facility) VALUES (%s, %s, %s, %s, %s)",
                        (self.formno, atype, self.cardnumber, self.pin, facility))

            # Insert into login (match column names exactly)
            cur.execute("INSERT INTO login (formno, accountType, cardnumber, pin) VALUES (%s, %s, %s, %s)",
                        (self.formno, atype, self.cardnumber, self.pin))

            con.commit()
            con.close()

            messagebox.showinfo("Success", f"Card No: {self.cardnumber}\nPIN: {self.pin}")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))


if __name__ == "__main__":
    run_signup3("1234")  # Example form number
