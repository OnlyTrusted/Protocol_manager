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
    
    # Emitted when a protocol is loaded into editor and copied to clipboard
    # (model_name, protocol_name, version)
    protocol_loaded = pyqtSignal(str, str, str)
    
    # Emitted when a protocol is saved (for future use, e.g., status indication)
    # (model_name, protocol_name, version)
    protocol_saved = pyqtSignal(str, str, str)
    
    # Emitted when the current version is changed for a protocol (for future use)
    # (model_name, protocol_name, version)
    version_changed = pyqtSignal(str, str, str)
    
    # Emitted when hierarchy (ordering) changes
    hierarchy_changed = pyqtSignal()


# Global signals instance
signals = AppSignals()
