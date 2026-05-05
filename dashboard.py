import tkinter as tk

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("800x500")

        # Main container
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.container, bg="#2c3e50", width=210)
        self.sidebar.pack(side="left", fill="y")

        # Content area
        self.content = tk.Frame(self.container, bg="#ecf0f1")
        self.content.pack(side="right", fill="both", expand=True)

        # Sidebar buttons
        tk.Button(self.sidebar, text="Assets", fg="white", bg="#34495e",
                  command=self.show_assets, height=2).pack(fill="x", pady=5)

        tk.Button(self.sidebar, text="Employees", fg="white", bg="#34495e",
                  command=self.show_employees, height=2).pack(fill="x", pady=5)

        # Default view
        self.show_assets()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_assets(self):
        self.clear_content()
        from assets import AssetsView
        AssetsView(self.content)

    def show_employees(self):
        self.clear_content()
        from employees import EmployeesView
        EmployeesView(self.content)