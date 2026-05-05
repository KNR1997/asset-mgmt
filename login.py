import tkinter as tk
from tkinter import messagebox
import sqlite3

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x500")

        tk.Label(root, text="Username").pack()
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login", command=self.check_login).pack()

    def check_login(self):
        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM admin WHERE username=? AND password=?",
                    (self.username.get(), self.password.get()))

        messagebox.showinfo("Success", "Login successful")
        self.root.destroy()
        from dashboard import Dashboard
        root = tk.Tk()
        Dashboard(root)
        root.mainloop()

        # if cur.fetchone():
        #     messagebox.showinfo("Success", "Login successful")
        #     self.root.destroy()
        #     from dashboard import open_dashboard
        #     open_dashboard()
        # else:
        #     messagebox.showerror("Error", "Invalid credentials")