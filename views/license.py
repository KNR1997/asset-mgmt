import tkinter as tk
from tkinter import ttk, messagebox
from services import license_service as service
from services import type_service as type_service
from models.license import License
from typing import Optional
from enums.license_category import LicenseCategory
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from services import manufacturer_service as manufacturer_service

class LicensesView:
    def __init__(self, parent):
        self.licenses = []
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="📜 Licenses",
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

        # Add License button with icon
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
            command=self.delete_license,
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
                "Name", 
                "Product Key",
                "Expiration Date",
                "Licensed to Email",
                "Licensed To",
                "Manufacturer",
                "Min QTY",
                "Total",
            ),
            show="headings",
            height=15
        )

        self.tree.heading("Name", text="Name")
        self.tree.heading("Product Key", text="Product Key")
        self.tree.heading("Expiration Date", text="Expiration Date")
        self.tree.heading("Licensed to Email", text="Licensed to Email")
        self.tree.heading("Licensed To", text="Licensed To")
        self.tree.heading("Manufacturer", text="Manufacturer")
        self.tree.heading("Min QTY", text="Min QTY")
        self.tree.heading("Total", text="Total")
        # self.tree.heading("Avail", text="Avail")

        self.tree.column("Name", width=300, anchor="center")
        self.tree.column("Product Key", width=200, anchor="center")
        self.tree.column("Expiration Date", width=150, anchor="center")
        self.tree.column("Licensed to Email", width=150, anchor="center")
        self.tree.column("Licensed To", width=150, anchor="center")
        self.tree.column("Manufacturer", width=150, anchor="center")
        self.tree.column("Min QTY", width=50, anchor="center")
        self.tree.column("Total", width=50, anchor="center")
        # self.tree.column("Avail", width=300, anchor="center")

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

        self.load_licenses()

    def load_licenses(self, keyword=""):
        # Clear existing items
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = service.get_all(keyword)

        for license in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    # license.id,
                    license.softwareName,
                    license.productKey,
                    license.expirationDate,
                    license.licensedToEmail,
                    license.licensedTo,
                    license.manufacturer_name,
                    license.minQuantity,
                    license.seats,
                )
            )

        self.licenses = rows

        # Update status label
        count = len(rows)
        self.status_label.config(text=f"📊 Total categories: {count}")

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_licenses(keyword)

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
        self.open_form("Add License")

    def open_form(self, title, license: Optional[License] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("450x600")  # Increased height for date pickers

        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        manufacturers = manufacturer_service.get_all()
        manufacturer_map = {m.name: m.id for m in manufacturers}

        license_category_map = {
            LicenseCategory.GRAPHIC_SOFTWARE.value,
            LicenseCategory.OFFICE_SOFTWARE.value,
            # Add more categories as needed
        }

        # Helper function to create required label
        def create_label(parent, text, required=False):
            frame = tk.Frame(parent)
            frame.pack(pady=(10, 0))
            
            label = tk.Label(frame, text=text)
            label.pack(side=tk.LEFT)
            
            if required:
                asterisk = tk.Label(frame, text=" *", fg="red", font=("Arial", 10, "bold"))
                asterisk.pack(side=tk.LEFT)
            
            return frame
        
        # Create a scrollable frame for fields
        main_frame = tk.Frame(modal)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Software Name (Required)
        create_label(scrollable_frame, "Software Name", required=True)
        software_name_entry = tk.Entry(scrollable_frame)
        software_name_entry.pack(fill=tk.X, padx=20)

        # Category Name (Required)
        create_label(scrollable_frame, "Category Name", required=True)
        license_category_combo = ttk.Combobox(
            scrollable_frame,
            values=list(license_category_map),
            state="readonly"
        )
        license_category_combo.pack(fill=tk.X, padx=20)

        # Seats
        create_label(scrollable_frame, "Seats")
        seats_entry = tk.Entry(scrollable_frame)
        seats_entry.pack(fill=tk.X, padx=20)

        # Product Key
        create_label(scrollable_frame, "Product Key")
        product_key_entry = tk.Entry(scrollable_frame)
        product_key_entry.pack(fill=tk.X, padx=20)

        # Manufacturer
        create_label(scrollable_frame, "Manufacturer")
        manufacturer_combo = ttk.Combobox(
            scrollable_frame,
            values=list(manufacturer_map.keys()),
            state="readonly"
        )
        manufacturer_combo.pack(fill=tk.X, padx=20)

        # Licensed To
        create_label(scrollable_frame, "Licensed To")
        licensed_to_entry = tk.Entry(scrollable_frame)
        licensed_to_entry.pack(fill=tk.X, padx=20)

        # Licensed to Email
        create_label(scrollable_frame, "Licensed to Email")
        licensed_to_email_entry = tk.Entry(scrollable_frame)
        licensed_to_email_entry.pack(fill=tk.X, padx=20)

        # Purchase Cost
        create_label(scrollable_frame, "Purchase Cost")
        purchase_cost_entry = tk.Entry(scrollable_frame)
        purchase_cost_entry.pack(fill=tk.X, padx=20)

        # Purchase Date with Date Picker
        create_label(scrollable_frame, "Purchase Date")
        purchase_date_frame = tk.Frame(scrollable_frame)
        purchase_date_frame.pack(fill=tk.X, padx=20, pady=(5, 0))
        
        # Default to today if no date
        default_date = datetime.now()
        
        purchase_date_entry = DateEntry(
            purchase_date_frame,
            width=25,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=default_date.year,
            month=default_date.month,
            day=default_date.day,
            date_pattern='yyyy-mm-dd',
            locale='en_US'
        )
        purchase_date_entry.pack(side="left", fill=tk.X, expand=True)
        
        # Quick "Today" button for purchase date
        tk.Button(
            purchase_date_frame,
            text="Today",
            command=lambda: purchase_date_entry.set_date(datetime.now()),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=10,
            font=("Arial", 8)
        ).pack(side="right", padx=(5, 0))

        # Expiration Date with Date Picker
        create_label(scrollable_frame, "Expiration Date")
        expiration_date_frame = tk.Frame(scrollable_frame)
        expiration_date_frame.pack(fill=tk.X, padx=20, pady=(5, 0))
        
        # Default to 1 year from now
        default_expiry = datetime.now() + timedelta(days=365)
        
        expiration_date_entry = DateEntry(
            expiration_date_frame,
            width=25,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=default_expiry.year,
            month=default_expiry.month,
            day=default_expiry.day,
            date_pattern='yyyy-mm-dd',
            locale='en_US'
        )
        expiration_date_entry.pack(side="left", fill=tk.X, expand=True)
        
        # Quick options for expiration date
        expiry_btn_frame = tk.Frame(expiration_date_frame)
        expiry_btn_frame.pack(side="right", padx=(5, 0))
        
        def set_expiry(days):
            expiration_date_entry.set_date(datetime.now() + timedelta(days=days))
        
        tk.Button(
            expiry_btn_frame,
            text="1Y",
            command=lambda: set_expiry(365),
            bg="#2ecc71",
            fg="white",
            relief="flat",
            padx=8,
            font=("Arial", 8)
        ).pack(side="left", padx=(0, 2))
        
        tk.Button(
            expiry_btn_frame,
            text="2Y",
            command=lambda: set_expiry(730),
            bg="#f39c12",
            fg="white",
            relief="flat",
            padx=8,
            font=("Arial", 8)
        ).pack(side="left", padx=(0, 2))
        
        tk.Button(
            expiry_btn_frame,
            text="3Y",
            command=lambda: set_expiry(1095),
            bg="#9b59b6",
            fg="white",
            relief="flat",
            padx=8,
            font=("Arial", 8)
        ).pack(side="left")

        # Purchase Order number
        create_label(scrollable_frame, "Purchase Order Number")
        purchase_order_number_entry = tk.Entry(scrollable_frame)
        purchase_order_number_entry.pack(fill=tk.X, padx=20)

        # Notes
        create_label(scrollable_frame, "Notes")
        notes_entry = tk.Entry(scrollable_frame)
        notes_entry.pack(fill=tk.X, padx=20)

        # Populate fields if editing
        if license:
            software_name_entry.insert(0, license.softwareName)
            license_category_combo.set(license.categoryName if license.categoryName else "")
            seats_entry.insert(0, str(license.seats) if license.seats else "")
            product_key_entry.insert(0, license.productKey)
            licensed_to_entry.insert(0, license.licensedTo or "")
            licensed_to_email_entry.insert(0, license.licensedToEmail or "")
            purchase_order_number_entry.insert(0, license.orderNumber or "")
            purchase_cost_entry.insert(0, str(license.purchaseCost) if license.purchaseCost else "")
            manufacturer_combo.set(
                license.manufacturer_name if license.manufacturer_name else "")

            # Set dates if they exist
            if license.purchaseDate:
                try:
                    purchase_date_entry.set_date(datetime.strptime(license.purchaseDate, '%Y-%m-%d'))
                except:
                    pass
            
            if license.expirationDate:
                try:
                    expiration_date_entry.set_date(datetime.strptime(license.expirationDate, '%Y-%m-%d'))
                except:
                    pass
            
            notes_entry.insert(0, license.notes or "")

        def save():
            # Get values
            software_name = software_name_entry.get().strip()
            selected_category = license_category_combo.get()
            seats = seats_entry.get().strip()
            product_key = product_key_entry.get().strip()
            licensed_to = licensed_to_entry.get().strip()
            licensed_to_email = licensed_to_email_entry.get().strip()
            purchase_cost = purchase_cost_entry.get().strip()
            purchase_order_number = purchase_order_number_entry.get().strip()
            selected_manufacturer = manufacturer_combo.get()
            manufacturer_id = manufacturer_map[selected_manufacturer] if selected_manufacturer else None
            notes = notes_entry.get().strip()
            
            # Validate required fields
            if not software_name:
                # warning("Validation Error", "Please enter a software name")
                messagebox.showwarning("Warning", "Please enter a software name")
                software_name_entry.focus()
                return

            if not selected_category:
                # warning("Validation Error", "Please select a category")
                messagebox.showwarning("Warning", "Please enter a category")
                license_category_combo.focus()
                return

            # Validate seats (if provided)
            if seats:
                try:
                    seats_int = int(seats)
                    if seats_int < 0:
                        # warning("Validation Error", "Seats must be a positive number")
                        messagebox.showwarning("Error", "Seats must be a positive numbe")
                        seats_entry.focus()
                        return
                except ValueError:
                    # warning("Validation Error", "Seats must be a valid number")
                    messagebox.showwarning("Error", "Seats must be a valid number")
                    seats_entry.focus()
                    return

            # Validate purchase cost (if provided)
            if purchase_cost:
                try:
                    purchase_cost_float = float(purchase_cost)
                    if purchase_cost_float < 0:
                        # warning("Validation Error", "Purchase cost must be a positive number")
                        messagebox.showwarning("Warning", "Purchase cost must be a positive number")
                        purchase_cost_entry.focus()
                        return
                except ValueError:
                    # warning("Validation Error", "Purchase cost must be a valid number")
                    messagebox.showwarning("Warning", "Purchase cost must be a valid number")
                    purchase_cost_entry.focus()
                    return

            # Validate email (if provided)
            if licensed_to_email and '@' not in licensed_to_email:
                # warning("Validation Error", "Please enter a valid email address")
                messagebox.showwarning("Warning", "Please enter a valid email address")
                licensed_to_email_entry.focus()
                return

            # Get dates as strings
            try:
                purchase_date = purchase_date_entry.get_date().strftime('%Y-%m-%d')
            except:
                purchase_date = None
            
            try:
                expiration_date = expiration_date_entry.get_date().strftime('%Y-%m-%d')
            except:
                expiration_date = None

            # Validate expiration date is after purchase date
            if purchase_date and expiration_date:
                if datetime.strptime(expiration_date, '%Y-%m-%d') < datetime.strptime(purchase_date, '%Y-%m-%d'):
                    # warning("Validation Error", "Expiration date must be after purchase date")
                    messagebox.showwarning("Warning", "Expiration date must be after purchase date")
                    expiration_date_entry.focus()
                    return

            try:
                if license:
                    service.update(
                        license_id=license.id,
                        softwareName=software_name,
                        categoryName=selected_category,
                        seats=seats,
                        productKey=product_key,
                        licensedTo=licensed_to,
                        licensedToEmail=licensed_to_email,
                        orderNumber=purchase_order_number,
                        purchaseCost=purchase_cost,
                        purchaseDate=purchase_date,
                        expirationDate=expiration_date,
                        manufacturer_id=manufacturer_id,
                        notes=notes,
                    )
                    # success("Success!", f"License '{software_name}' updated successfully")
                else:
                    service.insert(
                        softwareName=software_name,
                        categoryName=selected_category,
                        seats=seats,
                        productKey=product_key,
                        licensedTo=licensed_to,
                        licensedToEmail=licensed_to_email,
                        orderNumber=purchase_order_number,
                        purchaseCost=purchase_cost,
                        purchaseDate=purchase_date,
                        expirationDate=expiration_date,
                        manufacturer_id=manufacturer_id,
                        notes=notes,
                    )
                    messagebox.showinfo(title, "License created successfully")
                    # success("Success!", f"License '{software_name}' created successfully")

                modal.destroy()
                self.load_licenses()
                
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
                # error("Validation Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))
                # error("Error", f"Failed to save license: {str(e)}")

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
        selected = self.tree.focus()
        if not selected:
            return

        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        if selected_index < len(self.licenses):
            license = self.licenses[selected_index]

            if values:
                self.open_form("Edit License", license)

    def delete_license(self):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        license = self.licenses[selected_index]

        print("license------------------------: ", license)

        if not values:
            messagebox.showwarning(
                "Warning", "Please select a license to delete")
            return

        # Show license name in confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete license '{license.softwareName}'?\n\nThis action cannot be undone.",
            icon="warning"
        )

        if not confirm:
            return

        try:
            service.delete(license.id)
            messagebox.showinfo("Success", "License deleted successfully!")
            self.load_licenses()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to delete license: {str(e)}")
