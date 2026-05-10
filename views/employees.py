import tkinter as tk
from tkinter import ttk, messagebox
from services import employee_service as employee_service
from models.employee import Employee
from typing import Optional


class EmployeesView:
    def __init__(self, parent):
        self.employees = []
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Employees",
                 font=("Arial", 16)).pack(pady=10)

        # Top section (buttons + search)
        top = tk.Frame(self.frame)
        top.pack(fill="x", padx=10)

        tk.Button(top, text="Add Employee Model", command=self.open_add_modal)\
            .pack(side="left", padx=5)

        tk.Button(top, text="Delete Selected", command=self.delete_model)\
            .pack(side="left", padx=5)

        # Search field (right aligned)
        tk.Label(top, text="Search:").pack(side="right", padx=5)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)

        search_entry = tk.Entry(top, textvariable=self.search_var)
        search_entry.pack(side="right", padx=5)

        # Table
        self.tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Name", "Department"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")

        self.tree.column("ID", width=50)

        self.tree.pack(fill="both", expand=True)

        # Double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)

        self.load_employees()

    # ---------------- LOAD ---------------- #

    def load_employees(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = employee_service.get_all(keyword)

        for model in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    model.id,
                    model.name,
                    model.department,
                )
            )

        self.employees = rows

    # ---------------- SEARCH ---------------- #

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_employees(keyword)

    # ---------------- ADD / EDIT ---------------- #

    def open_add_modal(self):
        self.open_form("Add Employee")

    def open_form(self, title, model: Optional[Employee] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x300")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # ---------------- FORM ---------------- #
        tk.Label(modal, text="Employee Name").pack()
        name_entry = tk.Entry(modal)
        name_entry.pack()

        tk.Label(modal, text="Department Name").pack()
        department_entry = tk.Entry(modal)
        department_entry.pack()

        # ---------------- PREFILL (EDIT) ---------------- #

        if model:
            name_entry.insert(0, model.name)
            department_entry.insert(0, model.department)

        # ---------------- SAVE ---------------- #

        def save():
            name = name_entry.get()
            department = department_entry.get()

            if model:
                employee_service.update(
                    employee_id=model.id,
                    name=name,
                    department=department,
                )
            else:
                employee_service.insert(
                    name=name,
                    department=department,
                )

            modal.destroy()
            self.load_employees()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        model = self.employees[selected_index]

        if values:
            self.open_form("Edit Employee", model)

    # ---------------- DELETE ---------------- #

    def delete_model(self):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            messagebox.showwarning("Warning", "Select a row")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this model?")
        if not confirm:
            return

        employee_service.delete(values[0])
        self.load_employees()
