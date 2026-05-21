import tkinter as tk
from tkinter import messagebox


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("800x500")

        # Store current active button
        self.current_active_button = None

        # Main container
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.container, bg="#2c3e50", width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Content area
        self.content = tk.Frame(self.container, bg="#ecf0f1")
        self.content.pack(side="right", fill="both", expand=True)

        # ========== TOP SECTION: Logo / System Name ==========
        self.create_header()

        # ========== MIDDLE SECTION: Navigation Buttons ==========
        # Create a frame for navigation buttons (so they stay above logout)
        self.nav_frame = tk.Frame(self.sidebar, bg="#2c3e50")
        self.nav_frame.pack(side="top", fill="both", expand=True)

        # Define button styles
        self.button_normal_bg = "#34495e"
        self.button_active_bg = "#e74c3c"
        self.button_hover_bg = "#3d566e"

        # Create sidebar buttons with references
        self.dashboard_btn = self.create_sidebar_button(
            self.nav_frame, "📊 Dashboard", self.show_dashboard)
        self.assets_btn = self.create_sidebar_button(
            self.nav_frame, "💻 Assets", self.show_assets)
        self.licenses_btn = self.create_sidebar_button(
            self.nav_frame, "📜 Licenses", self.show_licenses)
        self.accessories_btn = self.create_sidebar_button(
            self.nav_frame, "🖱️ Accessories", self.show_accessories)
        self.employees_btn = self.create_sidebar_button(
            self.nav_frame, "👥 Employees", self.show_employees)
        self.manufacturers_btn = self.create_sidebar_button(
            self.nav_frame, "🏭 Manufacturers", self.show_manufacturers)
        self.categories_btn = self.create_sidebar_button(
            self.nav_frame, "📁 Categories", self.show_categories)
        self.models_btn = self.create_sidebar_button(
            self.nav_frame, "🔧 Asset Models", self.show_asset_models)

        # ========== BOTTOM SECTION: Logout Button ==========
        self.create_logout_button()

        # Set initial active button
        self.set_active_button(self.dashboard_btn)

        # Default view
        self.show_dashboard()

    def create_header(self):
        """Create logo/system name header at the top of sidebar"""
        header_frame = tk.Frame(self.sidebar, bg="#1a252f", height=100)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        # Option 1: Text-based logo
        logo_label = tk.Label(
            header_frame,
            text="🏢\nAsset\nManager",
            font=("Arial", 14, "bold"),
            fg="#ecf0f1",
            bg="#1a252f",
            justify="center"
        )
        logo_label.pack(expand=True, pady=10)

        # Optional: Add a separator line
        separator = tk.Frame(self.sidebar, bg="#1a252f", height=2)
        separator.pack(side="top", fill="x")

        tk.Label(
            separator,
            text="─" * 30,
            fg="#34495e",
            bg="#1a252f",
            font=("Arial", 8)
        ).pack()

    def create_logout_button(self):
        """Create logout button at the bottom of sidebar"""
        logout_frame = tk.Frame(self.sidebar, bg="#2c3e50")
        logout_frame.pack(side="bottom", fill="x", pady=10)

        logout_btn = tk.Button(
            logout_frame,
            text="🚪 Logout",
            fg="white",
            bg="#c0392b",  # Dark red for logout
            font=("Arial", 10, "bold"),
            command=self.logout,
            height=2,
            cursor="hand2",
            relief="flat"
        )
        logout_btn.pack(fill="x", padx=10, pady=5)

        # Add hover effect for logout button
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#e74c3c"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#c0392b"))

    def create_sidebar_button(self, parent, text, command):
        """Create a styled sidebar button with hover effects"""
        btn = tk.Button(
            parent,
            text=text,
            fg="white",
            bg=self.button_normal_bg,
            font=("Arial", 10),
            command=lambda: self.on_button_click(btn, command),
            height=2,
            cursor="hand2",
            relief="flat",
            anchor="w",  # Left align text
            padx=10
        )
        btn.pack(fill="x", pady=2, padx=10)

        # Add hover effects
        btn.bind("<Enter>", lambda e: self.on_hover(btn))
        btn.bind("<Leave>", lambda e: self.on_leave(btn))

        return btn

    def on_hover(self, button):
        """Handle mouse hover effect"""
        if button != self.current_active_button:
            button.config(bg=self.button_hover_bg)

    def on_leave(self, button):
        """Handle mouse leave effect"""
        if button != self.current_active_button:
            button.config(bg=self.button_normal_bg)

    def on_button_click(self, button, command):
        """Handle button click"""
        self.set_active_button(button)
        command()

    def set_active_button(self, active_button):
        """Set the active button with visual highlighting"""
        # Reset previous active button
        if self.current_active_button:
            self.current_active_button.config(
                bg=self.button_normal_bg,
                relief="flat",
                font=("Arial", 10)
            )

        # Set new active button
        self.current_active_button = active_button
        self.current_active_button.config(
            bg=self.button_active_bg,
            relief="sunken",
            font=("Arial", 10, "bold")
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        try:
            from views.dashboard import DashboardView
            DashboardView(self.content)
        except ImportError:
            self.show_placeholder("Dashboard View")

    def show_assets(self):
        self.clear_content()
        try:
            from views.assets import AssetsView
            AssetsView(self.content)
        except ImportError:
            self.show_placeholder("Assets View")

    def show_licenses(self):
        self.clear_content()
        try:
            from views.license import LicensesView
            LicensesView(self.content)
        except ImportError:
            self.show_placeholder("Licenses View")

    def show_accessories(self):
        self.clear_content()
        try:
            from views.accessories import AccessoriesView
            AccessoriesView(self.content)
        except ImportError:
            self.show_placeholder("Accessories View")

    def show_employees(self):
        self.clear_content()
        try:
            from views.employees import EmployeesView
            EmployeesView(self.content)
        except ImportError:
            self.show_placeholder("Employees View")

    def show_manufacturers(self):
        self.clear_content()
        try:
            from views.manufacturers import ManufacturersView
            ManufacturersView(self.content)
        except ImportError:
            self.show_placeholder("Manufacturers View")

    def show_categories(self):
        self.clear_content()
        try:
            from views.categories import CategoriesView
            CategoriesView(self.content)
        except ImportError:
            self.show_placeholder("Categories View")

    def show_asset_models(self):
        self.clear_content()
        try:
            from views.models import AssetModelsView
            AssetModelsView(self.content)
        except ImportError:
            self.show_placeholder("Asset Models View")

    def show_placeholder(self, view_name):
        """Show placeholder content when view modules are not available"""
        label = tk.Label(
            self.content,
            text=f"{view_name}\n\n(This is a placeholder)",
            font=("Arial", 24),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        label.pack(expand=True)

    def logout(self):
        """Handle logout functionality"""
        # Show confirmation dialog
        response = messagebox.askyesno(
            "Logout Confirmation",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if response:
            # Clear current content
            self.clear_content()

            # Show logout message
            label = tk.Label(
                self.content,
                text="Logged Out Successfully!\n\nClosing application...",
                font=("Arial", 16),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            label.pack(expand=True)

            # Option 1: Close the application
            self.root.after(1500, self.root.destroy)

            # Option 2: Return to login screen (uncomment if you have a login class)
            # self.root.after(1500, lambda: self.show_login_screen())

    def show_login_screen(self):
        """Method to show login screen (optional)"""
        for widget in self.root.winfo_children():
            widget.destroy()
        # from views.login import LoginView
        # LoginView(self.root)


# Alternative header styles you can use:

def create_header_with_image(self):
    """Alternative header with image logo (requires PIL)"""
    header_frame = tk.Frame(self.sidebar, bg="#1a252f", height=120)
    header_frame.pack(side="top", fill="x")
    header_frame.pack_propagate(False)

    try:
        from PIL import Image, ImageTk
        # Load and resize logo image
        img = Image.open("logo.png")  # Make sure you have a logo.png file
        img = img.resize((50, 50), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(img)

        logo_label = tk.Label(header_frame, image=logo, bg="#1a252f")
        logo_label.image = logo  # Keep a reference
        logo_label.pack(pady=10)
    except:
        # Fallback to text if image not available
        logo_label = tk.Label(
            header_frame,
            text="🏢 ASSET MANAGER",
            font=("Arial", 12, "bold"),
            fg="#ecf0f1",
            bg="#1a252f"
        )
        logo_label.pack(expand=True)

    # System name
    name_label = tk.Label(
        header_frame,
        text="Asset Management System",
        font=("Arial", 8),
        fg="#95a5a6",
        bg="#1a252f"
    )
    name_label.pack(pady=(0, 10))


def create_header_with_canvas(self):
    """Alternative header with custom canvas design"""
    header_frame = tk.Frame(self.sidebar, bg="#1a252f", height=100)
    header_frame.pack(side="top", fill="x")
    header_frame.pack_propagate(False)

    canvas = tk.Canvas(header_frame, bg="#1a252f",
                       height=80, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Draw a circle or shape for logo
    canvas.create_oval(75, 15, 125, 65, fill="#e74c3c", outline="")
    canvas.create_text(100, 40, text="AMS", font=(
        "Arial", 12, "bold"), fill="white")

    # System name below
    tk.Label(
        header_frame,
        text="Asset Manager",
        font=("Arial", 10, "bold"),
        fg="#ecf0f1",
        bg="#1a252f"
    ).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
