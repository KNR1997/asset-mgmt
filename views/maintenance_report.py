import tkinter as tk
from tkinter import ttk, messagebox
from services import asset_service as asset_service
from services import repairs_service as repairs_service
from enums.asset_status import AssetStatus
from tkinter import ttk, messagebox, filedialog
import csv


class MaintenanceReportView:
    def __init__(self, parent):
        self.broken_assets = []
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="🛠 Maintenance Reports",
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

        self.export_btn = tk.Button(
            btn_frame,
            text="⬇ Export CSV",
            command=self.export_csv,
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )

        self.export_btn.pack(side="left")

        # Hover effect
        self.export_btn.bind(
            "<Enter>", lambda e: self.export_btn.config(bg="#219150")
        )

        self.export_btn.bind(
            "<Leave>", lambda e: self.export_btn.config(bg="#27ae60")
        )

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
                "SerialNumber",
                "Model",
                "Category",
                "Repair Date",
                "Repair Cost",
                "Status",
                "Performed by",
                "Warranty Covered",
            ),
            show="headings",
            height=15
        )

        self.tree.heading("Asset Tag", text="Asset Tag")
        self.tree.heading("SerialNumber", text="SerialNumber")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Repair Date", text="Repair Date")
        self.tree.heading("Repair Cost", text="Repair Cost")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Performed by", text="Performed By")
        self.tree.heading("Warranty Covered", text="Warranty Covered")

        self.tree.column("Asset Tag", width=80, anchor="center")
        self.tree.column("SerialNumber", width=80, anchor="center")
        self.tree.column("Model", width=80, anchor="center")
        self.tree.column("Category", width=80, anchor="center")
        self.tree.column("Repair Date", width=80, anchor="center")
        self.tree.column("Repair Cost", width=300, anchor="center")
        self.tree.column("Status", width=150, anchor="center")
        self.tree.column("Performed by", width=150, anchor="center")
        self.tree.column("Warranty Covered", width=150, anchor="center")

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

        self.load_maintenance_reports()

    def load_maintenance_reports(self, keyword=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = repairs_service.get_all(keyword)

        for repair in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    repair.asset_tag,
                    repair.asset_serial_number,
                    repair.asset_model_name,
                    repair.asset_category_name,
                    repair.repair_date,
                    repair.repair_cost,
                    repair.status,
                    repair.performed_by,
                    repair.warranty_covered,
                    # self.get_status_display(repair.status),
                )
            )

        self.broken_assets = rows

    def export_csv(self):

        # Ask save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Maintenance Report"
        )

        # User cancelled
        if not file_path:
            return

        try:

            with open(file_path, mode="w", newline="", encoding="utf-8") as file:

                writer = csv.writer(file)

                # Write headers
                writer.writerow([
                    "Asset Tag",
                    "Serial Number",
                    "Category",
                    "Model",
                    "Repair Date",
                    "Repair Cost",
                    "Status",
                    "Performed By",
                    "Warranty Covered"
                ])

                # Write table rows
                for item in self.tree.get_children():

                    row = self.tree.item(item)["values"]

                    writer.writerow(row)

            messagebox.showinfo(
                "Success",
                "CSV report exported successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to export CSV:\n{str(e)}"
            )

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_maintenance_reports(keyword)

    def get_status_display(self, status):
        status_map = {
            "Ready to Deploy": "🟢 Ready to Deploy",
            "Deployed": "🔵 Deployed",
            "Broken": "🔴 Broken",
            "Archived": "⚫ Archived",
            "Checked Out": "🔵 Checked Out",
        }

        return status_map.get(status, status)

    def clear_search(self):
        ...

    def open_add_modal(self):
        self.open_form("Repair Asset")

    def open_form(self, title):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        broken_asset = self.broken_assets[selected_index]
    
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x450")

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        tk.Label(modal, text="Repair Date").pack(pady=5)
        repair_date_entry = tk.Entry(modal)
        repair_date_entry.pack()

        tk.Label(modal, text="Repair Cost").pack(pady=5)
        repair_cost_entry = tk.Entry(modal)
        repair_cost_entry.pack()

        tk.Label(modal, text="Notes").pack(pady=5)
        notes_entry = tk.Entry(modal)
        notes_entry.pack()

        tk.Label(modal, text="Performed by").pack(pady=5)
        performed_by_entry = tk.Entry(modal)
        performed_by_entry.pack()

        if not broken_asset:
            ...
            # name_entry.insert(0, broken_asset.name)
            # url_entry.insert(0, manufacturer.url)
            # support_url_entry.insert(0, manufacturer.supportURL)

        def save():
            repair_date = repair_date_entry.get()
            repair_cost = repair_cost_entry.get()
            notes = notes_entry.get()
            performed_by = performed_by_entry.get()

            if not repair_cost:
                messagebox.showwarning("Warning", "Enter repair cost")
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
                    performed_by=performed_by
                )

                asset_service.update_status(
                    asset_id=broken_asset.id,
                    status=AssetStatus.READY_TO_DEPLOY,
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save category: {str(e)}")

            messagebox.showinfo(
                "Success", "Asset Ready to Use!")
                
            modal.destroy()
            self.load_maintenance_reports()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        ...
