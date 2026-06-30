import tkinter as tk
from tkinter import ttk, messagebox
from services import category_service as service
from services import type_service as type_service
from models.category import Category
from typing import Optional


class CategoriesView:
    def __init__(self, parent):
        self.categories = []
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="📁 Categories",
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
            command=self.delete_category,
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
                "Name",
                "Type"
            ),
            show="headings",
            height=15
        )

        # self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Category Name")
        self.tree.heading("Type", text="Type")

        # self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=300, anchor="center")
        self.tree.column("Type", width=300, anchor="center")

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

        self.load_categories()

    def load_categories(self, keyword=""):
        # Clear existing items
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = service.get_all(keyword)

        for category in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    # category.id,
                    category.name,
                    category.type_name,
                )
            )

        self.categories = rows

        # Update status label
        count = len(rows)
        self.status_label.config(text=f"📊 Total categories: {count}")

    def on_search(self, *args):
        keyword = self.search_var.get()
        self.load_categories(keyword)

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
        self.open_form("Add Category")

    def open_form(self, title, category: Optional[Category] = None):
        modal = tk.Toplevel()
        modal.title(title)
        modal.geometry("350x200")

        # Center the modal
        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        types = type_service.get_all()
        type_map = {type.name: type.id for type in types}

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

        create_label(modal, "Category Name", required=True).pack()
        name_entry = tk.Entry(modal)
        name_entry.pack(fill=tk.X, padx=20)

        create_label(modal, "Type", required=True).pack()
        type_combo = ttk.Combobox(
            modal,
            values=list(type_map.keys()),
            state="readonly"
        )
        type_combo.pack(fill=tk.X, padx=20)

        if category:
            name_entry.insert(0, category.name)
            type_combo.set(category.type_name if category.type_name else "")
            name_entry.focus()

        def save():
            name = name_entry.get().strip()
            selected_type = type_combo.get()

            if not name:
                messagebox.showwarning(
                    "Warning", "Please enter a category name")
                name_entry.focus()
                return

            if not selected_type:
                messagebox.showwarning("Warning", "Please select a type")
                return

            type_id = type_map[selected_type]

            try:
                if category:
                    service.update(
                        category_id=category.id,
                        name=name,
                        type_id=type_id,
                    )
                    messagebox.showinfo(title, "Category updated successfully")
                else:
                    service.insert(
                        name=name,
                        type_id=type_id,
                        description='',
                    )
                    messagebox.showinfo(title, "Category created successfully")
                modal.destroy()
                self.load_categories()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save category: {str(e)}")

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

        if selected_index < len(self.categories):
            category = self.categories[selected_index]

            if values:
                self.open_form("Edit Category", category)

    def delete_category(self):
        selected = self.tree.focus()
        selected_index = self.tree.index(selected)
        values = self.tree.item(selected, "values")

        category = self.categories[selected_index]

        if not values:
            messagebox.showwarning("Warning", "Select a row")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this category?")
        if not confirm:
            return

        service.delete(category.id)
        self.load_categories()
