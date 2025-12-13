"""
Storage utility for managing models and protocols data.
Handles JSON files and protocol text files with automatic directory creation.
"""
import json
import shutil
import logging
from pathlib import Path
from typing import List, Optional

# Set up logging
logger = logging.getLogger(__name__)


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
                content = f.read().strip()
                if not content:
                    logger.warning("models.json is empty, returning empty list")
                    return []
                data = json.loads(content)
                return data.get('models', [])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse models.json: {e}")
            return []
        except IOError as e:
            logger.error(f"Failed to read models.json: {e}")
            return []
    
    def save_models(self, models: List[str]):
        """Save list of models to models.json with atomic write."""
        self._ensure_directories()
        try:
            # Write to temporary file first (atomic write)
            temp_file = self.models_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump({'models': models}, f, indent=2)
            # Atomic replace
            temp_file.replace(self.models_file)
            logger.debug(f"Saved models: {models}")
        except IOError as e:
            logger.error(f"Failed to save models.json: {e}")
            raise
    
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
        """
        Rename a model and its directory.
        Returns True if successful, False otherwise.
        """
        models = self.load_models()
        if old_name not in models:
            logger.warning(f"Cannot rename: model '{old_name}' not found")
            return False
        
        if new_name in models:
            logger.warning(f"Cannot rename: model '{new_name}' already exists")
            return False
        
        # Rename directory if it exists
        old_path = self.base_path / old_name
        new_path = self.base_path / new_name
        
        try:
            if old_path.exists():
                if new_path.exists():
                    logger.error(f"Cannot rename: directory '{new_path}' already exists")
                    return False
                old_path.rename(new_path)
                logger.info(f"Renamed model directory from '{old_name}' to '{new_name}'")
            else:
                self._ensure_model_directory(new_name)
                logger.info(f"Created new directory for model '{new_name}'")
            
            # Update models list
            models[models.index(old_name)] = new_name
            self.save_models(models)
            return True
        except (IOError, OSError) as e:
            logger.error(f"Failed to rename model '{old_name}' to '{new_name}': {e}")
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """
        Delete a model and its directory.
        Returns True if successful, False otherwise.
        """
        models = self.load_models()
        if model_name not in models:
            logger.warning(f"Cannot delete: model '{model_name}' not found")
            return False
        
        try:
            # Remove from models list
            models.remove(model_name)
            self.save_models(models)
            
            # Delete directory if it exists
            model_path = self.base_path / model_name
            if model_path.exists():
                shutil.rmtree(model_path)
                logger.info(f"Deleted model '{model_name}' and its directory")
            
            return True
        except (IOError, OSError) as e:
            logger.error(f"Failed to delete model '{model_name}': {e}")
            return False
    
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
                content = f.read().strip()
                if not content:
                    logger.warning(f"order.json for {model_name} is empty")
                    return []
                data = json.loads(content)
                return data.get('protocols', [])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse order.json for {model_name}: {e}")
            return []
        except IOError as e:
            logger.error(f"Failed to read order.json for {model_name}: {e}")
            return []
    
    def save_protocol_order(self, model_name: str, protocols: List[str]):
        """Save protocol order for a specific model with atomic write."""
        model_path = self._ensure_model_directory(model_name)
        order_file = model_path / "order.json"
        
        try:
            # Write to temporary file first (atomic write)
            temp_file = order_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump({'protocols': protocols}, f, indent=2)
            # Atomic replace
            temp_file.replace(order_file)
            logger.debug(f"Saved protocol order for {model_name}: {protocols}")
        except IOError as e:
            logger.error(f"Failed to save protocol order for {model_name}: {e}")
            raise
    
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
        except IOError as e:
            logger.error(f"Failed to read protocol '{protocol_name}' for model '{model_name}': {e}")
            return ""
    
    def save_protocol(self, model_name: str, protocol_name: str, content: str):
        """Save protocol content to text file with atomic write."""
        model_path = self._ensure_model_directory(model_name)
        protocol_file = model_path / f"{protocol_name}.txt"
        
        try:
            # Write to temporary file first (atomic write)
            temp_file = protocol_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            # Atomic replace
            temp_file.replace(protocol_file)
            logger.debug(f"Saved protocol '{protocol_name}' for model '{model_name}'")
        except IOError as e:
            logger.error(f"Failed to save protocol '{protocol_name}' for model '{model_name}': {e}")
            raise
    
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
        """
        Rename a protocol and its file.
        Returns True if successful, False otherwise.
        """
        protocols = self.load_protocol_order(model_name)
        if old_name not in protocols:
            logger.warning(f"Cannot rename: protocol '{old_name}' not found in model '{model_name}'")
            return False
        
        if new_name in protocols:
            logger.warning(f"Cannot rename: protocol '{new_name}' already exists in model '{model_name}'")
            return False
        
        try:
            # Rename versioned directory if it exists
            old_dir = self.base_path / model_name / old_name
            new_dir = self.base_path / model_name / new_name
            
            if old_dir.exists() and old_dir.is_dir():
                if new_dir.exists():
                    logger.error(f"Cannot rename: directory '{new_dir}' already exists")
                    return False
                old_dir.rename(new_dir)
                logger.info(f"Renamed protocol directory from '{old_name}' to '{new_name}'")
            else:
                # Try legacy .txt file
                old_file = self.base_path / model_name / f"{old_name}.txt"
                new_file = self.base_path / model_name / f"{new_name}.txt"
                
                if old_file.exists():
                    if new_file.exists():
                        logger.error(f"Cannot rename: file '{new_file}' already exists")
                        return False
                    old_file.rename(new_file)
                    logger.info(f"Renamed protocol file from '{old_name}.txt' to '{new_name}.txt'")
                else:
                    # No file exists, just create empty version structure
                    self.save_protocol(model_name, new_name, "")
                    logger.info(f"Created new protocol '{new_name}' (no old file found)")
            
            # Update protocol order
            protocols[protocols.index(old_name)] = new_name
            self.save_protocol_order(model_name, protocols)
            return True
        except (IOError, OSError) as e:
            logger.error(f"Failed to rename protocol '{old_name}' to '{new_name}' in model '{model_name}': {e}")
            return False
    
    def delete_protocol(self, model_name: str, protocol_name: str) -> bool:
        """
        Delete a protocol and its file/folder.
        Returns True if successful, False otherwise.
        """
        protocols = self.load_protocol_order(model_name)
        if protocol_name not in protocols:
            logger.warning(f"Cannot delete: protocol '{protocol_name}' not found in model '{model_name}'")
            return False
        
        try:
            # Remove from order
            protocols.remove(protocol_name)
            self.save_protocol_order(model_name, protocols)
            
            # Delete versioned protocol directory if it exists
            protocol_dir = self._get_protocol_dir(model_name, protocol_name)
            if protocol_dir.exists():
                shutil.rmtree(protocol_dir)
                logger.info(f"Deleted protocol directory '{protocol_name}'")
            
            # Delete legacy .txt file if it exists
            protocol_file = self.base_path / model_name / f"{protocol_name}.txt"
            if protocol_file.exists():
                protocol_file.unlink()
                logger.info(f"Deleted legacy protocol file '{protocol_name}.txt'")
            
            return True
        except (IOError, OSError) as e:
            logger.error(f"Failed to delete protocol '{protocol_name}' from model '{model_name}': {e}")
            return False
    
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
        This method is idempotent - safe to call multiple times.
        """
        protocol_dir = self._get_protocol_dir(model_name, protocol_name)
        versions_file = self._get_versions_file(model_name, protocol_name)
        old_protocol_file = self.base_path / model_name / f"{protocol_name}.txt"
        
        # Already has versioning structure
        if versions_file.exists():
            return
        
        try:
            # Check if we need to migrate from old format
            if old_protocol_file.exists():
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
                logger.info(f"Migrated protocol '{protocol_name}' from old format to versioned format")
                
            else:
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
                logger.info(f"Created new versioning structure for protocol '{protocol_name}'")
        except (IOError, OSError) as e:
            logger.error(f"Failed to ensure protocol versions for {model_name}/{protocol_name}: {e}")
            raise
    
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
                content = f.read().strip()
                if not content:
                    logger.warning(f"versions.json for {model_name}/{protocol_name} is empty")
                    return []
                data = json.loads(content)
                versions = data.get('versions', [])
                
                # Sort versions by semantic versioning
                return sorted(versions, key=self._parse_version)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse versions.json for {model_name}/{protocol_name}: {e}")
            return []
        except IOError as e:
            logger.error(f"Failed to read versions.json for {model_name}/{protocol_name}: {e}")
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
                content = f.read().strip()
                if not content:
                    logger.warning(f"versions.json for {model_name}/{protocol_name} is empty, returning default '1.0'")
                    return "1.0"
                data = json.loads(content)
                current = data.get('current', "1.0")
                # Verify current version exists in versions list
                versions = data.get('versions', [])
                if current not in versions and versions:
                    logger.warning(f"Current version '{current}' not in versions list, using first version")
                    return versions[0]
                return current
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse versions.json for {model_name}/{protocol_name}: {e}, returning default '1.0'")
            return "1.0"
        except IOError as e:
            logger.error(f"Failed to read versions.json for {model_name}/{protocol_name}: {e}, returning default '1.0'")
            return "1.0"
    
    def set_current_version(self, model_name: str, protocol_name: str, version: str) -> bool:
        """
        Set the current/default version for a protocol.
        Returns True if successful, False otherwise.
        """
        versions_file = self._get_versions_file(model_name, protocol_name)
        
        if not versions_file.exists():
            logger.warning(f"Cannot set current version: versions.json not found for {model_name}/{protocol_name}")
            return False
        
        try:
            with open(versions_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logger.error(f"versions.json for {model_name}/{protocol_name} is empty")
                    return False
                data = json.loads(content)
            
            # Verify version exists
            if version not in data.get('versions', []):
                logger.warning(f"Version '{version}' not found in versions list")
                return False
            
            data['current'] = version
            
            # Atomic write
            temp_file = versions_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            temp_file.replace(versions_file)
            
            logger.info(f"Set current version to '{version}' for {model_name}/{protocol_name}")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse versions.json for {model_name}/{protocol_name}: {e}")
            return False
        except IOError as e:
            logger.error(f"Failed to update versions.json for {model_name}/{protocol_name}: {e}")
            return False
    
    def create_new_version(self, model_name: str, protocol_name: str, base_version: str = None) -> Optional[str]:
        """
        Create a new version by incrementing the patch number.
        Copies content from base_version if provided, otherwise from current version.
        Returns the new version name (e.g., "1.1") or None if failed.
        """
        versions_file = self._get_versions_file(model_name, protocol_name)
        
        if not versions_file.exists():
            logger.error(f"Cannot create version: versions.json not found for {model_name}/{protocol_name}")
            return None
        
        try:
            with open(versions_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logger.error(f"versions.json for {model_name}/{protocol_name} is empty")
                    return None
                data = json.loads(content)
            
            # Use list_versions to get sorted list
            versions = self.list_versions(model_name, protocol_name)
            
            if not versions:
                logger.error(f"No versions found for {model_name}/{protocol_name}")
                return None
            
            # Get the latest version and increment patch
            latest = versions[-1]
            major, minor = self._parse_version(latest)
            
            new_version = f"{major}.{minor + 1}"
            
            # Check if version already exists (shouldn't happen, but be safe)
            if new_version in versions:
                logger.warning(f"Version '{new_version}' already exists, using next available")
                new_version = f"{major}.{minor + 2}"
            
            # Get content from base version or use current
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
            
            # Update versions.json with atomic write
            versions.append(new_version)
            data['versions'] = versions
            
            temp_file = versions_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            temp_file.replace(versions_file)
            
            logger.info(f"Created new version '{new_version}' for {model_name}/{protocol_name}")
            return new_version
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse versions.json for {model_name}/{protocol_name}: {e}")
            return None
        except (IOError, OSError, ValueError) as e:
            logger.error(f"Failed to create new version for {model_name}/{protocol_name}: {e}")
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
            logger.warning(f"Version file not found: {version_file}")
            return ""
        
        try:
            return version_file.read_text(encoding='utf-8')
        except IOError as e:
            logger.error(f"Failed to read version '{version}' for {model_name}/{protocol_name}: {e}")
            return ""
    
    def write_version(self, model_name: str, protocol_name: str, version: str, content: str):
        """
        Write content to a specific version file with atomic write.
        """
        # Ensure versioning is set up
        self.ensure_protocol_versions(model_name, protocol_name)
        
        version_file = self._get_version_file(model_name, protocol_name, version)
        
        try:
            # Atomic write using temporary file
            temp_file = version_file.with_suffix('.tmp')
            temp_file.write_text(content, encoding='utf-8')
            temp_file.replace(version_file)
            logger.debug(f"Wrote version '{version}' for {model_name}/{protocol_name}")
        except IOError as e:
            logger.error(f"Failed to write version '{version}' for {model_name}/{protocol_name}: {e}")
            raise


# Global storage manager instance
storage = StorageManager()
