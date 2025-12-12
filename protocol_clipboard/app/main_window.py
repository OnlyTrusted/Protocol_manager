"""
Main window - application entry point with layout and menu.
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                             QAction, QStatusBar)
from PyQt5.QtCore import Qt

from .styles import get_main_window_stylesheet
from .signals import signals
from .models_panel import ModelsPanel
from .protocols_panel import ProtocolsPanel
from .editor_panel import EditorPanel
from .hierarchy_dialog import HierarchyDialog


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protocol Clipboard Manager")
        self.resize(1200, 700)
        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the main UI layout."""
        # Apply stylesheet
        self.setStyleSheet(get_main_window_stylesheet())
        
        # Central widget with horizontal layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create panels
        self.models_panel = ModelsPanel()
        self.protocols_panel = ProtocolsPanel()
        self.editor_panel = EditorPanel()
        
        # Add panels to layout with stretch factors
        layout.addWidget(self.models_panel, 1)
        layout.addWidget(self.protocols_panel, 1)
        layout.addWidget(self.editor_panel, 3)
    
    def _setup_menu(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        # Placeholder for future edit actions
        
        # Manage Hierarchy menu
        manage_menu = menubar.addMenu("Manage Hierarchy")
        
        hierarchy_action = QAction("Reorder Models/Protocols", self)
        hierarchy_action.setShortcut("Ctrl+H")
        hierarchy_action.triggered.connect(self._show_hierarchy_dialog)
        manage_menu.addAction(hierarchy_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Placeholder for future view actions
    
    def _setup_statusbar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _connect_signals(self):
        """Connect to application signals."""
        signals.protocol_selected.connect(self._on_protocol_selected)
        signals.hierarchy_changed.connect(self._on_hierarchy_changed)
    
    def _on_protocol_selected(self, model_name: str, protocol_name: str):
        """Update status bar when protocol is selected."""
        self.status_bar.showMessage(f"Copied '{protocol_name}' to clipboard")
    
    def _on_hierarchy_changed(self):
        """Refresh panels when hierarchy changes."""
        self.models_panel.refresh()
        self.protocols_panel.refresh()
    
    def _show_hierarchy_dialog(self):
        """Show the hierarchy management dialog."""
        dialog = HierarchyDialog(self)
        dialog.exec_()
