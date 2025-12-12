"""Dialog utilities for input and confirmation."""
from PyQt5.QtWidgets import QInputDialog, QMessageBox


def get_text_input(parent, title: str, label: str, default: str = "") -> tuple:
    """
    Show input dialog and return (text, ok).
    Returns (text_value, True) if confirmed, ("", False) if cancelled.
    """
    text, ok = QInputDialog.getText(parent, title, label, text=default)
    return (text.strip(), ok) if ok else ("", False)


def confirm_action(parent, title: str, message: str) -> bool:
    """
    Show confirmation dialog for destructive actions.
    Returns True if confirmed, False otherwise.
    """
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    return reply == QMessageBox.Yes


def show_error(parent, title: str, message: str):
    """
    Show error message dialog.
    """
    QMessageBox.critical(parent, title, message, QMessageBox.Ok)
