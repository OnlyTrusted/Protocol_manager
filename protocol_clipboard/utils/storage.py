"""
Storage utility for managing models and protocols data.
Handles JSON files and protocol text files with automatic directory creation.
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class StorageManager:
    """Manages persistent storage for models and protocols."""
    
    def __init__(self, base_path: str = "data"):
        """Initialize storage manager with base data path."""
        self.base_path = Path(base_path)
        self.models_file = self.base_path / "models.json"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure base data directory exists."""
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _ensure_model_directory(self, model_name: str):
        """Ensure model-specific directory exists."""
        model_path = self.base_path / model_name
        model_path.mkdir(parents=True, exist_ok=True)
        return model_path
    
    def load_models(self) -> List[str]:
        """Load list of models from models.json, return in stored order."""
        if not self.models_file.exists():
            # Create default models.json with sample models
            default_models = ["chatgpt", "claude", "copilot"]
            self.save_models(default_models)
            # Create default data for each model
            for model in default_models:
                self._ensure_model_directory(model)
                self.save_protocol_order(model, [])
            return default_models
        
        try:
            with open(self.models_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('models', [])
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_models(self, models: List[str]):
        """Save list of models to models.json."""
        self._ensure_directories()
        with open(self.models_file, 'w', encoding='utf-8') as f:
            json.dump({'models': models}, f, indent=2)
    
    def add_model(self, model_name: str) -> bool:
        """Add a new model."""
        models = self.load_models()
        if model_name in models:
            return False
        models.append(model_name)
        self.save_models(models)
        self._ensure_model_directory(model_name)
        self.save_protocol_order(model_name, [])
        return True
    
    def rename_model(self, old_name: str, new_name: str) -> bool:
        """Rename a model and its directory."""
        models = self.load_models()
        if old_name not in models or new_name in models:
            return False
        
        # Rename directory if it exists
        old_path = self.base_path / old_name
        new_path = self.base_path / new_name
        if old_path.exists():
            old_path.rename(new_path)
        else:
            self._ensure_model_directory(new_name)
        
        # Update models list
        models[models.index(old_name)] = new_name
        self.save_models(models)
        return True
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a model and its directory."""
        models = self.load_models()
        if model_name not in models:
            return False
        
        # Remove from models list
        models.remove(model_name)
        self.save_models(models)
        
        # Delete directory if it exists
        model_path = self.base_path / model_name
        if model_path.exists():
            import shutil
            shutil.rmtree(model_path)
        
        return True
    
    def load_protocol_order(self, model_name: str) -> List[str]:
        """Load protocol order for a specific model."""
        order_file = self.base_path / model_name / "order.json"
        
        if not order_file.exists():
            # Auto-create order.json
            self._ensure_model_directory(model_name)
            self.save_protocol_order(model_name, [])
            return []
        
        try:
            with open(order_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('protocols', [])
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_protocol_order(self, model_name: str, protocols: List[str]):
        """Save protocol order for a specific model."""
        model_path = self._ensure_model_directory(model_name)
        order_file = model_path / "order.json"
        
        with open(order_file, 'w', encoding='utf-8') as f:
            json.dump({'protocols': protocols}, f, indent=2)
    
    def load_protocol(self, model_name: str, protocol_name: str) -> str:
        """Load protocol content from text file."""
        protocol_file = self.base_path / model_name / f"{protocol_name}.txt"
        
        if not protocol_file.exists():
            # Auto-create empty protocol file
            self._ensure_model_directory(model_name)
            self.save_protocol(model_name, protocol_name, "")
            return ""
        
        try:
            with open(protocol_file, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            return ""
    
    def save_protocol(self, model_name: str, protocol_name: str, content: str):
        """Save protocol content to text file."""
        model_path = self._ensure_model_directory(model_name)
        protocol_file = model_path / f"{protocol_name}.txt"
        
        with open(protocol_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def add_protocol(self, model_name: str, protocol_name: str) -> bool:
        """Add a new protocol to a model."""
        protocols = self.load_protocol_order(model_name)
        if protocol_name in protocols:
            return False
        
        protocols.append(protocol_name)
        self.save_protocol_order(model_name, protocols)
        self.save_protocol(model_name, protocol_name, "")
        return True
    
    def rename_protocol(self, model_name: str, old_name: str, new_name: str) -> bool:
        """Rename a protocol and its file."""
        protocols = self.load_protocol_order(model_name)
        if old_name not in protocols or new_name in protocols:
            return False
        
        # Rename file if it exists
        old_file = self.base_path / model_name / f"{old_name}.txt"
        new_file = self.base_path / model_name / f"{new_name}.txt"
        
        if old_file.exists():
            old_file.rename(new_file)
        else:
            self.save_protocol(model_name, new_name, "")
        
        # Update protocol order
        protocols[protocols.index(old_name)] = new_name
        self.save_protocol_order(model_name, protocols)
        return True
    
    def delete_protocol(self, model_name: str, protocol_name: str) -> bool:
        """Delete a protocol and its file."""
        protocols = self.load_protocol_order(model_name)
        if protocol_name not in protocols:
            return False
        
        # Remove from order
        protocols.remove(protocol_name)
        self.save_protocol_order(model_name, protocols)
        
        # Delete file if it exists
        protocol_file = self.base_path / model_name / f"{protocol_name}.txt"
        if protocol_file.exists():
            protocol_file.unlink()
        
        return True


# Global storage manager instance
storage = StorageManager()
