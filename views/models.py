import tkinter as tk
from tkinter import ttk, messagebox
from services import model_service as model_service
from services import category_service as category_service
from models.model import Model
from typing import Optional

class AssetModelsView:
    def __init__(self, parent):
        self.models = []
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Asset Models",
                 font=("Arial", 16)).pack(pady=10)

        # Top section (buttons + search)
        top = tk.Frame(self.frame)
        top.pack(fill="x", padx=10)

        tk.Button(top, text="Add Asset Model", command=self.open_add_modal)\
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

        rows = model_service.get_all(keyword)

        for model in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    model.id,
                    model.name,
                    model.modelNumber,
                    model.category_name,
                )
            )

        self.models = rows

    # ---------------- SEARCH ---------------- #

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_asset_models(keyword)

    # ---------------- ADD / EDIT ---------------- #

    def open_add_modal(self):
        self.open_form("Add Category")

    def open_form(self, title, model: Optional[Model] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x300")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # ---------------- LOAD CATEGORIES ---------------- #
        categories =  category_service.get_all()
        category_map = {c.name: c.id for c in categories}

        # ---------------- FORM ---------------- #
        tk.Label(modal, text="Model Name").pack()
        name_entry = tk.Entry(modal)
        name_entry.pack()

        tk.Label(modal, text="Model Number").pack()
        model_number_entry = tk.Entry(modal)
        model_number_entry.pack()

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

        if model:
            name_entry.insert(0, model.name)
            model_number_entry.insert(0, model.modelNumber)

            # set category name
            category_combo.set(model.category_name if model.category_name else "")

        # ---------------- SAVE ---------------- #

        def save():
            selected_category = category_combo.get()

            if not selected_category:
                messagebox.showwarning("Warning", "Select a category")
                return

            category_id = category_map[selected_category]

            name = name_entry.get()
            model_number = model_number_entry.get()
            description = name_entry.get()

            if model:
                model_service.update(
                    model_id=model.id,
                    name=name,
                    modelNumber=model_number,
                    description=description,
                    category_id=category_id,
                )
            else:
                model_service.insert(
                    name=name,
                    modelNumber=model_number,
                    description=description,
                    category_id=category_id,
                )

            modal.destroy()
            self.load_asset_models()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        model = self.models[selected_index]

        if values:
            self.open_form("Edit Model", model)

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

        model_service.delete(values[0])
        self.load_asset_models()
