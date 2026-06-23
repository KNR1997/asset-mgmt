# utils/toast/manager.py
from ttkbootstrap.toast import ToastNotification
from typing import Optional
from .types import ToastType


class ToastManager:
    """Toast notification manager with queue support"""

    _instance = None
    _queue = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def show(
        title: str,
        message: str,
        toast_type: ToastType = ToastType.INFO,
        duration: int = 3000,
        alert: bool = False
    ):
        try:
            toast = ToastNotification(
                title=title,
                message=message,
                duration=duration,
                bootstyle="success",
                alert=alert,
                position=(10, 10, "ne") # Position: offset X, offset Y, North-East corner
            )
            toast.show_toast()
        except Exception as e:
            # Log error and use fallback
            print(f"Toast error: {e}")
            from tkinter import messagebox
            messagebox.showinfo(title, message)

# Convenience shortcuts


def success(title: str, message: str, duration: int = 3000):
    ToastManager.show(title, message, ToastType.SUCCESS, duration)


def error(title: str, message: str, duration: int = 4000):
    ToastManager.show(title, message, ToastType.ERROR, duration)


def warning(title: str, message: str, duration: int = 3500):
    ToastManager.show(title, message, ToastType.WARNING, duration)


def info(title: str, message: str, duration: int = 3000):
    ToastManager.show(title, message, ToastType.INFO, duration)
