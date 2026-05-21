import tkinter as tk
from tkinter import ttk, messagebox
from services import accessory_service as service
from services import type_service as type_service
from models.accessory import Accessory
from typing import Optional


class AccessoriesView:
    def __init__(self, parent):
        self.accessories = []
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="🖱️ Accessories",
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

        # Add Accessory button with icon
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
            command=self.delete_accessory,
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
                "Accessory Name", 
                "Category Name",
                "Supplier Name",
                "Model No.", 
                "Min. QTY", 
                "Total", 
            ),
            show="headings",
            height=15
        )

        self.tree.heading("Accessory Name", text="Accessory Name")
        self.tree.heading("Category Name", text="Category Name")
        self.tree.heading("Supplier Name", text="Supplier Name")
        self.tree.heading("Model No.", text="Model No.")
        self.tree.heading("Min. QTY", text="Min. QTY")
        self.tree.heading("Total", text="Total")

        self.tree.column("Accessory Name", width=300, anchor="center")
        self.tree.column("Category Name", width=300, anchor="center")
        self.tree.column("Supplier Name", width=300, anchor="center")
        self.tree.column("Model No.", width=100, anchor="center")
        self.tree.column("Min. QTY", width=100, anchor="center")
        self.tree.column("Total", width=100, anchor="center")

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

        self.load_accessories()

    def load_accessories(self, keyword=""):
        # Clear existing items
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = service.get_all(keyword)

        for accessory in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    accessory.accessoryName,
                    accessory.categoryName,
                    accessory.supplierName,
                    accessory.modelNumber,
                    accessory.minQuantity,
                    accessory.qunatity,
                )
            )

        self.accessories = rows

        # Update status label
        count = len(rows)
        self.status_label.config(text=f"📊 Total accessories: {count}")

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_accessories(keyword)

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
        self.open_form("Add Accessory")

    def open_form(self, title, accessory: Optional[Accessory] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x400")

        # Center the modal
        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        tk.Label(modal, text="Accessory Name").pack()
        accessory_name_entry = tk.Entry(modal)
        accessory_name_entry.pack()

        tk.Label(modal, text="Category Name").pack()
        category_name_entry = tk.Entry(modal)
        category_name_entry.pack()

        tk.Label(modal, text="Supplier Name").pack()
        supplier_name_entry = tk.Entry(modal)
        supplier_name_entry.pack()

        tk.Label(modal, text="Model No.").pack()
        model_number_entry = tk.Entry(modal)
        model_number_entry.pack()

        tk.Label(modal, text="Min. Quantity").pack()
        min_qty_entry = tk.Entry(modal)
        min_qty_entry.pack()

        tk.Label(modal, text="Total").pack()
        total_entry = tk.Entry(modal)
        total_entry.pack()

        if accessory:
            accessory_name_entry.insert(0, accessory.accessoryName)
            category_name_entry.insert(0, accessory.categoryName)
            supplier_name_entry.insert(0, accessory.supplierName)
            model_number_entry.insert(0, accessory.modelNumber)
            min_qty_entry.insert(0, accessory.minQuantity)
            total_entry.insert(0, accessory.qunatity)

        def save():
            accessory_name = accessory_name_entry.get().strip()
            category_name = category_name_entry.get().strip()
            supplier_name = supplier_name_entry.get().strip()
            model_number = model_number_entry.get().strip()
            min_qty = min_qty_entry.get().strip()
            total = total_entry.get().strip()

            if not accessory_name:
                messagebox.showwarning(
                    "Warning", "Please enter a accessory name")
                accessory_name_entry.focus()
                return

            try:
                if accessory:
                    service.update(
                        accessory_id=accessory.id,
                        accessoryName=accessory_name,
                        categoryName=category_name,
                        supplierName=supplier_name,
                        modelNumber=model_number,
                        minQuantity=min_qty,
                        qunatity=total,
                    )
                    # messagebox.showinfo(
                    #     "Success", "Accessory updated successfully!")
                else:
                    service.insert(
                        accessoryName=accessory_name,
                        categoryName=category_name,
                        supplierName=supplier_name,
                        modelNumber=model_number,
                        minQuantity=min_qty,
                        qunatity=total,
                    )
                    # messagebox.showinfo(
                    #     "Success", "Accessory added successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save accessory: {str(e)}")

            modal.destroy()
            self.load_accessories()

        tk.Button(modal, text="Save", command=save).pack(pady=10)

    def on_double_click(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        if selected_index < len(self.accessories):
            accessory = self.accessories[selected_index]

            if values:
                self.open_form("Edit Accessory", accessory)

    def delete_accessory(self):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            messagebox.showwarning(
                "Warning", "Please select a accessory to delete")
            return

        # Show accessory name in confirmation
        accessory_name = values[1]
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete accessory '{accessory_name}'?\n\nThis action cannot be undone.",
            icon="warning"
        )

        if not confirm:
            return

        try:
            service.delete(values[0])
            messagebox.showinfo("Success", "Accessory deleted successfully!")
            self.load_accessories()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to delete accessory: {str(e)}")
