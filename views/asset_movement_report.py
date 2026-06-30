import csv
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import ttk, messagebox, filedialog
from utils.asset.status_with_icon import status_with_icon
from services import asset_service as asset_service
from services import asset_movement_service as asset_movement_service


class AssetMovementReportView:
    def __init__(self, parent):
        self.asset_movements = []
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="🛠 Asset Movement Reports",
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
                "Model",
                "Category",
                "Checkout Employee",
                "Checkout Date",
                "Expected Checkin Date",
                "Checkin Date",
                "Status",
                "Return Condition",
            ),
            show="headings",
            height=15
        )

        self.tree.heading("Asset Tag", text="Asset Tag")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Checkout Employee", text="Checkout Employee")
        self.tree.heading("Checkout Date", text="Checkout Date")
        self.tree.heading("Expected Checkin Date",
                          text="Expected Checkin Date")
        self.tree.heading("Checkin Date", text="Checkin Date")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Return Condition", text="Return Condition")

        self.tree.column("Asset Tag", width=80, anchor="center")
        self.tree.column("Model", width=80, anchor="center")
        self.tree.column("Category", width=80, anchor="center")
        self.tree.column("Checkout Employee", width=80, anchor="center")
        self.tree.column("Checkout Date", width=80, anchor="center")
        self.tree.column("Expected Checkin Date", width=80, anchor="center")
        self.tree.column("Checkin Date", width=80, anchor="center")
        self.tree.column("Status", width=80, anchor="center")
        self.tree.column("Return Condition", width=80, anchor="center")

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

        rows = asset_movement_service.get_all(keyword)

        for repair in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    repair.asset_tag,
                    repair.model_name,
                    repair.category_name,
                    repair.employee_name,
                    repair.checkout_date,
                    repair.expected_checkin_date,
                    repair.actual_checkin_date,
                    "✅ Active" if repair.is_active else "🚫 Inactive",
                    status_with_icon(repair.return_condition),
                )
            )

        self.asset_movements = rows

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
                    "Model",
                    "Category",
                    "Checkout Employee",
                    "Checkout Date",
                    "Expected Checkin Date",
                    "Checkin Date",
                    "Status",
                    "Return Condition",
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

        # Show clear button if search has text
        if keyword and not self.clear_btn.winfo_ismapped():
            self.clear_btn.pack(side="left", padx=(0, 5))
        elif not keyword and self.clear_btn.winfo_ismapped():
            self.clear_btn.pack_forget()

    def clear_search(self):
        ...

    def on_double_click(self, event):
        ...
