import tkinter as tk
from tkinter import ttk, messagebox
from utils.asset.status_with_icon import status_with_icon
from services import asset_service as asset_service
from services import model_service as model_service
from services import employee_service as employee_service
from services import checkout_service as checkout_service
from models.asset import Asset
from typing import Optional
from enums.asset_status import AssetStatus
from tkcalendar import DateEntry
from datetime import datetime, timedelta


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

        # Add Checkout button with icon
        self.checkout_btn = tk.Button(
            btn_frame,
            text="🔺 Checkout",
            command=self.open_checkout_modal,
            bg="#9412c7",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        self.checkout_btn.pack(side="left", padx=(0, 10))

        # Hover effect for Add button
        self.checkout_btn.bind(
            "<Enter>", lambda e: self.checkout_btn.config(bg="#c068e2"))
        self.checkout_btn.bind(
            "<Leave>", lambda e: self.checkout_btn.config(bg="#9412c7"))

        # Add Checkin button with icon
        self.checkin_btn = tk.Button(
            btn_frame,
            text="🔻 Checkin",
            command=self.open_checkin_modal,
            bg="#4819ca",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        self.checkin_btn.pack(side="left", padx=(0, 10))

        # Hover effect for Add button
        self.checkin_btn.bind(
            "<Enter>", lambda e: self.checkin_btn.config(bg="#7c5bd6"))
        self.checkin_btn.bind(
            "<Leave>", lambda e: self.checkin_btn.config(bg="#4819ca"))

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

        # Status Filter
        self.status_filter_var = tk.StringVar(value="All")

        status_options = [
            "All",
            AssetStatus.PENDING.value,
            AssetStatus.READY_TO_DEPLOY.value,
            AssetStatus.DEPLOYED.value,
            AssetStatus.BROKEN.value,
            AssetStatus.ARCHIVED.value,
            AssetStatus.LOST_STOLEN.value,
            AssetStatus.OUT_FOR_DIAGNOSTICS.value,
            AssetStatus.OUT_FOR_REPAIR.value,
        ]

        status_combo = ttk.Combobox(
            search_frame,
            textvariable=self.status_filter_var,
            values=status_options,
            state="readonly",
            width=20
        )

        status_combo.pack(side="left", padx=5)
        status_combo.bind("<<ComboboxSelected>>", self.on_filter_change)

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
                "Serial Number",
                "Model",
                "Category",
                "Status",
                "Checked Out to"
            ),
            show="headings",
            height=15
        )

        self.tree.heading("Asset Tag", text="Asset Tag")
        self.tree.heading("Asset Name", text="Asset Name")
        self.tree.heading("Serial Number", text="Serial Number")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Checked Out to", text="Checked Out to")

        self.tree.column("Asset Tag", width=80, anchor="center")
        self.tree.column("Asset Name", width=300, anchor="center")
        self.tree.column("Serial Number", width=150, anchor="center")
        self.tree.column("Model", width=150, anchor="center")
        self.tree.column("Category", width=150, anchor="center")
        self.tree.column("Status", width=200, anchor="center")
        self.tree.column("Checked Out to", width=300, anchor="center")

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

    def on_filter_change(self, event=None):
        keyword = self.search_var.get()
        status = self.status_filter_var.get()

        self.load_assets(keyword, status)

    def load_assets(self, keyword="", status="All"):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = asset_service.get_all(keyword, status)

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
                    status_with_icon(asset.status),
                    asset.current_checkout_employee_name,
                )
            )

        self.assets = rows

    def clear_search(self):
        self.search_var.set("")
        self.status_filter_var.set("All")
        self.load_assets()

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_assets(keyword)

        # Show clear button if search has text
        if keyword and not self.clear_btn.winfo_ismapped():
            self.clear_btn.pack(side="left", padx=(0, 5))
        elif not keyword and self.clear_btn.winfo_ismapped():
            self.clear_btn.pack_forget()

    def open_add_modal(self):
        self.open_form("Add Asset")

    def open_form(self, title, asset: Optional[Asset] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x450")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # LOAD MODELS
        models = model_service.get_all()
        model_map = {model.name:  model.id for model in models}

        status_map = {
            AssetStatus.PENDING.value,
            AssetStatus.READY_TO_DEPLOY.value,
            AssetStatus.ARCHIVED.value,
            AssetStatus.BROKEN.value,
            AssetStatus.LOST_STOLEN.value,
            AssetStatus.OUT_FOR_DIAGNOSTICS.value,
            AssetStatus.OUT_FOR_REPAIR.value,
        }

        # Helper function to create required label
        def create_label(parent, text, required=False):
            frame = tk.Frame(parent)
            frame.pack(pady=(10, 0))

            label = tk.Label(frame, text=text)
            label.pack(side=tk.LEFT)

            if required:
                asterisk = tk.Label(frame, text=" *", fg="red",
                                    font=("Arial", 10, "bold"))
                asterisk.pack(side=tk.LEFT)

            return frame

        # Asset Name
        create_label(modal, "Asset Name").pack()
        name_entry = tk.Entry(modal)
        name_entry.pack(fill=tk.X, padx=20)

        # Tag (Required)
        create_label(modal, "Asset Tag", required=True)
        tag_entry = tk.Entry(modal)
        tag_entry.pack(fill=tk.X, padx=20)

        # Serial Number (Required)
        create_label(modal, "Serial No.", required=True)
        serial_number_entry = tk.Entry(modal)
        serial_number_entry.pack(fill=tk.X, padx=20)

        # Asset Model (Required)
        create_label(modal, "Model", required=True)
        model_combo = ttk.Combobox(
            modal,
            values=list(model_map.keys()),
            state="readonly"
        )
        model_combo.pack(fill=tk.X, padx=20)

        # Status (Required)
        create_label(modal, "Status", required=True)
        status_combo = ttk.Combobox(
            modal,
            values=list(status_map),
            state="readonly"
        )
        status_combo.pack(fill=tk.X, padx=20)

        # Description
        create_label(modal, "Description")
        desc_entry = tk.Entry(modal)
        desc_entry.pack(fill=tk.X, padx=20)

        # Add required fields hint
        # hint_label = tk.Label(
        #     modal,
        #     text="* Required fields",
        #     fg="gray",
        #     font=("Arial", 8, "italic")
        # )
        # hint_label.pack(pady=(5, 0))

        if asset:
            tag_entry.insert(0, asset.tag)
            name_entry.insert(0, asset.name)
            serial_number_entry.insert(0, asset.serial_number)
            model_combo.set(asset.model_name if asset.model_name else "")
            status_combo.set(asset.status if asset.status else "")
            desc_entry.insert(0, asset.description)

        def save():
            name = name_entry.get().strip()
            serial_number = serial_number_entry.get().strip()
            tag = tag_entry.get().strip()
            selected_status = status_combo.get()
            selected_model = model_combo.get()
            description = desc_entry.get().strip()

            if not tag:
                messagebox.showwarning("Warning", "Plese provide a tag")
                return

            if not serial_number:
                messagebox.showwarning(
                    "Warning", "Please provide a serial number")
                return

            if not selected_model:
                messagebox.showwarning("Warning", "Please select a model")
                return

            if not selected_status:
                messagebox.showwarning("Warning", "Please select a status")
                return

            model_id = model_map[selected_model]

            try:
                if asset:
                    # Pass the data object along with asset_id
                    asset_service.update(
                        asset_id=asset.id,
                        name=name,
                        serialNumber=serial_number,
                        tag=tag,
                        status=selected_status,
                        model_id=model_id,
                        description=description,
                    )
                    messagebox.showinfo(title, "Asset updated successfully")
                    # success("Success!", "Asset updated successfully")
                else:
                    # Pass the data object directly
                    asset_service.insert(
                        name=name,
                        serialNumber=serial_number,
                        tag=tag,
                        status=selected_status,
                        model_id=model_id,
                        description=description,
                    )
                    messagebox.showinfo(title, "Asset created successfully")
                    # success("Success!", "Asset created successfully")
                modal.destroy()
                self.load_assets()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save asset: {str(e)}")

        # Save and Cancel buttons
        btn_frame = tk.Frame(modal)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="💾 Save",
            command=save,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame,
            text="✖ Cancel",
            command=modal.destroy,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2"
        ).pack(side="left")

        # Bind keyboard shortcuts
        modal.bind("<Return>", lambda e: save())
        modal.bind("<Escape>", lambda e: modal.destroy())

    def open_checkout_modal(self):
        selected = self.tree.focus()

        if not selected:
            messagebox.showwarning("Warning", "Select an Asset")
            return

        selected_index = self.tree.index(selected)
        asset = self.assets[selected_index]

        if asset.status == AssetStatus.DEPLOYED:
            messagebox.showwarning("Warning", "Asset is already deployed")
            return

        if asset.status == AssetStatus.BROKEN:
            messagebox.showwarning("Warning", "Asset is broken")
            return

        self.open_checkout_form("Checkout Asset", asset)

    def open_checkout_form(self, title, asset: Asset):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x450")  # Slightly taller for calendar

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # Load employees
        employees = employee_service.get_all()
        employee_map = {employee.name: employee.id for employee in employees}

        # Helper function to create required label
        def create_label(parent, text, required=False):
            frame = tk.Frame(parent)
            frame.pack(pady=(10, 0))

            label = tk.Label(frame, text=text)
            label.pack(side=tk.LEFT)

            if required:
                asterisk = tk.Label(frame, text=" *", fg="red",
                                    font=("Arial", 10, "bold"))
                asterisk.pack(side=tk.LEFT)

            return frame

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

        # Asset Name (read-only since it's checkout)
        create_label(modal, "Asset Name", required=True)
        name_entry = tk.Entry(modal)
        name_entry.insert(0, asset.name)
        name_entry.pack(fill=tk.X, padx=20)

        # Employee Selection
        create_label(modal, "Employee", required=True)
        employee_combo = ttk.Combobox(
            modal,
            values=list(employee_map.keys()),
            state="readonly"
        )
        employee_combo.pack(fill=tk.X, padx=20)

        # Date Picker with tkcalendar
        create_label(modal, "Expected Check-in Date", required=True)

        # Create a frame for the date entry with some padding
        date_frame = tk.Frame(modal)
        date_frame.pack(fill=tk.X, padx=20)

        # Default to 7 days from now
        default_date = datetime.now() + timedelta(days=7)

        expected_checkin_entry = DateEntry(
            date_frame,
            width=25,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=default_date.year,
            month=default_date.month,
            day=default_date.day,
            date_pattern='yyyy-mm-dd',  # Format: 2026-05-20
            locale='en_US'
        )
        expected_checkin_entry.pack(fill=tk.X, pady=(0, 5))

        # Optional: Add a "Today" and "+7 days" quick buttons
        quick_btn_frame = tk.Frame(modal)
        quick_btn_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        def set_date(days_offset):
            new_date = datetime.now() + timedelta(days=days_offset)
            expected_checkin_entry.set_date(new_date)

        tk.Button(
            quick_btn_frame,
            text="Today",
            command=lambda: set_date(0),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=10,
            pady=2,
            font=("Arial", 8)
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            quick_btn_frame,
            text="+3 days",
            command=lambda: set_date(3),
            bg="#2ecc71",
            fg="white",
            relief="flat",
            padx=10,
            pady=2,
            font=("Arial", 8)
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            quick_btn_frame,
            text="+7 days",
            command=lambda: set_date(7),
            bg="#f39c12",
            fg="white",
            relief="flat",
            padx=10,
            pady=2,
            font=("Arial", 8)
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            quick_btn_frame,
            text="+14 days",
            command=lambda: set_date(14),
            bg="#9b59b6",
            fg="white",
            relief="flat",
            padx=10,
            pady=2,
            font=("Arial", 8)
        ).pack(side="left")

        # Checkout Notes
        create_label(modal, "Checkout Notes")
        notes_text = tk.Text(modal, height=4, width=30)
        notes_text.pack(fill=tk.X, padx=20)

        def save():
            name = name_entry.get().strip()
            selected_employee = employee_combo.get()

            if not name:
                messagebox.showwarning(
                    "Warning", "Please a name for the Asset")
                return

            if not selected_employee:
                messagebox.showwarning("Warning", "Please select an employee")
                return

            # Get the date as string
            try:
                expected_checkin_date = expected_checkin_entry.get_date()
                # Format as string for your service
                date_str = expected_checkin_date.strftime('%Y-%m-%d')
            except Exception as e:
                messagebox.showerror("Error", "Invalid date selected")
                return

            employee_id = employee_map[selected_employee]
            checkout_notes = notes_text.get("1.0", tk.END).strip()

            try:
                checkout_service.checkout_asset(
                    asset_id=asset.id,
                    asset_name=name,
                    employee_id=employee_id,
                    expected_checkin_date=date_str,
                    checkout_notes=checkout_notes,
                )
                modal.destroy()
                messagebox.showinfo(title, "Asset checkout successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

            self.load_assets()

        tk.Button(modal, text="Checkout", command=save, bg="#2ecc71", fg="white",
                  font=("Arial", 10, "bold"), padx=20, pady=8).pack(pady=10)

    def open_checkin_modal(self):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        asset = self.assets[selected_index]

        if not values:
            messagebox.showwarning("Warning", "Select an Asset")
            return

        if asset.status == AssetStatus.READY_TO_DEPLOY:
            messagebox.showwarning("Warning", "Asset is not yet checkout")
            return

        if asset.status == AssetStatus.BROKEN:
            messagebox.showwarning("Warning", "Asset is broken")
            return

        if asset.status == AssetStatus.LOST_STOLEN:
            messagebox.showwarning("Warning", "Asset is Lost or Stolen")
            return

        if asset.status == AssetStatus.ARCHIVED:
            messagebox.showwarning("Warning", "Asset is Archived")
            return

        if asset.status == AssetStatus.PENDING:
            messagebox.showwarning("Warning", "Asset is Pending")
            return

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

        # Helper function to create required label
        def create_label(parent, text, required=False):
            frame = tk.Frame(parent)
            frame.pack(pady=(10, 0))

            label = tk.Label(frame, text=text)
            label.pack(side=tk.LEFT)

            if required:
                asterisk = tk.Label(frame, text=" *", fg="red",
                                    font=("Arial", 10, "bold"))
                asterisk.pack(side=tk.LEFT)

            return frame

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

        create_label(modal, "Status", required=True)
        status_combo = ttk.Combobox(
            modal,
            values=checkin_status_list,
            state="readonly"
        )
        status_combo.pack(fill=tk.X, padx=20)

        create_label(modal, "Check-in Date", required=True)
        date_frame = tk.Frame(modal)
        date_frame.pack(fill=tk.X, padx=20)
        # Default today
        default_date = datetime.now()
        checkin_entry = DateEntry(
            date_frame,
            width=25,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=default_date.year,
            month=default_date.month,
            day=default_date.day,
            date_pattern='yyyy-mm-dd',  # Format: 2026-05-20
            locale='en_US'
        )
        checkin_entry.pack(fill=tk.X, pady=(0, 5))

        create_label(modal, "Return Notes")
        notes_text = tk.Text(modal, height=4, width=30)
        notes_text.pack(fill=tk.X, padx=20)

        def save():
            selected_status = status_combo.get()

            if not selected_status:
                messagebox.showwarning("Warning", "Select status")
                return

            # Get the date as string
            try:
                checkin_date = checkin_entry.get_date()
                # Format as string for your service
                date_str = checkin_date.strftime('%Y-%m-%d')
            except Exception as e:
                messagebox.showerror("Error", "Invalid date selected")
                return

            return_notes = notes_text.get("1.0", tk.END).strip()

            try:
                checkout_service.checkin_asset(
                    asset_id=asset.id,
                    status=selected_status,
                    checkin_date=date_str,
                    return_notes=return_notes,
                )
                modal.destroy()
                messagebox.showinfo(title, "Asset checkin successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

            self.load_assets()

        tk.Button(modal, text="Checkin", command=save, bg="#2ecc71", fg="white",
                  font=("Arial", 10, "bold"), padx=20, pady=8).pack(pady=10)

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
