import tkinter as tk
from tkinter import ttk, messagebox
from services import asset_service as asset_service
from services import model_service as model_service
from services import employee_service as employee_service
from services import checkout_service as checkout_service
from models.asset import Asset
from typing import Optional
from enums.asset_status import AssetStatus


class AssetsView:
    def __init__(self, parent):
        self.assets = []
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="📊 Assets",
            font=("Segoe UI", 20, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa"
        ).pack(side="left", padx=20)

        # Separator line
        separator = tk.Frame(self.frame, bg="#dcdde1", height=2)
        separator.pack(fill="x", padx=20, pady=(0, 20))

        # Top section (buttons + search)
        top = tk.Frame(self.frame, bg="#f5f6fa")
        top.pack(fill="x", padx=20, pady=(0, 15))

        # Button frame (left side)
        btn_frame = tk.Frame(top, bg="#f5f6fa")
        btn_frame.pack(side="left")

        # Add Category button with icon
        self.add_btn = tk.Button(
            btn_frame,
            text="➕ Add New",
            command=self.open_add_modal,
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        # Hover effect for Add button
        self.add_btn.bind(
            "<Enter>", lambda e: self.add_btn.config(bg="#2980b9"))
        self.add_btn.bind(
            "<Leave>", lambda e: self.add_btn.config(bg="#3498db"))

        # Delete button with icon
        self.delete_btn = tk.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            command=self.delete_asset,
            bg="#e74c3c",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        self.delete_btn.pack(side="left")

        # Hover effect for Delete button
        self.delete_btn.bind(
            "<Enter>", lambda e: self.delete_btn.config(bg="#c0392b"))
        self.delete_btn.bind(
            "<Leave>", lambda e: self.delete_btn.config(bg="#e74c3c"))

        # Search frame (right side)
        search_frame = tk.Frame(top, bg="#f5f6fa")
        search_frame.pack(side="right")

        # Search icon/label
        tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 12),
            bg="#f5f6fa",
            fg="#7f8c8d"
        ).pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            width=25
        )
        search_entry.pack(side="left", padx=5, pady=5)

        # Clear search button (appears when there's text)
        self.clear_btn = tk.Button(
            search_frame,
            text="✖",
            font=("Segoe UI", 9),
            bg="#f5f6fa",
            fg="#95a5a6",
            relief="flat",
            cursor="hand2",
            command=self.clear_search,
            padx=5
        )

        # Bind focus effects for search entry
        search_entry.bind("<FocusIn>", lambda e: search_entry.config(
            bg="#fff", highlightcolor="#3498db", highlightthickness=1))
        search_entry.bind("<FocusOut>", lambda e: search_entry.config(
            bg="white", highlightthickness=0))

        # Table Frame with border
        table_frame = tk.Frame(self.frame, bg="#dcdde1", padx=1, pady=1)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Table with improved styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground="#2c3e50",
            rowheight=30,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#34495e",
            foreground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        style.map("Treeview", background=[("selected", "#3498db")])

        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "Asset Tag",
                "Asset Name",
                "Serial",
                "Model",
                "Category",
                "Status"
            ),
            show="headings",
            height=15
        )

        self.tree.heading("Asset Tag", text="Asset_Tag")
        self.tree.heading("Asset Name", text="Asset_Name")
        self.tree.heading("Serial", text="Serial")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")

        self.tree.column("Asset Tag", width=80, anchor="center")
        self.tree.column("Asset Name", width=300, anchor="center")
        self.tree.column("Serial", width=300, anchor="center")
        self.tree.column("Model", width=300, anchor="center")
        self.tree.column("Category", width=300, anchor="center")
        self.tree.column("Status", width=300, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)

        # Status label at bottom
        self.status_label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 9),
            fg="#7f8c8d",
            bg="#f5f6fa"
        )
        self.status_label.pack(
            side="bottom",
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        self.load_assets()

        # # Top section (buttons + search)
        # top = tk.Frame(self.frame)
        # top.pack(fill="x", padx=10)

        # tk.Button(top, text="Add Asset", command=self.open_add_modal)\
        #     .pack(side="left", padx=5)

        # tk.Button(top, text="Checkout Asset", command=self.open_checkout_modal)\
        #     .pack(side="left", padx=5)

        # tk.Button(top, text="Checkin Asset", command=self.open_checkin_modal)\
        #     .pack(side="left", padx=5)

        # tk.Button(top, text="Delete Selected", command=self.delete_asset)\
        #     .pack(side="left", padx=5)

        # # Search field (right aligned)
        # tk.Label(top, text="Search:").pack(side="right", padx=5)

        # self.search_var = tk.StringVar()
        # self.search_var.trace("w", self.on_search)

        # search_entry = tk.Entry(top, textvariable=self.search_var)
        # search_entry.pack(side="right", padx=5)

        # # Table
        # self.tree = ttk.Treeview(
        #     self.frame,
        #     columns=("Asset Tag", "Asset Name", "Serial",
        #              "Model", "Category", "Status"),
        #     show="headings"
        # )

        # self.tree.heading("Asset Tag", text="Asset_Tag")
        # self.tree.heading("Asset Name", text="Asset_Name")
        # self.tree.heading("Serial", text="Serial")
        # self.tree.heading("Model", text="Model")
        # self.tree.heading("Category", text="Category")
        # self.tree.heading("Status", text="Status")

        # # self.tree.column("Asset_Tag", width=50)

        # self.tree.pack(fill="both", expand=True)

        # # Double click to edit
        # self.tree.bind("<Double-1>", self.on_double_click)

        # self.load_assets()

    def load_assets(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = asset_service.get_all(keyword)

        for asset in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    asset.tag,
                    asset.name,
                    asset.serial_number,
                    asset.model_name,
                    asset.category_name,
                    self.get_status_display(asset.status)
                )
            )

        self.assets = rows

    def clear_search(self):
        ...

    def get_status_display(self, status):
        status_map = {
            "Ready to Deploy": "🟢 Ready to Deploy",
            "Deployed": "🔵 Deployed",
            "Broken": "🔴 Broken",
            "Archived": "⚫ Archived",
            "Checked Out": "🔵 Checked Out",
        }

        return status_map.get(status, status)

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_assets(keyword)

    def open_add_modal(self):
        self.open_form("Add Asset")

    def open_form(self, title, asset: Optional[Asset] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x400")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # ---------------- LOAD MODELS ---------------- #
        models = model_service.get_all()
        model_map = {model.name:  model.id for model in models}

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
            tag_entry.insert(0, asset.tag)
            name_entry.insert(0, asset.name)
            serial_entry.insert(0, asset.serial_number)
            model_combo.set(asset.model_name if asset.model_name else "")
            status_combo.set(asset.status if asset.status else "")
            desc_entry.insert(0, asset.description)

        def save():
            selected_model = model_combo.get()
            selected_status = status_combo.get()

            if not selected_model:
                messagebox.showwarning("Warning", "Select a model")
                return

            model_id = model_map[selected_model]

            if asset:
                asset_service.update(
                    asset_id=asset.id,
                    name=name_entry.get(),
                    serialNumber=serial_entry.get(),
                    tag=tag_entry.get(),
                    status=selected_status,
                    model_id=model_id,
                    description=desc_entry.get(),
                )
            else:
                asset_service.insert(
                    name=name_entry.get(),
                    serialNumber=serial_entry.get(),
                    tag=tag_entry.get(),
                    status=selected_status,
                    model_id=model_id,
                    description=desc_entry.get(),
                )

            modal.destroy()
            self.load_assets()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def open_checkout_modal(self):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        asset = self.assets[selected_index]

        if not values:
            messagebox.showwarning("Warning", "Select an Asset")
            return

        # if asset.status != AssetStatus.READY_TO_DEPLOY:
        #     messagebox.showwarning("Warning", "Asset is not ready to deploy")
        #     return

        self.open_checkout_form("Checkout Asset", asset)

    def open_checkout_form(self, title, asset: Asset):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x400")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # Load employees
        employees = employee_service.get_all()
        employee_map = {employee.name: employee.id for employee in employees}

        print('employee_map-----------: ', employee_map)
        print('asset-----------: ', asset)

        checkout_status_map = {
            "Ready to Deploy",
        }

        info_frame = tk.Frame(modal)
        info_frame.pack(pady=10, fill="x")

        tk.Label(info_frame, text="Category:", font=("Arial", 10, "bold"))\
            .grid(row=0, column=0, sticky="w", padx=10)

        tk.Label(info_frame, text=asset.category_name or "-")\
            .grid(row=0, column=1, sticky="w")

        tk.Label(info_frame, text="Model:", font=("Arial", 10, "bold"))\
            .grid(row=1, column=0, sticky="w", padx=10)

        tk.Label(info_frame, text=asset.model_name or "-")\
            .grid(row=1, column=1, sticky="w")

        tk.Label(modal, text="Asset Name").pack(pady=5)
        name_entry = tk.Entry(modal)
        name_entry.pack()

        tk.Label(modal, text="Employee").pack()
        employee_combo = ttk.Combobox(
            modal,
            values=list(employee_map.keys()),
            state="readonly"
        )
        employee_combo.pack()

        tk.Label(modal, text="Expected Check-in Date").pack(pady=5)
        expected_checkin_entry = tk.Entry(modal)
        expected_checkin_entry.pack()

        expected_checkin_entry.insert(0, "2026-05-20")

        tk.Label(modal, text="Checkout Notes").pack(pady=5)
        notes_text = tk.Text(modal, height=4, width=30)
        notes_text.pack()

        # tk.Label(modal, text="Status").pack()
        # status_combo = ttk.Combobox(
        #     modal,
        #     values=list(checkout_status_map),
        #     state="readonly"
        # )
        # status_combo.pack()

        def save():
            selected_employee = employee_combo.get()

            employee_id = employee_map[selected_employee]
            expected_checkin_date = expected_checkin_entry.get()
            checkout_notes = notes_text.get("1.0", tk.END).strip()

            try:
                checkout_service.checkout_asset(
                    asset_id=asset.id,
                    employee_id=employee_id,
                    expected_checkin_date=expected_checkin_date,
                    checkout_notes=checkout_notes,
                )
            except Exception as e:
                messagebox.showerror("Error", str(e))

            modal.destroy()
            self.load_assets()

        tk.Button(modal, text="Checkout", command=save).pack(pady=10)

    def open_checkin_modal(self):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        asset = self.assets[selected_index]

        if not values:
            messagebox.showwarning("Warning", "Select an Asset")
            return

        # if asset.status != AssetStatus.CHECKED_OUT:
        #     messagebox.showwarning("Warning", "Asset is not checked out")
        #     return

        self.open_checkin_form("Checkin Asset", asset)

    def open_checkin_form(self, title, asset: Asset):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x400")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        checkin_status_list = [
            AssetStatus.PENDING.value,
            AssetStatus.READY_TO_DEPLOY.value,
            AssetStatus.ARCHIVED.value,
            AssetStatus.BROKEN.value,
            AssetStatus.LOST_STOLEN.value,
            AssetStatus.OUT_FOR_DIAGNOSTICS.value,
        ]

        info_frame = tk.Frame(modal)
        info_frame.pack(pady=10, fill="x")

        tk.Label(info_frame, text="Category:", font=("Arial", 10, "bold"))\
            .grid(row=0, column=0, sticky="w", padx=10)

        tk.Label(info_frame, text=asset.category_name or "-")\
            .grid(row=0, column=1, sticky="w")

        tk.Label(info_frame, text="Model:", font=("Arial", 10, "bold"))\
            .grid(row=1, column=0, sticky="w", padx=10)

        tk.Label(info_frame, text=asset.model_name or "-")\
            .grid(row=1, column=1, sticky="w")

        tk.Label(modal, text="Status").pack()
        status_combo = ttk.Combobox(
            modal,
            values=checkin_status_list,
            state="readonly"
        )
        status_combo.pack()

        tk.Label(modal, text="Return Notes").pack(pady=5)
        notes_text = tk.Text(modal, height=4, width=30)
        notes_text.pack()

        def save():
            selected_status = status_combo.get()

            if not selected_status:
                messagebox.showwarning("Warning", "Select status")
                return

            return_notes = notes_text.get("1.0", tk.END).strip()

            try:
                checkout_service.checkin_asset(
                    asset_id=asset.id,
                    status=selected_status,
                    return_notes=return_notes,
                )
            except Exception as e:
                messagebox.showerror("Error", str(e))

            modal.destroy()
            self.load_assets()

        tk.Button(modal, text="Checkin", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        asset = self.assets[selected_index]

        if values:
            self.open_form("Edit Asset", asset)

    def delete_asset(self):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        asset = self.assets[selected_index]

        if not values:
            messagebox.showwarning("Warning", "Select a row")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this asset?")
        if not confirm:
            return

        asset_service.delete(asset.id)
        self.load_assets()
