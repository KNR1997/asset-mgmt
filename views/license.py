import tkinter as tk
from tkinter import ttk, messagebox
from services import license_service as service
from services import type_service as type_service
from models.license import License
from typing import Optional


class LicensesView:
    def __init__(self, parent):
        self.categories = []
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
                # "ID", 
                "Software Name", 
                "Category Name",
                "Seats"
            ),
            show="headings",
            height=15
        )

        # self.tree.heading("ID", text="ID")
        self.tree.heading("Software Name", text="Software Name")
        self.tree.heading("Category Name", text="Type")
        self.tree.heading("Seats", text="Seats")

        # self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Software Name", width=300, anchor="center")
        self.tree.column("Category Name", width=300, anchor="center")
        self.tree.column("Seats", width=300, anchor="center")

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
                    license.categoryName,
                    license.seats,
                )
            )

        self.categories = rows

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
        modal.geometry("400x300")
        # modal.resizable(False, False)
        # modal.configure(bg="#f5f6fa")

        # Center the modal
        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        types = type_service.get_all()
        type_map = {type.name: type.id for type in types}

        tk.Label(modal, text="Software Name").pack()
        software_name_entry = tk.Entry(modal)
        software_name_entry.pack()

        tk.Label(modal, text="Category Name").pack()
        category_name_entry = tk.Entry(modal)
        category_name_entry.pack()

        tk.Label(modal, text="Seats").pack()
        seats_entry = tk.Entry(modal)
        seats_entry.pack()

        if license:
            software_name_entry.insert(0, license.softwareName)
            category_name_entry.insert(0, license.categoryName)
            seats_entry.insert(0, license.seats)

        def save():
            software_name = software_name_entry.get().strip()
            category_name = category_name_entry.get().strip()
            seats = seats_entry.get().strip()

            if not software_name:
                messagebox.showwarning(
                    "Warning", "Please enter a software name")
                software_name_entry.focus()
                return

            try:
                if license:
                    service.update(
                        license_id=license.id,
                        softwareName=software_name,
                        categoryName=category_name,
                        seats=seats,
                    )
                    messagebox.showinfo(
                        "Success", "License updated successfully!")
                else:
                    service.insert(
                        softwareName=software_name,
                        categoryName=category_name,
                        seats=seats,
                    )
                    messagebox.showinfo(
                        "Success", "License added successfully!")

                modal.destroy()
                self.load_licenses()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save license: {str(e)}")

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        if selected_index < len(self.categories):
            license = self.categories[selected_index]

            if values:
                self.open_form("Edit License", license)

    def delete_license(self):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            messagebox.showwarning(
                "Warning", "Please select a license to delete")
            return

        # Show license name in confirmation
        license_name = values[1]
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete license '{license_name}'?\n\nThis action cannot be undone.",
            icon="warning"
        )

        if not confirm:
            return

        try:
            service.delete(values[0])
            messagebox.showinfo("Success", "License deleted successfully!")
            self.load_licenses()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to delete license: {str(e)}")
