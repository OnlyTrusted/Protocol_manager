"""
Editor panel - text editor with autosave and clipboard integration.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import QTimer

from .styles import get_text_edit_stylesheet, get_label_stylesheet
from .signals import signals
from ..utils.storage import storage
from ..utils import clipboard


class EditorPanel(QWidget):
    """Panel for editing protocol content with autosave."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_model = None
        self.current_protocol = None
        self.current_version = None
        self.autosave_timer = QTimer()
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.timeout.connect(self._save_content)
        self._is_loading = False
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Label
        label = QLabel("EDITOR")
        label.setStyleSheet(get_label_stylesheet())
        layout.addWidget(label)
        
        # Text edit
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet(get_text_edit_stylesheet())
        self.text_edit.setPlaceholderText("Select a protocol to edit...")
        self.text_edit.textChanged.connect(self._on_text_changed)
        self.text_edit.setEnabled(False)
        layout.addWidget(self.text_edit)
    
    def _connect_signals(self):
        """Connect to application signals."""
        signals.protocol_selected.connect(self._on_protocol_selected)
    
    def _on_protocol_selected(self, model_name: str, protocol_name: str, version: str):
        """Handle protocol selection - load version content and copy to clipboard."""
        # Save current content first if different protocol or version
        if self.current_model and self.current_protocol and self.current_version:
            if (self.current_model != model_name or 
                self.current_protocol != protocol_name or
                self.current_version != version):
                self._save_content()
        
        # Load new protocol version
        self.current_model = model_name
        self.current_protocol = protocol_name
        self.current_version = version
        
        # Load content from specific version
        self._is_loading = True
        content = storage.read_version(model_name, protocol_name, version)
        self.text_edit.setPlainText(content)
        self._is_loading = False
        
        # Enable editing
        self.text_edit.setEnabled(True)
        
        # Copy to clipboard
        clipboard.copy(content)
        
        # Emit loaded signal for status bar
        signals.protocol_loaded.emit(model_name, protocol_name, version)
    
    def _on_text_changed(self):
        """Handle text changes - trigger autosave with debounce."""
        if self._is_loading:
            return
        
        if not self.current_model or not self.current_protocol or not self.current_version:
            return
        
        # Restart the autosave timer (debounce ~400ms)
        self.autosave_timer.stop()
        self.autosave_timer.start(400)
    
    def _save_content(self):
        """Save the current content to storage."""
        if not self.current_model or not self.current_protocol or not self.current_version:
            return
        
        content = self.text_edit.toPlainText()
        storage.write_version(self.current_model, self.current_protocol, self.current_version, content)
        
        # Emit saved signal
        signals.protocol_saved.emit(self.current_model, self.current_protocol, self.current_version)
    
    def clear(self):
        """Clear the editor."""
        self._is_loading = True
        self.text_edit.clear()
        self.text_edit.setEnabled(False)
        self._is_loading = False
        self.current_model = None
        self.current_protocol = None
        self.current_version = None
    
    def save_and_cleanup(self):
        """Save any pending content and stop timers. Called when application closes."""
        # Stop autosave timer
        if self.autosave_timer.isActive():
            self.autosave_timer.stop()
        # Save any pending content
        self._save_content()
