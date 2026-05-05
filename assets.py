import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class AssetsView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Assets", font=("Arial", 16)).pack(pady=10)

        # Top section (buttons + search)
        top = tk.Frame(self.frame)
        top.pack(fill="x", padx=10)

        tk.Button(top, text="Add Asset", command=self.open_add_modal)\
            .pack(side="left", padx=5)

        tk.Button(top, text="Delete Selected", command=self.delete_asset)\
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
            columns=("ID", "Name", "Status"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50)

        self.tree.pack(fill="both", expand=True)

        # Double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)

        self.load_assets()

    # ---------------- LOAD ---------------- #

    def load_assets(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        if keyword:
            cur.execute("SELECT * FROM assets WHERE name LIKE ?", ('%' + keyword + '%',))
        else:
            cur.execute("SELECT * FROM assets")

        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

        conn.close()

    # ---------------- SEARCH ---------------- #

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_assets(keyword)

    # ---------------- ADD / EDIT ---------------- #

    def open_add_modal(self):
        self.open_form("Add Asset")

    def open_form(self, title, asset=None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("300x150")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        tk.Label(modal, text="Asset Name").pack(pady=5)
        name_entry = tk.Entry(modal)
        name_entry.pack()

        if asset:
            name_entry.insert(0, asset[1])

        def save():
            conn = sqlite3.connect("assets.db")
            cur = conn.cursor()

            if asset:
                cur.execute("UPDATE assets SET name=? WHERE id=?",
                            (name_entry.get(), asset[0]))
            else:
                cur.execute("INSERT INTO assets (name, status) VALUES (?, ?)",
                            (name_entry.get(), "available"))

            conn.commit()
            conn.close()

            modal.destroy()
            self.load_assets()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if values:
            self.open_form("Edit Asset", values)

    # ---------------- DELETE ---------------- #

    def delete_asset(self):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            messagebox.showwarning("Warning", "Select a row")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this asset?")
        if not confirm:
            return

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM assets WHERE id=?", (values[0],))

        conn.commit()
        conn.close()

        self.load_assets()