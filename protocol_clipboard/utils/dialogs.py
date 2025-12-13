"""Dialog utilities for input and confirmation."""
import re
from typing import Tuple
from PyQt5.QtWidgets import QInputDialog, QMessageBox


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate a model or protocol name.
    Returns (valid: bool, error_message: str).
    
    Rules:
    - Not empty
    - No leading/trailing whitespace
    - No path separators (/ or \\)
    - No special characters that could break filesystem
    """
    if not name:
        return (False, "Name cannot be empty")
    
    if name != name.strip():
        return (False, "Name cannot have leading or trailing spaces")
    
    # Check for invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, name):
        return (False, "Name contains invalid characters: < > : \" / \\ | ? *")
    
    # Check for reserved names on Windows
    reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                      'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                      'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    if name.upper() in reserved_names:
        return (False, f"'{name}' is a reserved system name")
    
    return (True, "")


def get_text_input(parent, title: str, label: str, default: str = "") -> tuple:
    """
    Show input dialog and return (text, ok).
    Returns (text_value, True) if confirmed, ("", False) if cancelled.
    Validates the input name.
    """
    while True:
        text, ok = QInputDialog.getText(parent, title, label, text=default)
        if not ok:
            return ("", False)
        
        text = text.strip()
        valid, error_msg = validate_name(text)
        
        if valid:
            return (text, True)
        else:
            QMessageBox.warning(parent, "Invalid Name", error_msg)
            default = text  # Keep the invalid input so user can fix it


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
