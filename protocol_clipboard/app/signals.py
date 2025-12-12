"""
Centralized signals for communication between components.
Uses Qt signals for type-safe event handling.
"""
from PyQt5.QtCore import QObject, pyqtSignal


class AppSignals(QObject):
    """Centralized signals for the application."""
    
    # Emitted when a model is selected (model_name)
    model_selected = pyqtSignal(str)
    
    # Emitted when a protocol is selected (model_name, protocol_name)
    protocol_selected = pyqtSignal(str, str)
    
    # Emitted when a protocol is updated (model_name, protocol_name, content)
    protocol_updated = pyqtSignal(str, str, str)
    
    # Emitted when hierarchy (ordering) changes
    hierarchy_changed = pyqtSignal()


# Global signals instance
signals = AppSignals()
