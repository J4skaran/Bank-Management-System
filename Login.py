import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import get_db_connection  # Ensure this function connects to your MySQL db

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AUTOMATED TELLER MACHINE")
        self.root.geometry("800x480")
        self.root.configure(bg="white")

        # Load logo
        try:
            img = Image.open("C:/Users/91700/OneDrive/Documents/BANK PROJECT/icons/atm.jpg").resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(root, image=self.logo_img).place(x=70, y=10)
        except Exception as e:
            print(f"Image load error: {e}")

        # Labels and Entry Fields
        tk.Label(root, text="WELCOME TO ATM", font=("Osward", 38, "bold"), bg="white").place(x=200, y=40)
        tk.Label(root, text="Card No:", font=("Raleway", 28, "bold"), bg="white").place(x=125, y=150)
        self.card_entry = tk.Entry(root, font=("Arial", 14))
        self.card_entry.place(x=300, y=150, width=230, height=30)

        tk.Label(root, text="PIN:", font=("Raleway", 28, "bold"), bg="white").place(x=125, y=220)
        self.pin_entry = tk.Entry(root, font=("Arial", 14), show="*")
        self.pin_entry.place(x=300, y=220, width=230, height=30)

        # Buttons
        tk.Button(root, text="SIGN IN", font=("Arial", 14, "bold"), bg="black", fg="white",
                  command=self.sign_in).place(x=300, y=300, width=100, height=30)

        tk.Button(root, text="CLEAR", font=("Arial", 14, "bold"), bg="black", fg="white",
                  command=self.clear_fields).place(x=430, y=300, width=100, height=30)

        tk.Button(root, text="SIGN UP", font=("Arial", 14, "bold"), bg="black", fg="white",
                  command=self.sign_up).place(x=300, y=350, width=230, height=30)

    def sign_in(self):
        cardnumber = self.card_entry.get()
        pin = self.pin_entry.get()

        if not cardnumber or not pin:
            messagebox.showerror("Input Error", "Please enter both Card Number and PIN")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login WHERE cardnumber = %s AND pin = %s", (cardnumber, pin))
            result = cursor.fetchone()
            conn.close()

            if result:
                messagebox.showinfo("Login", "Login Successful ✅")
                self.root.destroy()

                # Call transactions or dashboard page
                import transactions
                transactions.run_transactions(pin)
            else:
                messagebox.showerror("Login Failed", "❌ Incorrect Card Number or PIN")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def clear_fields(self):
        self.card_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)

    def sign_up(self):
        self.root.destroy()
        import signup
        signup.run_signup()

def run_login():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_login()
