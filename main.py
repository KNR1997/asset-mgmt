import tkinter as tk
from views.login import Login
from db import setup

setup()

root = tk.Tk()
app = Login(root)
root.mainloop()
