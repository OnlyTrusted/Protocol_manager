"""
Styling constants and stylesheets for the application.
Defines color palette and Qt stylesheets with dark theme.
"""

# Color constants
BLACK_BG = "#0b0b0d"
PANEL_BG = "#141418"
EDITOR_BG = "#1f1f24"
ACCENT = "#2d2d35"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#a0a0a0"
BORDER = "#2a2a30"


def get_main_window_stylesheet() -> str:
    """Return stylesheet for the main window."""
    return f"""
    QMainWindow {{
        background-color: {BLACK_BG};
    }}
    QMenuBar {{
        background-color: {PANEL_BG};
        color: {TEXT_PRIMARY};
        border-bottom: 1px solid {BORDER};
    }}
    QMenuBar::item:selected {{
        background-color: {ACCENT};
    }}
    QMenu {{
        background-color: {PANEL_BG};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
    }}
    QMenu::item:selected {{
        background-color: {ACCENT};
    }}
    QStatusBar {{
        background-color: {PANEL_BG};
        color: {TEXT_MUTED};
        border-top: 1px solid {BORDER};
    }}
    """


def get_list_widget_stylesheet() -> str:
    """Return stylesheet for list widgets (models and protocols panels)."""
    return f"""
    QListWidget {{
        background-color: {PANEL_BG};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 4px;
        outline: none;
    }}
    QListWidget::item {{
        padding: 8px;
        border-radius: 4px;
        margin: 2px 0;
    }}
    QListWidget::item:selected {{
        background-color: {ACCENT};
        color: {TEXT_PRIMARY};
    }}
    QListWidget::item:hover {{
        background-color: {ACCENT};
    }}
    """


def get_text_edit_stylesheet() -> str:
    """Return stylesheet for the text editor."""
    return f"""
    QTextEdit {{
        background-color: {EDITOR_BG};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 12px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 13px;
        selection-background-color: {ACCENT};
    }}
    """


def get_button_stylesheet() -> str:
    """Return stylesheet for buttons."""
    return f"""
    QPushButton {{
        background-color: {ACCENT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {BORDER};
    }}
    QPushButton:pressed {{
        background-color: {PANEL_BG};
    }}
    """


def get_label_stylesheet() -> str:
    """Return stylesheet for labels."""
    return f"""
    QLabel {{
        color: {TEXT_MUTED};
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    """


def get_tree_widget_stylesheet() -> str:
    """Return stylesheet for tree widget in hierarchy dialog."""
    return f"""
    QTreeWidget {{
        background-color: {PANEL_BG};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 6px;
        outline: none;
    }}
    QTreeWidget::item {{
        padding: 6px;
        border-radius: 3px;
    }}
    QTreeWidget::item:selected {{
        background-color: {ACCENT};
        color: {TEXT_PRIMARY};
    }}
    QTreeWidget::item:hover {{
        background-color: {ACCENT};
    }}
    QHeaderView::section {{
        background-color: {PANEL_BG};
        color: {TEXT_MUTED};
        border: none;
        padding: 6px;
        font-weight: bold;
    }}
    """


def get_dialog_stylesheet() -> str:
    """Return stylesheet for dialogs."""
    return f"""
    QDialog {{
        background-color: {BLACK_BG};
    }}
    QInputDialog {{
        background-color: {BLACK_BG};
    }}
    QMessageBox {{
        background-color: {BLACK_BG};
    }}
    """
