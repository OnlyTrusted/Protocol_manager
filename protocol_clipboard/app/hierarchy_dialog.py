"""
Hierarchy dialog - drag and drop interface for reordering models and protocols.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                             QTreeWidgetItem, QPushButton, QLabel)
from PyQt5.QtCore import Qt

from .styles import get_tree_widget_stylesheet, get_button_stylesheet, get_label_stylesheet
from .signals import signals
from ..utils.storage import storage


class HierarchyDialog(QDialog):
    """Dialog for managing model and protocol ordering via drag and drop."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Hierarchy")
        self.setModal(True)
        self.resize(600, 500)
        self._setup_ui()
        self._load_hierarchy()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # Instructions label
        info_label = QLabel("Drag and drop to reorder models and protocols")
        info_label.setStyleSheet(get_label_stylesheet())
        layout.addWidget(info_label)
        
        # Tree widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setStyleSheet(get_tree_widget_stylesheet())
        self.tree_widget.setHeaderLabel("Models and Protocols")
        self.tree_widget.setDragDropMode(QTreeWidget.InternalMove)
        self.tree_widget.setSelectionMode(QTreeWidget.SingleSelection)
        self.tree_widget.setExpandsOnDoubleClick(True)
        layout.addWidget(self.tree_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet(get_button_stylesheet())
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Save")
        save_button.setStyleSheet(get_button_stylesheet())
        save_button.clicked.connect(self._save_hierarchy)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def _load_hierarchy(self):
        """Load current hierarchy into the tree."""
        self.tree_widget.clear()
        
        models = storage.load_models()
        
        for model in models:
            model_item = QTreeWidgetItem([model])
            model_item.setData(0, Qt.UserRole, {'type': 'model', 'name': model})
            self.tree_widget.addTopLevelItem(model_item)
            
            protocols = storage.load_protocol_order(model)
            for protocol in protocols:
                protocol_item = QTreeWidgetItem([protocol])
                protocol_item.setData(0, Qt.UserRole, {'type': 'protocol', 'name': protocol})
                model_item.addChild(protocol_item)
            
            model_item.setExpanded(True)
    
    def _save_hierarchy(self):
        """Save the new hierarchy from the tree."""
        # Extract new model order
        models = []
        for i in range(self.tree_widget.topLevelItemCount()):
            model_item = self.tree_widget.topLevelItem(i)
            model_name = model_item.text(0)
            models.append(model_name)
            
            # Extract protocol order for this model
            protocols = []
            for j in range(model_item.childCount()):
                protocol_item = model_item.child(j)
                protocol_name = protocol_item.text(0)
                protocols.append(protocol_name)
            
            # Save protocol order
            storage.save_protocol_order(model_name, protocols)
        
        # Save model order
        storage.save_models(models)
        
        # Emit signal to refresh UI
        signals.hierarchy_changed.emit()
        
        # Close dialog
        self.accept()
