import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class AssetModelsView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Asset Models",
                 font=("Arial", 16)).pack(pady=10)

        # Top section (buttons + search)
        top = tk.Frame(self.frame)
        top.pack(fill="x", padx=10)

        tk.Button(top, text="Add Asset Model", command=self.open_add_modal)\
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
            columns=("ID", "Name", "Model No", "Category"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Model No", text="Model No")
        self.tree.heading("Category", text="Category")

        self.tree.column("ID", width=50)

        self.tree.pack(fill="both", expand=True)

        # Double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)

        self.load_asset_models()

    # ---------------- LOAD ---------------- #

    def load_asset_models(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        if keyword:
            cur.execute("""
                SELECT models.id, models.name, models.modelNumber, categories.name
                FROM models
                LEFT JOIN categories ON models.category_id = categories.id
                WHERE models.name LIKE ?
            """, ('%' + keyword + '%',))
        else:
            cur.execute("""
                SELECT models.id, models.name, models.modelNumber, categories.name
                FROM models
                LEFT JOIN categories ON models.category_id = categories.id
            """)

        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)

        conn.close()

    # ---------------- SEARCH ---------------- #

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_asset_models(keyword)

    # ---------------- ADD / EDIT ---------------- #

    def open_add_modal(self):
        self.open_form("Add Category")

    def open_form(self, title, asset=None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x300")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # ---------------- LOAD CATEGORIES ---------------- #
        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM categories")
        categories = cur.fetchall()

        conn.close()

        category_map = {c[1]: c[0] for c in categories}

        # ---------------- FORM ---------------- #

        tk.Label(modal, text="Model Name").pack()
        name_entry = tk.Entry(modal)
        name_entry.pack()

        tk.Label(modal, text="Model Number").pack()
        model_no_entry = tk.Entry(modal)
        model_no_entry.pack()

        tk.Label(modal, text="Description").pack()
        desc_entry = tk.Entry(modal)
        desc_entry.pack()

        tk.Label(modal, text="Category").pack()
        category_combo = ttk.Combobox(
            modal,
            values=list(category_map.keys()),
            state="readonly"
        )
        category_combo.pack()

        # ---------------- PREFILL (EDIT) ---------------- #

        if asset:
            name_entry.insert(0, asset[1])
            model_no_entry.insert(0, asset[2])

            # set category name
            category_combo.set(asset[3] if asset[3] else "")

        # ---------------- SAVE ---------------- #

        def save():
            selected_category = category_combo.get()

            if not selected_category:
                messagebox.showwarning("Warning", "Select a category")
                return

            category_id = category_map[selected_category]

            conn = sqlite3.connect("assets.db")
            cur = conn.cursor()

            if asset:
                cur.execute("""
                    UPDATE models 
                    SET name=?, modelNumber=?, description=?, category_id=? 
                    WHERE id=?
                """, (
                    name_entry.get(),
                    model_no_entry.get(),
                    desc_entry.get(),
                    category_id,
                    asset[0]
                ))
            else:
                cur.execute("""
                    INSERT INTO models (name, modelNumber, description, category_id)
                    VALUES (?, ?, ?, ?)
                """, (
                    name_entry.get(),
                    model_no_entry.get(),
                    desc_entry.get(),
                    category_id
                ))

            conn.commit()
            conn.close()

            modal.destroy()
            self.load_asset_models()

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

        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM models WHERE id=?", (values[0],))

        conn.commit()
        conn.close()

        self.load_asset_models()
