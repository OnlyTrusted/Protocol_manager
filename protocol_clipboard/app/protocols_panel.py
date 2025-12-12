"""
Protocols panel - displays and manages protocols for the selected model.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt

from .styles import get_list_widget_stylesheet, get_button_stylesheet, get_label_stylesheet
from .signals import signals
from ..utils.storage import storage
from ..utils.dialogs import get_text_input, confirm_action


class ProtocolsPanel(QWidget):
    """Panel for displaying and managing protocols."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_model = None
        self.current_protocol = None
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Label
        label = QLabel("PROTOCOLS")
        label.setStyleSheet(get_label_stylesheet())
        layout.addWidget(label)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(get_list_widget_stylesheet())
        self.list_widget.itemClicked.connect(self._on_protocol_selected)
        self.list_widget.itemDoubleClicked.connect(self._on_rename_protocol)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.list_widget)
        
        # Add button
        add_button = QPushButton("+")
        add_button.setStyleSheet(get_button_stylesheet())
        add_button.clicked.connect(self._on_add_protocol)
        add_button.setEnabled(False)  # Disabled until model is selected
        self.add_button = add_button
        layout.addWidget(add_button)
    
    def _connect_signals(self):
        """Connect to application signals."""
        signals.model_selected.connect(self._on_model_changed)
    
    def _on_model_changed(self, model_name: str):
        """Handle model selection change."""
        self.current_model = model_name
        self.current_protocol = None
        self._load_protocols()
        self.add_button.setEnabled(True)
    
    def _load_protocols(self):
        """Load protocols for the current model."""
        self.list_widget.clear()
        
        if not self.current_model:
            return
        
        protocols = storage.load_protocol_order(self.current_model)
        self.list_widget.addItems(protocols)
    
    def _on_protocol_selected(self, item):
        """Handle protocol selection."""
        if item and self.current_model:
            protocol_name = item.text()
            self.current_protocol = protocol_name
            signals.protocol_selected.emit(self.current_model, protocol_name)
    
    def _on_add_protocol(self):
        """Handle adding a new protocol."""
        if not self.current_model:
            return
        
        name, ok = get_text_input(self, "New Protocol", "Enter protocol name:")
        if ok and name:
            if storage.add_protocol(self.current_model, name):
                self.list_widget.addItem(name)
                # Select the newly added protocol
                self.list_widget.setCurrentRow(self.list_widget.count() - 1)
                self._on_protocol_selected(self.list_widget.item(self.list_widget.count() - 1))
            else:
                # Protocol already exists
                pass
    
    def _on_rename_protocol(self, item):
        """Handle renaming a protocol."""
        if not item or not self.current_model:
            return
        
        old_name = item.text()
        new_name, ok = get_text_input(self, "Rename Protocol", "Enter new name:", old_name)
        
        if ok and new_name and new_name != old_name:
            if storage.rename_protocol(self.current_model, old_name, new_name):
                item.setText(new_name)
                if self.current_protocol == old_name:
                    self.current_protocol = new_name
                    signals.protocol_selected.emit(self.current_model, new_name)
    
    def _on_delete_protocol(self):
        """Handle deleting a protocol."""
        item = self.list_widget.currentItem()
        if not item or not self.current_model:
            return
        
        protocol_name = item.text()
        if confirm_action(self, "Delete Protocol", f"Delete protocol '{protocol_name}'?"):
            if storage.delete_protocol(self.current_model, protocol_name):
                row = self.list_widget.row(item)
                self.list_widget.takeItem(row)
                
                # Select another protocol if available
                if self.list_widget.count() > 0:
                    new_row = min(row, self.list_widget.count() - 1)
                    self.list_widget.setCurrentRow(new_row)
                    self._on_protocol_selected(self.list_widget.item(new_row))
                else:
                    self.current_protocol = None
    
    def _show_context_menu(self, position):
        """Show context menu for protocol operations."""
        from PyQt5.QtWidgets import QMenu
        
        item = self.list_widget.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(self.list_widget.mapToGlobal(position))
        
        if action == rename_action:
            self._on_rename_protocol(item)
        elif action == delete_action:
            self._on_delete_protocol()
    
    def refresh(self):
        """Refresh the protocols list after hierarchy changes."""
        if not self.current_model:
            return
        
        current = self.current_protocol
        self._load_protocols()
        
        # Try to restore selection
        if current:
            for i in range(self.list_widget.count()):
                if self.list_widget.item(i).text() == current:
                    self.list_widget.setCurrentRow(i)
                    break
