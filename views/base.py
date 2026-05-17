import tkinter as tk


class BaseView:
    """Base class for consistent styling across all views"""

    COLORS = {
        'bg': '#f5f6fa',
        'header': '#2c3e50',
        'primary': '#3498db',
        'danger': '#e74c3c',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'text': '#2c3e50',
        'text_light': '#7f8c8d',
        'border': '#dcdde1'
    }

    FONTS = {
        'header': ('Segoe UI', 20, 'bold'),
        'subheader': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 10),
        'button': ('Segoe UI', 10, 'bold'),
        'small': ('Segoe UI', 9)
    }

    @staticmethod
    def create_button(parent, text, command, color='primary', icon=''):
        """Create a styled button"""
        color_map = {
            'primary': '#3498db',
            'danger': '#e74c3c',
            'success': '#2ecc71',
            'warning': '#f39c12'
        }

        btn_text = f"{icon} {text}" if icon else text

        button = tk.Button(
            parent,
            text=btn_text,
            command=command,
            bg=color_map.get(color, '#3498db'),
            fg='white',
            font=BaseView.FONTS['button'],
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )

        # Add hover effect
        def on_enter(e):
            button.config(bg=self.darken_color(
                color_map.get(color, '#3498db')))

        def on_leave(e):
            button.config(bg=color_map.get(color, '#3498db'))

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    @staticmethod
    def darken_color(hex_color, factor=0.8):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f'#{r:02x}{g:02x}{b:02x}'
