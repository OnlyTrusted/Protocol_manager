# Protocol Clipboard Manager

A desktop application for managing and organizing AI agent protocols with instant clipboard access.

## Features

- **Model Management**: Organize protocols by AI model (ChatGPT, Claude, Copilot, etc.)
- **Quick Access**: Select any protocol to instantly copy it to clipboard
- **Auto-save**: Edits are automatically saved as you type (400ms debounce)
- **Custom Ordering**: Drag and drop to reorder models and protocols
- **Dark Theme**: Modern dark UI with rounded corners
- **Persistent Storage**: All data stored locally in JSON and text files
- **Protocol Versioning**: Each protocol can have multiple versions with version management

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

From the project root directory:
```bash
python -m protocol_clipboard.main
```

Or from within the protocol_clipboard directory:
```bash
python main.py
```

## Usage

1. **Select a Model**: Click on a model in the left panel
2. **Select a Protocol**: Click on a protocol in the middle panel (auto-copies to clipboard)
3. **Edit**: Make changes in the right editor panel (auto-saves)
4. **Add New**: Use the "+" buttons to add models or protocols
5. **Rename/Delete**: Double-click to rename, or right-click for context menu
6. **Reorder**: Menu → Manage Hierarchy → Reorder Models/Protocols (Ctrl+H)
7. **Version Management**: Right-click a protocol to:
   - **Add Version**: Create a new version (increments from current)
   - **Select Version**: Choose a specific version to view/edit
   - **Set as Current**: Mark selected version as default

## Protocol Versioning

Each protocol supports multiple versions for iteration and improvement:

- **Version Format**: Uses semantic versioning (1.0, 1.1, 1.2, etc.)
- **Default Behavior**: When selecting a protocol, the current/default version loads automatically
- **Version Creation**: Right-click → "Add Version" creates a new version by copying the current version's content
- **Version Selection**: Right-click → "Select Version" submenu shows all versions (current version marked)
- **Set Current**: Right-click → "Set Selected as Current" makes the active version the default
- **Auto-save**: Edits always save to the currently selected version
- **Clipboard**: The selected version's content is copied to clipboard

### Version Storage Structure

Versioned protocols are stored as:
```
data/{model_name}/{protocol_name}/
  ├── versions.json          # Metadata: versions list and current version
  ├── 1.0.txt               # Version 1.0 content
  ├── 1.1.txt               # Version 1.1 content
  └── 1.2.txt               # Version 1.2 content
```

### Backward Compatibility

Old protocols stored as flat `.txt` files are automatically migrated to the versioned structure:
- Original content becomes version 1.0
- `versions.json` is created automatically
- Old `.txt` file is removed after migration

## Data Storage

All data is stored in `protocol_clipboard/data/`:
- `models.json`: List of models and their order
- `{model_name}/order.json`: Protocol order for each model
- `{model_name}/{protocol_name}/`: Versioned protocol directory
  - `versions.json`: Version metadata (list of versions, current version)
  - `{version}.txt`: Individual version files (e.g., 1.0.txt, 1.1.txt)

## UI Features

- Black background (#0b0b0d)
- Dark grey panels (#141418)
- Rounded editor (#1f1f24)
- No default Qt blue highlights
- Status bar shows clipboard confirmation
