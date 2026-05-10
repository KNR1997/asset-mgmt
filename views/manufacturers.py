import tkinter as tk
from tkinter import ttk, messagebox
from services import manufacturer_service as service
from models.manufacturer import Manufacturer
from typing import Optional

class ManufacturersView:
    def __init__(self, parent):
        self.categories = []
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Categories",
                 font=("Arial", 16)).pack(pady=10)

        # Top section (buttons + search)
        top = tk.Frame(self.frame)
        top.pack(fill="x", padx=10)

        tk.Button(top, text="Add Manufacturer", command=self.open_add_modal)\
            .pack(side="left", padx=5)

        tk.Button(top, text="Delete Selected", command=self.delete_manufacturer)\
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
            columns=("ID", "Name", "URL", "Support URL"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Support URL", text="Support URL")

        self.tree.column("ID", width=50)

        self.tree.pack(fill="both", expand=True)

        # Double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)

        self.load_manufacturers()

    # ---------------- LOAD ---------------- #

    def load_manufacturers(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = service.get_all(keyword)

        for manufacturer in rows:
            self.tree.insert(
                "", 
                tk.END, 
                values=(
                    manufacturer.id,
                    manufacturer.name,
                    manufacturer.url,
                    manufacturer.supportURL,
                )
            )

        self.categories = rows

    # ---------------- SEARCH ---------------- #

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_manufacturers(keyword)

    # ---------------- ADD / EDIT ---------------- #

    def open_add_modal(self):
        self.open_form("Add Manufacturer")

    def open_form(self, title, manufacturer: Optional[Manufacturer] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x450")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        tk.Label(modal, text="Manufacturer Name").pack(pady=5)
        name_entry = tk.Entry(modal)
        name_entry.pack()

        tk.Label(modal, text="URL").pack(pady=5)
        url_entry = tk.Entry(modal)
        url_entry.pack()

        tk.Label(modal, text="Support URL").pack(pady=5)
        support_url_entry = tk.Entry(modal)
        support_url_entry.pack()

        tk.Label(modal, text="Warranty Lookup URL").pack(pady=5)
        warranty_lookup_url_entry = tk.Entry(modal)
        warranty_lookup_url_entry.pack()

        tk.Label(modal, text="Support Phone").pack(pady=5)
        support_phone_entry = tk.Entry(modal)
        support_phone_entry.pack()

        tk.Label(modal, text="Support Email").pack(pady=5)
        support_email_entry = tk.Entry(modal)
        support_email_entry.pack()

        tk.Label(modal, text="Notes").pack(pady=5)
        notes_entry = tk.Entry(modal)
        notes_entry.pack()

        if manufacturer:
            name_entry.insert(0, manufacturer.name)
            url_entry.insert(0, manufacturer.url)
            support_url_entry.insert(0, manufacturer.supportURL)

        def save():
            name = name_entry.get()
            url = url_entry.get()
            supportURL = support_url_entry.get()
            warrantyLookupUrl = warranty_lookup_url_entry.get()
            supportPhone = support_phone_entry.get()
            supportEmail = support_email_entry.get()
            notes = notes_entry.get()

            if not name:
                messagebox.showwarning("Warning", "Enter name")
                return

            if manufacturer:
                service.update(
                    manufacturer_id=manufacturer.id, 
                    name=name,
                    url=url,
                    supportURL=supportURL,
                    warrantyLookupUrl=warrantyLookupUrl,
                    supportPhone=supportPhone,
                    supportEmail=supportEmail,
                    notes=notes,
                )
            else:
                service.insert(
                    name=name,
                    url=url,
                    supportURL=supportURL,
                    warrantyLookupUrl=warrantyLookupUrl,
                    supportPhone=supportPhone,
                    supportEmail=supportEmail,
                    notes=notes,
                )

            modal.destroy()
            self.load_manufacturers()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        manufacturer = self.categories[selected_index]

        if values:
            self.open_form("Edit Manufacturer", manufacturer)

    # ---------------- DELETE ---------------- #

    def delete_manufacturer(self):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            messagebox.showwarning("Warning", "Select a row")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this manufacturer?")
        if not confirm:
            return

        service.delete(values[0])
        self.load_manufacturers()
