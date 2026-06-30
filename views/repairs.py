import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from enums.asset_status import AssetStatus
from services import asset_service as asset_service
from services import repairs_service as repairs_service
from utils.asset.status_with_icon import status_with_icon


class RepairsView:
    def __init__(self, parent):
        self.broken_assets = []
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="🛠 Repairs",
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
            text="➕ Repair Asset",
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
                # "Asset Name",
                "Serial Number",
                "Model",
                "Category",
                "Status",
            ),
            show="headings",
            height=15
        )

        self.tree.heading("Asset Tag", text="Asset Tag")
        # self.tree.heading("Asset Name", text="Asset Name")
        self.tree.heading("Serial Number", text="Serial Number")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")

        self.tree.column("Asset Tag", width=80, anchor="center")
        # self.tree.column("Asset Name", width=300, anchor="center")
        self.tree.column("Serial Number", width=150, anchor="center")
        self.tree.column("Model", width=150, anchor="center")
        self.tree.column("Category", width=150, anchor="center")
        self.tree.column("Status", width=200, anchor="center")

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

        self.load_broken_assets()

    def load_broken_assets(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = asset_service.get_all_broken(keyword)

        for asset in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    asset.tag,
                    # asset.name,
                    asset.serial_number,
                    asset.model_name,
                    asset.category_name,
                    status_with_icon(asset.status),
                )
            )

        self.broken_assets = rows

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_broken_assets(keyword)

        # Show clear button if search has text
        if keyword and not self.clear_btn.winfo_ismapped():
            self.clear_btn.pack(side="left", padx=(0, 5))
        elif not keyword and self.clear_btn.winfo_ismapped():
            self.clear_btn.pack_forget()

    def clear_search(self):
        """Clear search entry"""
        self.search_var.set("")
        self.search_entry = self.clear_btn.master.winfo_children()[1]
        self.search_entry.focus()

    def open_add_modal(self):
        self.open_form("Repair Asset")

    def open_form(self, title):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        broken_asset = self.broken_assets[selected_index]

        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x550")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

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

        tk.Label(info_frame, text="Asset Tag:", font=("Arial", 10, "bold"))\
            .grid(row=0, column=0, sticky="w", padx=10)

        tk.Label(info_frame, text=broken_asset.tag or "-")\
            .grid(row=0, column=1, sticky="w")

        tk.Label(info_frame, text="Model Name:", font=("Arial", 10, "bold"))\
            .grid(row=1, column=0, sticky="w", padx=10)

        tk.Label(info_frame, text=broken_asset.model_name or "-")\
            .grid(row=1, column=1, sticky="w")

        tk.Label(info_frame, text="Category Name:", font=("Arial", 10, "bold"))\
            .grid(row=2, column=0, sticky="w", padx=10)

        tk.Label(info_frame, text=broken_asset.category_name or "-")\
            .grid(row=2, column=1, sticky="w")

        create_label(modal, "Repair Date", required=True)
        date_frame = tk.Frame(modal)
        date_frame.pack(fill=tk.X, padx=20)
        # Default today
        default_date = datetime.now()
        repair_date_entry = DateEntry(
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
        repair_date_entry.pack(fill=tk.X, pady=(0, 5))

        create_label(modal, "Repair Cost", required=True)
        repair_cost_entry = tk.Entry(modal)
        repair_cost_entry.pack(fill=tk.X, padx=20)

        create_label(modal, "Warranty Covered", required=True)
        warranty_covered_combo = ttk.Combobox(
            modal,
            values=list({
                "Yes", "No"
            }),
            state="readonly"
        )
        warranty_covered_combo.pack(fill=tk.X, padx=20)

        create_label(modal, "Performed by", required=True)
        performed_by_entry = tk.Entry(modal)
        performed_by_entry.pack(fill=tk.X, padx=20)

        create_label(modal, "Notes")
        notes_entry = tk.Entry(modal)
        notes_entry.pack(fill=tk.X, padx=20)

        if not broken_asset:
            ...
            # name_entry.insert(0, broken_asset.name)
            # url_entry.insert(0, manufacturer.url)
            # support_url_entry.insert(0, manufacturer.supportURL)

        def save():
            repair_date = repair_date_entry.get()
            repair_cost = repair_cost_entry.get()
            notes = notes_entry.get()
            warranty_covered = warranty_covered_combo.get()
            performed_by = performed_by_entry.get()

            if not repair_cost:
                messagebox.showwarning("Warning", "Enter repair cost")
                return

            if not performed_by:
                messagebox.showwarning("Warning", "Enter performed by details")
                return

            try:
                repairs_service.insert(
                    asset_id=broken_asset.id,
                    checkout_id=1,
                    repair_date=repair_date,
                    repair_cost=repair_cost,
                    status='Completed',
                    description='',
                    notes=notes,
                    performed_by=performed_by,
                    warranty_covered=warranty_covered,
                )

                asset_service.update_status(
                    asset_id=broken_asset.id,
                    status=AssetStatus.READY_TO_DEPLOY,
                )
                modal.destroy()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save category: {str(e)}")

            messagebox.showinfo(
                "Success", "Asset Ready to Use!")

            self.load_broken_assets()

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

    def on_double_click(self, event):
        ...
