"""Clipboard utility for copying text to system clipboard."""
from PyQt5.QtWidgets import QApplication


def copy(text: str):
    """Copy text to system clipboard."""
    clipboard = QApplication.clipboard()
    clipboard.setText(text)
