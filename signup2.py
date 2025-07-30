import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db_connection
# If you don't have get_db_connection() in db.py, use your own connection function.

def run_signup2(formno):
    root = tk.Tk()
    app = Signup2App(root, formno)
    root.mainloop()

class Signup2App:
    def __init__(self, root, formno):
        self.root = root
        self.root.title("New Account Application - Page 2")
        self.root.geometry("850x750")
        self.root.config(bg="white")
        self.formno = formno

        # --- Labels and ComboBoxes ---
        tk.Label(root, text="Page 2: Additional Details", font=("Raleway", 22, "bold"), bg="white").place(x=280, y=30)
        tk.Label(root, text="Form No:", font=("Raleway", 13), bg="white").place(x=700, y=10)
        tk.Label(root, text=formno, font=("Raleway", 13), bg="white").place(x=760, y=10)

        self.add_combo("Religion:", ["Hindu", "Muslim", "Sikh", "Christian", "Other"], 120, "religion")
        self.add_combo("Category:", ["General", "OBC", "SC", "ST", "Other"], 170, "category")
        self.add_combo("Income:", ["Null", "<1,50,000", "<2,50,000", "<5,00,000", "Upto 10,00,000", "Above 10,00,000"], 220, "income")
        self.add_combo("Educational Qualification:", ["Non-Graduate", "Graduate", "Post-Graduate", "Doctrate", "Others"], 270, "education")
        self.add_combo("Occupation:", ["Salaried", "Self-Employed", "Business", "Student", "Retired", "Others"], 340, "occupation")

        self.add_entry("PAN Number:", 390, "pan")
        self.add_entry("Aadhar Number:", 440, "aadhar")

        # Senior Citizen
        tk.Label(root, text="Senior Citizen:", font=("Raleway", 18, "bold"), bg="white").place(x=100, y=490)
        self.sr_var = tk.StringVar()
        tk.Radiobutton(root, text="Yes", variable=self.sr_var, value="Yes", bg="white", font=("Raleway", 14)).place(x=350, y=490)
        tk.Radiobutton(root, text="No", variable=self.sr_var, value="No", bg="white", font=("Raleway", 14)).place(x=460, y=490)

        # Existing Account
        tk.Label(root, text="Existing Account:", font=("Raleway", 18, "bold"), bg="white").place(x=100, y=540)
        self.exist_var = tk.StringVar()
        tk.Radiobutton(root, text="Yes", variable=self.exist_var, value="Yes", bg="white", font=("Raleway", 14)).place(x=350, y=540)
        tk.Radiobutton(root, text="No", variable=self.exist_var, value="No", bg="white", font=("Raleway", 14)).place(x=460, y=540)

        # Submit Button
        tk.Button(root, text="Next", command=self.submit, font=("Raleway", 14, "bold"), bg="black", fg="white").place(x=570, y=640, width=100, height=30)

    def add_combo(self, label, options, y, attr):
        tk.Label(self.root, text=label, font=("Raleway", 18, "bold"), bg="white").place(x=100, y=y)
        combo = ttk.Combobox(self.root, values=options, font=("Raleway", 14), state="readonly")
        combo.current(0)
        combo.place(x=350, y=y, width=320, height=30)
        setattr(self, attr, combo)

    def add_entry(self, label, y, attr):
        tk.Label(self.root, text=label, font=("Raleway", 18, "bold"), bg="white").place(x=100, y=y)
        entry = tk.Entry(self.root, font=("Raleway", 14))
        entry.place(x=350, y=y, width=320, height=30)
        setattr(self, attr, entry)

    def submit(self):
        data = {
            'formno': self.formno,
            'religion': self.religion.get(),
            'category': self.category.get(),
            'income': self.income.get(),
            'education': self.education.get(),
            'occupation': self.occupation.get(),
            'pan': self.pan.get(),
            'aadhar': self.aadhar.get(),
            'seniorcitizen': self.sr_var.get(),
            'existingaccount': self.exist_var.get()
        }

        if not data['aadhar'] or not data['pan']:
            messagebox.showerror("Error", "Please fill all required fields (Aadhar and PAN).")
            return

        try:
            con = get_db_connection()
            cur = con.cursor()
            query = """
                INSERT INTO signup2 
                (formno, religion, category, income, education, occupation, pan, aadhar, seniorcitizen, existingaccount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, tuple(data.values()))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Details Saved!")
            self.root.destroy()
            import signup3
            signup3.run_signup3(self.formno)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

if __name__ == "__main__":
    run_signup2("1234")  # For standalone testing
