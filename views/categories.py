import tkinter as tk
from tkinter import ttk, messagebox
from services import category_service as service


class CategoriesView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Categories",
                 font=("Arial", 16)).pack(pady=10)

        # Top section (buttons + search)
        top = tk.Frame(self.frame)
        top.pack(fill="x", padx=10)

        tk.Button(top, text="Add Category", command=self.open_add_modal)\
            .pack(side="left", padx=5)

        tk.Button(top, text="Delete Selected", command=self.delete_category)\
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
            columns=("ID", "Name"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        # self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50)

        self.tree.pack(fill="both", expand=True)

        # Double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)

        self.load_categories()

    # ---------------- LOAD ---------------- #

    def load_categories(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = service.get_all(keyword)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    # ---------------- SEARCH ---------------- #

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_categories(keyword)

    # ---------------- ADD / EDIT ---------------- #

    def open_add_modal(self):
        self.open_form("Add Category")

    def open_form(self, title, asset=None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("300x150")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        tk.Label(modal, text="Category Name").pack(pady=5)
        name_entry = tk.Entry(modal)
        name_entry.pack()

        if asset:
            name_entry.insert(0, asset[1])

        def save():
            name = name_entry.get()

            if not name:
                messagebox.showwarning("Warning", "Enter name")
                return

            if asset:
                service.update(asset[0], name)
            else:
                service.insert(name)

            modal.destroy()
            self.load_categories()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if values:
            self.open_form("Edit Category", values)

    # ---------------- DELETE ---------------- #

    def delete_category(self):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            messagebox.showwarning("Warning", "Select a row")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this category?")
        if not confirm:
            return

        service.delete(values[0])
        self.load_categories()
