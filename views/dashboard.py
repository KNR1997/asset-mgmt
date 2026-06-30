import tkinter as tk
from services import asset_service as asset_service
from services import employee_service as employee_service
from services import license_service as license_service
from services import accessory_service as accessory_service
from services import manufacturer_service as manufacturer_service
from services import category_service as category_service
from services import model_service as model_service


class DashboardView:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # Header with icon
        header_frame = tk.Frame(self.frame, bg="#f5f6fa")
        header_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            header_frame,
            text="📊 Dashboard",
            font=("Segoe UI", 20, "bold"),
            fg="#2c3e50",
            bg="#f5f6fa"
        ).pack(side="left", padx=20)
        
        # Separator line
        separator = tk.Frame(self.frame, bg="#dcdde1", height=2)
        separator.pack(fill="x", padx=20, pady=(0, 20))
        
        # Demo mode banner
        # demo_banner = tk.Frame(self.frame, bg="#f39c12", height=40)
        # demo_banner.pack(fill="x", padx=20, pady=(0, 20))
        
        # tk.Label(
        #     demo_banner,
        #     text="⚠️ DEMO MODE: Some features are disabled for this installation.",
        #     font=("Segoe UI", 10),
        #     fg="white",
        #     bg="#f39c12"
        # ).pack(expand=True, pady=10)
        
        # Create main container for cards
        cards_container = tk.Frame(self.frame, bg="#f5f6fa")
        cards_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        asset_count = asset_service.count()
        employee_count = employee_service.count()
        employee_count = employee_service.count()
        license_count = license_service.count()
        license_count = license_service.count()
        accessory_count = accessory_service.count()
        manufacturer_count = manufacturer_service.count()
        category_count = category_service.count()
        model_count = model_service.count()

        # Card data
        cards_data = [
            {"title": "Assets", "count": asset_count, "color": "#3498db", "icon": "💻"},
            {"title": "Categories", "count": category_count, "color": "#3498db", "icon": "📦"},
            {"title": "Manufacturers", "count": manufacturer_count, "color": "#3498db", "icon": "🚛"},
            {"title": "Employees", "count": employee_count, "color": "#3498db", "icon": "⛑️"},
            {"title": "Models", "count": model_count, "color": "#3498db", "icon": "⚒️"},
            # {"title": "Licenses", "count": license_count, "color": "#2ecc71", "icon": "📜"},
            # {"title": "Accessories", "count": accessory_count, "color": "#e67e22", "icon": "🖱️"},
            # {"title": "Consumables", "count": "3", "color": "#9b59b6", "icon": "📦"},
            # {"title": "Components", "count": "4", "color": "#1abc9c", "icon": "🔧"},
            {"title": "People", "count": employee_count, "color": "#e74c3c", "icon": "👥"}
        ]

        # Create cards in grid
        for i, card in enumerate(cards_data):
            row = i // 2
            col = i % 2
            
            card_frame = self.create_card(
                cards_container,
                card["title"],
                card["count"],
                card["color"],
                card["icon"]
            )
            card_frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            
            # Configure grid weights
            cards_container.grid_columnconfigure(0, weight=1)
            cards_container.grid_columnconfigure(1, weight=1)
            cards_container.grid_rowconfigure(row, weight=1)
    
    def create_card(self, parent, title, count, color, icon):
        """Create a single dashboard card"""
        card = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1,
            highlightbackground="#dcdde1",
            highlightthickness=1
        )
        
        # Top color bar
        color_bar = tk.Frame(card, bg=color, height=5)
        color_bar.pack(fill="x")
        
        # Card content
        content = tk.Frame(card, bg="white", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        # Icon
        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 48),
            bg="white",
            fg=color
        )
        icon_label.pack(side="left", padx=(0, 20))
        
        # Text content
        text_frame = tk.Frame(content, bg="white")
        text_frame.pack(side="left", fill="both", expand=True)
        
        count_label = tk.Label(
            text_frame,
            text=count,
            font=("Segoe UI", 32, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor="w"
        )
        count_label.pack(anchor="w")
        
        title_label = tk.Label(
            text_frame,
            text=title,
            font=("Segoe UI", 12),
            bg="white",
            fg="#7f8c8d",
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(5, 10))
        
        # View all button
        view_btn = tk.Button(
            text_frame,
            text="view all →",
            font=("Segoe UI", 9),
            bg="white",
            fg=color,
            relief="flat",
            cursor="hand2",
            anchor="w",
            command=lambda t=title: self.view_all(t)
        )
        view_btn.pack(anchor="w")
        
        # Hover effect
        def on_enter(e):
            view_btn.config(fg=self.darken_color(color))
        
        def on_leave(e):
            view_btn.config(fg=color)
        
        view_btn.bind("<Enter>", on_enter)
        view_btn.bind("<Leave>", on_leave)
        
        return card
    
    def view_all(self, category):
        from tkinter import messagebox
        messagebox.showinfo(
            "Coming Soon",
            f"The {category} management feature will be available in the full version."
        )
    
    def darken_color(self, hex_color, factor=0.7):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f'#{r:02x}{g:02x}{b:02x}'
