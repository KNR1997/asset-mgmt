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
            columns=("Asset Tag", "Asset Name", "Serial", "Model", "Category", "Status"),
            show="headings"
        )

        self.tree.heading("Asset Tag", text="Asset_Tag")
        self.tree.heading("Asset Name", text="Asset_Name")
        self.tree.heading("Serial", text="Serial")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")

        # self.tree.column("Asset_Tag", width=50)

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
            cur.execute("""
                SELECT assets.tag, assets.name, assets.serialNumber, models.name, categories.name, assets.status 
                FROM assets
                LEFT JOIN models ON assets.model_id = models.id
                LEFT JOIN categories ON models.category_id = categories.id
                WHERE assets.name LIKE ?
            """, ('%' + keyword + '%',))
        else:
            cur.execute("""
                SELECT assets.tag, assets.name, assets.serialNumber, models.name, categories.name, assets.status 
                FROM assets
                LEFT JOIN models ON assets.model_id = models.id
                LEFT JOIN categories ON models.category_id = categories.id
            """)

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
        modal.geometry("350x400")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # ---------------- LOAD MODELS ---------------- #
        conn = sqlite3.connect("assets.db")
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM models")
        models = cur.fetchall()

        print('fetch models----------: ', models)

        conn.close()

        model_map = {c[1]: c[0] for c in models}

        status_map = {
            "Pending",
            "Ready to Deploy",
            "Archived",
            "Broken - Not Fixable",
            "Lost/Stolen",
            "Out for Diagnostics",
            "Out for Repair"
        }

        tk.Label(modal, text="Asset Name").pack(pady=5)
        name_entry = tk.Entry(modal)
        name_entry.pack()

        tk.Label(modal, text="Asset Tag").pack(pady=5)
        tag_entry = tk.Entry(modal)
        tag_entry.pack()

        tk.Label(modal, text="Serial").pack(pady=5)
        serial_entry = tk.Entry(modal)
        serial_entry.pack()

        tk.Label(modal, text="Model").pack()
        model_combo = ttk.Combobox(
            modal,
            values=list(model_map.keys()),
            state="readonly"
        )
        model_combo.pack()

        tk.Label(modal, text="Status").pack()
        status_combo = ttk.Combobox(
            modal,
            values=list(status_map),
            state="readonly"
        )
        status_combo.pack()

        tk.Label(modal, text="Description").pack(pady=5)
        desc_entry = tk.Entry(modal)
        desc_entry.pack()

        if asset:
            name_entry.insert(0, asset[1])

        def save():
            selected_model = model_combo.get()
            selected_status = status_combo.get()

            print('selected_model-----------: ', selected_model)
            print('selected_status-----------: ', selected_status)

            if not selected_model:
                messagebox.showwarning("Warning", "Select a model")
                return

            model_id = model_map[selected_model]

            print('model_id-----------: ', model_id)

            conn = sqlite3.connect("assets.db")
            cur = conn.cursor()

            if asset:
                cur.execute("UPDATE assets SET name=? WHERE id=?",
                            (name_entry.get(), asset[0]))
            else:
                cur.execute("""
                    INSERT INTO assets (name, serialNumber, tag, status, model_id, description) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    name_entry.get(),
                    serial_entry.get(),
                    tag_entry.get(),
                    selected_status,
                    model_id,
                    desc_entry.get(),
                ))

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
