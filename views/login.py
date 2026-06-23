import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Set background color
        self.root.configure(bg="#f0f2f5")

        # Center the window on screen
        self.center_window()

        # Create main container
        self.main_container = tk.Frame(root, bg="#f0f2f5")
        self.main_container.pack(fill="both", expand=True)

        # Create left panel (branding/illustration)
        self.create_left_panel()

        # Create right panel (login form)
        self.create_right_panel()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_left_panel(self):
        """Create the left panel with branding and illustration"""
        left_panel = tk.Frame(
            self.main_container,
            bg="#2c3e50",
            width=400,
            height=600
        )
        left_panel.pack(side="left", fill="both", expand=True)
        left_panel.pack_propagate(False)

        # Logo/Icon
        logo_frame = tk.Frame(left_panel, bg="#2c3e50")
        logo_frame.pack(pady=(80, 20))

        # You can replace this with an image if you have one
        logo_label = tk.Label(
            logo_frame,
            text="🏢",
            font=("Segoe UI", 80),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        logo_label.pack()

        # System Name
        system_name = tk.Label(
            left_panel,
            text="Asset Management\nSystem",
            font=("Segoe UI", 28, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            justify="center"
        )
        system_name.pack(pady=(10, 20))

        # Tagline
        tagline = tk.Label(
            left_panel,
            text="Efficiently manage your\nassets, employees, and more",
            font=("Segoe UI", 12),
            bg="#2c3e50",
            fg="#95a5a6",
            justify="center"
        )
        tagline.pack()

        # Decorative elements
        canvas = tk.Canvas(left_panel, bg="#2c3e50",
                           height=2, highlightthickness=0)
        canvas.pack(fill="x", pady=40, padx=50)
        canvas.create_line(0, 1, 300, 1, fill="#34495e", width=2)

        # Features list
        features = [
            "✓ Asset Tracking",
            "✓ Employee Management",
            "✓ Real-time Updates",
            "✓ Analytics Dashboard"
        ]

        for feature in features:
            tk.Label(
                left_panel,
                text=feature,
                font=("Segoe UI", 10),
                bg="#2c3e50",
                fg="#bdc3c7",
                anchor="w"
            ).pack(pady=5, padx=50, anchor="w")

    def create_right_panel(self):
        """Create the right panel with login form"""
        right_panel = tk.Frame(
            self.main_container,
            bg="white",
            width=500,
            height=600
        )
        right_panel.pack(side="right", fill="both", expand=True)
        right_panel.pack_propagate(False)

        # Title
        title = tk.Label(
            right_panel,
            text="Welcome Back!",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        title.pack(pady=(80, 10))

        subtitle = tk.Label(
            right_panel,
            text="Please login to your account",
            font=("Segoe UI", 11),
            bg="white",
            fg="#7f8c8d"
        )
        subtitle.pack(pady=(0, 40))

        # Login Form Frame
        form_frame = tk.Frame(right_panel, bg="white")
        form_frame.pack(pady=20, padx=60, fill="both")

        # Username field
        username_label = tk.Label(
            form_frame,
            text="Username",
            font=("Segoe UI", 11),
            bg="white",
            fg="#2c3e50",
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))

        self.username = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            highlightcolor="#3498db",
            highlightthickness=1
        )
        self.username.pack(fill="x", pady=(0, 20), ipady=10)
        self.username.bind("<FocusIn>", lambda e: self.on_entry_focus(
            self.username, "#3498db"))
        self.username.bind("<FocusOut>", lambda e: self.on_entry_focus_out(
            self.username, "#f8f9fa"))

        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password",
            font=("Segoe UI", 11),
            bg="white",
            fg="#2c3e50",
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))

        self.password = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bg="#f8f9fa",
            fg="#2c3e50",
            show="•",
            relief="solid",
            borderwidth=1
        )
        self.password.pack(fill="x", pady=(0, 10), ipady=10)
        self.password.bind("<FocusIn>", lambda e: self.on_entry_focus(
            self.password, "#3498db"))
        self.password.bind("<FocusOut>", lambda e: self.on_entry_focus_out(
            self.password, "#f8f9fa"))

        # Show/Hide Password Toggle
        self.show_password = tk.BooleanVar(value=False)
        show_pwd_btn = tk.Checkbutton(
            form_frame,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password,
            bg="white",
            fg="#7f8c8d",
            font=("Segoe UI", 9),
            selectcolor="white",
            cursor="hand2"
        )
        show_pwd_btn.pack(anchor="e", pady=(0, 20))

        # Login Button
        login_btn = tk.Button(
            form_frame,
            text="LOGIN",
            command=self.check_login,
            font=("Segoe UI", 12, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            cursor="hand2",
            height=2
        )
        login_btn.pack(fill="x", pady=(10, 20))

        # Hover effect for login button
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#2980b9"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#3498db"))

        # Forgot Password Link
        forgot_password = tk.Label(
            form_frame,
            text="Forgot Password?",
            font=("Segoe UI", 9),
            bg="white",
            fg="#3498db",
            cursor="hand2"
        )
        forgot_password.pack()
        forgot_password.bind("<Button-1>", lambda e: self.forgot_password())

        # Demo credentials hint
        demo_hint = tk.Label(
            right_panel,
            text="Demo Credentials: admin / admin123",
            font=("Segoe UI", 8),
            bg="white",
            fg="#95a5a6"
        )
        demo_hint.pack(side="bottom", pady=20)

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.check_login())

    def on_entry_focus(self, entry, color):
        """Highlight entry border on focus"""
        entry.config(highlightcolor=color, highlightthickness=2)

    def on_entry_focus_out(self, entry, color):
        """Remove highlight on focus out"""
        entry.config(highlightthickness=1)

    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.password.config(show="")
        else:
            self.password.config(show="•")

    def forgot_password(self):
        """Handle forgot password"""
        messagebox.showinfo(
            "Reset Password",
            "Please contact your system administrator to reset your password."
        )

    def check_login(self):
        """Check login credentials"""
        username = self.username.get().strip()
        password = self.password.get().strip()

        # Validation
        if not username or not password:
            messagebox.showerror(
                "Error", "Please enter both username and password")
            return

        try:
            conn = sqlite3.connect("assets.db")
            cur = conn.cursor()

            # Create admin table if it doesn't exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            # Insert demo admin if table is empty
            cur.execute("SELECT COUNT(*) FROM admin")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                            ("admin", "admin123"))
                conn.commit()

            # Check credentials
            cur.execute("SELECT * FROM admin WHERE username=? AND password=?",
                        (username, password))

            user = cur.fetchone()
            conn.close()

            # Todo -> fix this
            # self.show_loading_animation()
            # self.root.after(1000, lambda: self.login_success())

            if user:
                # Show loading animation effect
                self.show_loading_animation()
                self.root.after(1000, lambda: self.login_success())
            else:
                messagebox.showerror("Error", "Invalid username or password")
                self.password.delete(0, tk.END)
                self.password.focus()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Database error: {str(e)}")

    def show_loading_animation(self):
        """Show a loading message before redirecting"""
        loading = tk.Toplevel(self.root)
        loading.title("Processing")
        loading.geometry("300x150")
        loading.resizable(False, False)

        # Center the loading window
        loading.transient(self.root)
        loading.grab_set()

        # Center relative to parent
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        loading.geometry(f"+{x}+{y}")

        tk.Label(
            loading,
            text="Logging in...",
            font=("Segoe UI", 14, "bold"),
            fg="#2c3e50"
        ).pack(expand=True, pady=20)

        # Progress bar simulation
        progress = ttk.Progressbar(
            loading, mode='indeterminate', length=200)
        progress.pack(pady=10)
        progress.start(10)

        self.loading_window = loading

    def login_success(self):
        """Handle successful login"""
        if hasattr(self, 'loading_window') and self.loading_window:
            self.loading_window.destroy()

        messagebox.showinfo(
            "Success", "Login successful! Welcome to the dashboard.")
        self.root.destroy()

        # Open dashboard
        from dashboard import Dashboard
        dashboard_root = tk.Tk()
        dashboard_root.title("Dashboard")
        Dashboard(dashboard_root)
        dashboard_root.mainloop()


# Alternative: If you want to add a modern splash screen and animations
class ModernLogin(Login):
    """Enhanced version with additional animations and styling"""

    def create_right_panel(self):
        """Enhanced right panel with gradient-like effect"""
        super().create_right_panel()

        # Add a subtle shadow effect to the panel
        self.main_container.configure(bg="#e8eef2")

        # Animate the form appearance
        self.animate_form()

    def animate_form(self):
        """Simple fade-in animation for the form"""
        alpha = 0
        for widget in self.right_panel.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    try:
                        child.configure(fg="#2c3e50")
                    except:
                        pass


if __name__ == "__main__":
    root = tk.Tk()

    # Optional: Set application icon
    # root.iconbitmap("icon.ico")

    app = Login(root)
    root.mainloop()
