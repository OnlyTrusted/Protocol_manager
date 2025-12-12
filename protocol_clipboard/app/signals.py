"""
Centralized signals for communication between components.
Uses Qt signals for type-safe event handling.
"""
from PyQt5.QtCore import QObject, pyqtSignal


class AppSignals(QObject):
    """Centralized signals for the application."""
    
    # Emitted when a model is selected (model_name)
    model_selected = pyqtSignal(str)
    
    # Emitted when a protocol is selected (model_name, protocol_name, version)
    protocol_selected = pyqtSignal(str, str, str)
    
    # Emitted when a protocol is updated (model_name, protocol_name, version, content)
    protocol_updated = pyqtSignal(str, str, str, str)
    
    # Emitted when a version is changed for a protocol (model_name, protocol_name, version)
    version_changed = pyqtSignal(str, str, str)
    
    # Emitted when hierarchy (ordering) changes
    hierarchy_changed = pyqtSignal()


# Global signals instance
signals = AppSignals()
