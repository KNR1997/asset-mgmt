import tkinter as tk
from tkinter import ttk, messagebox
from services import category_service as service
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
            columns=("ID", "Name"),
            show="headings",
            height=15
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Category Name")

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=300, anchor="center")

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
                    category.id,
                    category.name,
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
        modal.geometry("400x250")
        modal.resizable(False, False)
        modal.configure(bg="#f5f6fa")

        # Center the modal
        modal.transient(self.frame)
        modal.update_idletasks()
        modal.grab_set()

        # Center on screen
        # x = modal.winfo_screenwidth() // 2 - 200
        # y = modal.winfo_screenheight() // 2 - 125
        # modal.geometry(f"+{x}+{y}")

        # Icon
        tk.Label(
            modal,
            text="📁",
            font=("Segoe UI", 40),
            bg="#f5f6fa",
            fg="#3498db"
        ).pack(pady=(20, 10))

        # Title
        tk.Label(
            modal,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2c3e50"
        ).pack(pady=(0, 20))

        # Form frame
        form_frame = tk.Frame(modal, bg="#f5f6fa")
        form_frame.pack(pady=10)

        tk.Label(
            form_frame,
            text="Category Name:",
            font=("Segoe UI", 10),
            bg="#f5f6fa",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 5))

        name_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            width=30,
            relief="solid",
            borderwidth=1
        )
        name_entry.pack(pady=(0, 15), ipady=5)

        if category:
            name_entry.insert(0, category.name)
            name_entry.focus()
        else:
            name_entry.focus()

        # Button frame
        btn_frame = tk.Frame(modal, bg="#f5f6fa")
        btn_frame.pack(pady=10)

        def save():
            name = name_entry.get().strip()

            if not name:
                messagebox.showwarning(
                    "Warning", "Please enter a category name")
                name_entry.focus()
                return

            try:
                if category:
                    service.update(
                        category_id=category.id,
                        name=name,
                    )
                    messagebox.showinfo(
                        "Success", "Category updated successfully!")
                else:
                    service.insert(
                        name=name,
                        description='',
                    )
                    messagebox.showinfo(
                        "Success", "Category added successfully!")

                modal.destroy()
                self.load_categories()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save category: {str(e)}")

        # Save button
        save_btn = tk.Button(
            btn_frame,
            text="💾 Save",
            command=save,
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=5)

        # Hover effect for Save button
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg="#2980b9"))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg="#3498db"))

        # Cancel button
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=modal.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 10),
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        cancel_btn.pack(side="left", padx=5)

        # Hover effect for Cancel button
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg="#7f8c8d"))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg="#95a5a6"))

        # Bind Enter key to save
        modal.bind('<Return>', lambda event: save())

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
        values = self.tree.item(selected, "values")

        if not values:
            messagebox.showwarning(
                "Warning", "Please select a category to delete")
            return

        # Show category name in confirmation
        category_name = values[1]
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete category '{category_name}'?\n\nThis action cannot be undone.",
            icon="warning"
        )

        if not confirm:
            return

        try:
            service.delete(values[0])
            messagebox.showinfo("Success", "Category deleted successfully!")
            self.load_categories()
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to delete category: {str(e)}")


# if __name__ == "__main__":
#     # For testing
#     root = tk.Tk()
#     root.geometry("800x600")
#     app = CategoriesView(root)
#     root.mainloop()
