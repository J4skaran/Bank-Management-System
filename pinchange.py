import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import get_db_connection
from transactions import run_transactions  # Use run_transactions() instead of class directly

class PinChangeApp:
    def __init__(self, root, pinnumber):
        self.root = root
        self.root.title("Change PIN")
        self.root.geometry("960x1080")
        self.root.configure(bg="black")
        self.root.resizable(False, False)
        self.pinnumber = pinnumber

        # ✅ FIX: Use PIL to load JPG
        try:
            img = Image.open("C:/Users/91700/OneDrive/Documents/BANK PROJECT/icons/atm.jpg").resize((960, 1080))
            self.bg_img = ImageTk.PhotoImage(img)
            self.bg_label = tk.Label(root, image=self.bg_img)
            self.bg_label.place(x=0, y=0, width=960, height=1080)
        except Exception as e:
            print("Background image error:", e)
            self.bg_label = tk.Label(root, bg="black")
            self.bg_label.place(x=0, y=0, width=960, height=1080)

        # Labels
        tk.Label(self.bg_label, text="CHANGE YOUR PIN", font=("System", 16), fg="white", bg="black").place(x=280, y=330)
        tk.Label(self.bg_label, text="New PIN:", font=("System", 16), fg="white", bg="black").place(x=180, y=390)
        tk.Label(self.bg_label, text="Re-Enter New PIN:", font=("System", 16), fg="white", bg="black").place(x=180, y=440)

        # PIN Entry fields
        self.pin_entry = tk.Entry(self.bg_label, show='*', font=("Raleway", 14), width=15)
        self.pin_entry.place(x=350, y=390)

        self.repin_entry = tk.Entry(self.bg_label, show='*', font=("Raleway", 14), width=15)
        self.repin_entry.place(x=350, y=440)

        # Buttons
        tk.Button(self.bg_label, text="CHANGE", command=self.change_pin).place(x=390, y=588, width=150, height=35)
        tk.Button(self.bg_label, text="BACK", command=self.go_back).place(x=390, y=633, width=150, height=35)

    def change_pin(self):
        new_pin = self.pin_entry.get()
        re_entered_pin = self.repin_entry.get()

        if not new_pin or not re_entered_pin:
            messagebox.showwarning("Warning", "Please fill both fields")
            return
        if new_pin != re_entered_pin:
            messagebox.showerror("Error", "Entered PIN does not match")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Update PIN in all necessary tables
            cursor.execute("UPDATE bank SET pin = %s WHERE pin = %s", (new_pin, self.pinnumber))
            cursor.execute("UPDATE login SET pin = %s WHERE pin = %s", (new_pin, self.pinnumber))
            cursor.execute("UPDATE signup3 SET pin = %s WHERE pin = %s", (new_pin, self.pinnumber))
            conn.commit()

            messagebox.showinfo("Success", "PIN changed successfully")
            self.root.destroy()
            run_transactions(new_pin)

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def go_back(self):
        self.root.destroy()
        run_transactions(self.pinnumber)

def run_pinchange(pin):
    root = tk.Tk()
    PinChangeApp(root, pin)
    root.mainloop()

if __name__ == "__main__":
    run_pinchange("1234")
