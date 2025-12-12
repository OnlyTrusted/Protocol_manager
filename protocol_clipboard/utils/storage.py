"""
Storage utility for managing models and protocols data.
Handles JSON files and protocol text files with automatic directory creation.
"""
import json
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional


class StorageManager:
    """Manages persistent storage for models and protocols."""
    
    def __init__(self, base_path: str = None):
        """Initialize storage manager with base data path."""
        if base_path is None:
            # Default to data directory relative to this package
            package_dir = Path(__file__).parent.parent
            base_path = package_dir / "data"
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
    
    # ============= Version Management Methods =============
    
    def _parse_version(self, version: str) -> tuple:
        """
        Parse version string to tuple for comparison.
        Returns (major, minor) or (0, 0) for invalid versions.
        """
        try:
            parts = version.split('.')
            return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
        except (ValueError, IndexError):
            return (0, 0)
    
    def _get_protocol_dir(self, model_name: str, protocol_name: str) -> Path:
        """Get the directory path for a protocol."""
        return self.base_path / model_name / protocol_name
    
    def _get_versions_file(self, model_name: str, protocol_name: str) -> Path:
        """Get the versions.json file path for a protocol."""
        return self._get_protocol_dir(model_name, protocol_name) / "versions.json"
    
    def _get_version_file(self, model_name: str, protocol_name: str, version: str) -> Path:
        """Get the file path for a specific version."""
        return self._get_protocol_dir(model_name, protocol_name) / f"{version}.txt"
    
    def ensure_protocol_versions(self, model_name: str, protocol_name: str):
        """
        Ensure protocol has version structure. Migrates old .txt format if needed.
        Creates versions.json with 1.0 as default if missing.
        """
        protocol_dir = self._get_protocol_dir(model_name, protocol_name)
        versions_file = self._get_versions_file(model_name, protocol_name)
        old_protocol_file = self.base_path / model_name / f"{protocol_name}.txt"
        
        # Check if we need to migrate from old format
        if not versions_file.exists() and old_protocol_file.exists():
            # Migration: old flat .txt file exists
            protocol_dir.mkdir(parents=True, exist_ok=True)
            
            # Read old content
            content = old_protocol_file.read_text(encoding='utf-8')
            
            # Create version 1.0 with the old content
            version_file = self._get_version_file(model_name, protocol_name, "1.0")
            version_file.write_text(content, encoding='utf-8')
            
            # Create versions.json
            versions_data = {
                "versions": ["1.0"],
                "current": "1.0"
            }
            with open(versions_file, 'w', encoding='utf-8') as f:
                json.dump(versions_data, f, indent=2)
            
            # Delete old file
            old_protocol_file.unlink()
            
        elif not versions_file.exists():
            # No old file, create fresh versioning structure
            protocol_dir.mkdir(parents=True, exist_ok=True)
            
            # Create empty version 1.0
            version_file = self._get_version_file(model_name, protocol_name, "1.0")
            version_file.write_text("", encoding='utf-8')
            
            # Create versions.json
            versions_data = {
                "versions": ["1.0"],
                "current": "1.0"
            }
            with open(versions_file, 'w', encoding='utf-8') as f:
                json.dump(versions_data, f, indent=2)
    
    def list_versions(self, model_name: str, protocol_name: str) -> List[str]:
        """
        List all versions for a protocol, ordered semantically.
        Returns empty list if no versions exist.
        """
        versions_file = self._get_versions_file(model_name, protocol_name)
        
        if not versions_file.exists():
            return []
        
        try:
            with open(versions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                versions = data.get('versions', [])
                
                # Sort versions by semantic versioning
                return sorted(versions, key=self._parse_version)
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_current_version(self, model_name: str, protocol_name: str) -> str:
        """
        Get the current/default version for a protocol.
        Returns "1.0" if not set or file doesn't exist.
        """
        versions_file = self._get_versions_file(model_name, protocol_name)
        
        if not versions_file.exists():
            return "1.0"
        
        try:
            with open(versions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('current', "1.0")
        except (json.JSONDecodeError, IOError):
            return "1.0"
    
    def set_current_version(self, model_name: str, protocol_name: str, version: str) -> bool:
        """
        Set the current/default version for a protocol.
        Returns True if successful, False otherwise.
        """
        versions_file = self._get_versions_file(model_name, protocol_name)
        
        if not versions_file.exists():
            return False
        
        try:
            with open(versions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verify version exists
            if version not in data.get('versions', []):
                return False
            
            data['current'] = version
            
            with open(versions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            return True
        except (json.JSONDecodeError, IOError):
            return False
    
    def create_new_version(self, model_name: str, protocol_name: str, base_version: str = None) -> Optional[str]:
        """
        Create a new version by incrementing the patch number.
        Copies content from base_version if provided, otherwise empty.
        Returns the new version name (e.g., "1.1") or None if failed.
        """
        versions_file = self._get_versions_file(model_name, protocol_name)
        
        if not versions_file.exists():
            return None
        
        try:
            with open(versions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Use list_versions to get sorted list
            versions = self.list_versions(model_name, protocol_name)
            
            if not versions:
                return None
            
            # Get the latest version and increment patch
            latest = versions[-1]
            major, minor = self._parse_version(latest)
            
            new_version = f"{major}.{minor + 1}"
            
            # Get content from base version or use empty
            content = ""
            if base_version and base_version in versions:
                base_file = self._get_version_file(model_name, protocol_name, base_version)
                if base_file.exists():
                    content = base_file.read_text(encoding='utf-8')
            elif base_version is None and versions:
                # Use current version as base if no base specified
                current = data.get('current', versions[-1])
                current_file = self._get_version_file(model_name, protocol_name, current)
                if current_file.exists():
                    content = current_file.read_text(encoding='utf-8')
            
            # Create new version file
            new_file = self._get_version_file(model_name, protocol_name, new_version)
            new_file.write_text(content, encoding='utf-8')
            
            # Update versions.json
            versions.append(new_version)
            data['versions'] = versions
            
            with open(versions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            return new_version
        except (json.JSONDecodeError, IOError, ValueError):
            return None
    
    def read_version(self, model_name: str, protocol_name: str, version: str = None) -> str:
        """
        Read content of a specific version.
        If version is None, reads the current version.
        Returns empty string if version doesn't exist.
        """
        # Ensure versioning is set up
        self.ensure_protocol_versions(model_name, protocol_name)
        
        if version is None:
            version = self.get_current_version(model_name, protocol_name)
        
        version_file = self._get_version_file(model_name, protocol_name, version)
        
        if not version_file.exists():
            return ""
        
        try:
            return version_file.read_text(encoding='utf-8')
        except IOError:
            return ""
    
    def write_version(self, model_name: str, protocol_name: str, version: str, content: str):
        """
        Write content to a specific version file.
        """
        # Ensure versioning is set up
        self.ensure_protocol_versions(model_name, protocol_name)
        
        version_file = self._get_version_file(model_name, protocol_name, version)
        version_file.write_text(content, encoding='utf-8')


# Global storage manager instance
storage = StorageManager()
