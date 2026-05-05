import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class EmployeesView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Employees", font=("Arial", 16)).pack(pady=10)

        # Form
        form = tk.Frame(self.frame)
        form.pack()

        tk.Label(form, text="Name").grid(row=0, column=0)
        self.name = tk.Entry(form)
        self.name.grid(row=0, column=1)

        # Buttons
        tk.Button(form, text="Add", command=self.add_employee).grid(row=0, column=2, padx=5)
        tk.Button(form, text="Update", command=self.update_employee).grid(row=0, column=3, padx=5)
        tk.Button(form, text="Delete", command=self.delete_employee).grid(row=0, column=4, padx=5)

        # Table
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Department"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")

        self.tree.pack(fill="both", expand=True, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.selected_id = None

        self.load_employees()

    def add_employee(self):
        if not self.name.get():
            messagebox.showwarning("Warning", "Enter name")
            return

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO employees (name, department) VALUES (?, ?)",
                    (self.name.get(), "IT"))

        conn.commit()
        conn.close()

        self.clear_form()
        self.load_employees()

    def on_select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if values:
            self.selected_id = values[0]
            self.name.delete(0, tk.END)
            self.name.insert(0, values[1])

    def update_employee(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a row first")
            return

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("UPDATE employees SET name=? WHERE id=?",
                    (self.name.get(), self.selected_id))

        conn.commit()
        conn.close()

        self.clear_form()
        self.load_employees()

    def delete_employee(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a row first")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this employee?")
        if not confirm:
            return

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM employees WHERE id=?", (self.selected_id,))

        conn.commit()
        conn.close()

        self.clear_form()
        self.load_employees()

    def load_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        for row in cur.execute("SELECT * FROM employees"):
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def clear_form(self):
        self.name.delete(0, tk.END)
        self.selected_id = None