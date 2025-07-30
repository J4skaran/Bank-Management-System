from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import get_db_connection
import random

class SignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signup Form")
        self.root.geometry("600x700")
        self.root.configure(bg="white")

        Label(self.root, text="SIGNUP - Page 1", font=("Oswald", 24, "bold")).place(x=180, y=20)

        self.add_label_entry("Name:", "name_entry", 100)
        self.add_label_entry("Father's Name:", "father_entry", 140)

        Label(self.root, text="Date of Birth:", font=("Raleway", 12)).place(x=50, y=180)
        self.dob_entry = DateEntry(self.root, font=("Arial", 12), background='darkblue', foreground='white', borderwidth=2)
        self.dob_entry.place(x=220, y=180)

        Label(self.root, text="Gender:", font=("Raleway", 12)).place(x=50, y=220)
        self.gender_var = StringVar()
        gender_combo = ttk.Combobox(self.root, textvariable=self.gender_var, state="readonly", values=["Male", "Female", "Other"])
        gender_combo.place(x=220, y=220)
        gender_combo.current(0)

        self.add_label_entry("Email:", "email_entry", 260)

        Label(self.root, text="Marital Status:", font=("Raleway", 12)).place(x=50, y=300)
        self.marital_var = StringVar()
        marital_combo = ttk.Combobox(self.root, textvariable=self.marital_var, state="readonly", values=["Married", "Unmarried"])
        marital_combo.place(x=220, y=300)
        marital_combo.current(0)

        self.add_label_entry("Address:", "address_entry", 340)
        self.add_label_entry("City:", "city_entry", 380)
        self.add_label_entry("Pin Code:", "pin_entry", 420)

        Label(self.root, text="State:", font=("Raleway", 12)).place(x=50, y=460)
        self.state_var = StringVar()
        state_combo = ttk.Combobox(self.root, textvariable=self.state_var, state="readonly", values=[
            "Kashmir", "Delhi", "Punjab", "Maharashtra", "Karnataka", "Uttar Pradesh"
        ])
        state_combo.place(x=220, y=460)
        state_combo.current(0)

        Button(self.root, text="Next", command=self.submit, bg="black", fg="white", font=("Arial", 12)).place(x=240, y=520)

    def add_label_entry(self, label_text, tag, y):
        Label(self.root, text=label_text, font=("Raleway", 12)).place(x=50, y=y)
        entry = Entry(self.root, font=("Arial", 12))
        entry.place(x=220, y=y)
        setattr(self, tag, entry)

    def submit(self):
        name = self.name_entry.get()
        father = self.father_entry.get()
        dob = self.dob_entry.get_date()
        gender = self.gender_var.get()
        email = self.email_entry.get()
        marital_status = self.marital_var.get()
        address = self.address_entry.get()
        city = self.city_entry.get()
        pin = self.pin_entry.get()
        state = self.state_var.get()

        if not all([name, father, email, address, city, pin]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            formno = str(random.randint(1000, 9999))  # Generate random form number

            cursor.execute("""
                INSERT INTO signup (formno, name, father_name, dob, gender, email, marital_status, address, city, pin, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (formno, name, father, dob, gender, email, marital_status, address, city, pin, state))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Signup Step 1 Completed!")

            self.root.destroy()
            import signup2
            signup2.run_signup2(formno)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

def run_signup():
    root = Tk()
    app = SignupApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_signup()
