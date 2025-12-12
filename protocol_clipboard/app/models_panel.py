"""
Models panel - displays and manages the list of models.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt

from .styles import get_list_widget_stylesheet, get_button_stylesheet, get_label_stylesheet
from .signals import signals
from ..utils.storage import storage
from ..utils.dialogs import get_text_input, confirm_action


class ModelsPanel(QWidget):
    """Panel for displaying and managing models."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_model = None
        self._setup_ui()
        self._load_models()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Label
        label = QLabel("MODELS")
        label.setStyleSheet(get_label_stylesheet())
        layout.addWidget(label)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(get_list_widget_stylesheet())
        self.list_widget.itemClicked.connect(self._on_model_selected)
        self.list_widget.itemDoubleClicked.connect(self._on_rename_model)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.list_widget)
        
        # Add button
        add_button = QPushButton("+")
        add_button.setStyleSheet(get_button_stylesheet())
        add_button.clicked.connect(self._on_add_model)
        layout.addWidget(add_button)
    
    def _load_models(self):
        """Load models from storage and populate the list."""
        self.list_widget.clear()
        models = storage.load_models()
        self.list_widget.addItems(models)
        
        # Select first model if available
        if models and self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)
            self._on_model_selected(self.list_widget.item(0))
    
    def _on_model_selected(self, item):
        """Handle model selection."""
        if item:
            model_name = item.text()
            self.current_model = model_name
            signals.model_selected.emit(model_name)
    
    def _on_add_model(self):
        """Handle adding a new model."""
        name, ok = get_text_input(self, "New Model", "Enter model name:")
        if ok and name:
            if storage.add_model(name):
                self.list_widget.addItem(name)
                # Select the newly added model
                self.list_widget.setCurrentRow(self.list_widget.count() - 1)
                self._on_model_selected(self.list_widget.item(self.list_widget.count() - 1))
            else:
                # Model already exists
                pass
    
    def _on_rename_model(self, item):
        """Handle renaming a model."""
        if not item:
            return
        
        old_name = item.text()
        new_name, ok = get_text_input(self, "Rename Model", "Enter new name:", old_name)
        
        if ok and new_name and new_name != old_name:
            if storage.rename_model(old_name, new_name):
                item.setText(new_name)
                if self.current_model == old_name:
                    self.current_model = new_name
                    signals.model_selected.emit(new_name)
    
    def _on_delete_model(self):
        """Handle deleting a model."""
        item = self.list_widget.currentItem()
        if not item:
            return
        
        model_name = item.text()
        if confirm_action(self, "Delete Model", f"Delete model '{model_name}' and all its protocols?"):
            if storage.delete_model(model_name):
                row = self.list_widget.row(item)
                self.list_widget.takeItem(row)
                
                # Select another model if available
                if self.list_widget.count() > 0:
                    new_row = min(row, self.list_widget.count() - 1)
                    self.list_widget.setCurrentRow(new_row)
                    self._on_model_selected(self.list_widget.item(new_row))
                else:
                    self.current_model = None
    
    def _show_context_menu(self, position):
        """Show context menu for model operations."""
        from PyQt5.QtWidgets import QMenu
        
        item = self.list_widget.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(self.list_widget.mapToGlobal(position))
        
        if action == rename_action:
            self._on_rename_model(item)
        elif action == delete_action:
            self._on_delete_model()
    
    def refresh(self):
        """Refresh the models list after hierarchy changes."""
        current = self.current_model
        self._load_models()
        
        # Try to restore selection
        if current:
            for i in range(self.list_widget.count()):
                if self.list_widget.item(i).text() == current:
                    self.list_widget.setCurrentRow(i)
                    break
