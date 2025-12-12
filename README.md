# Protocol Clipboard Manager

A desktop application for managing and organizing AI agent protocols with instant clipboard access.

## Features

- **Model Management**: Organize protocols by AI model (ChatGPT, Claude, Copilot, etc.)
- **Quick Access**: Select any protocol to instantly copy it to clipboard
- **Auto-save**: Edits are automatically saved as you type (400ms debounce)
- **Custom Ordering**: Drag and drop to reorder models and protocols
- **Dark Theme**: Modern dark UI with rounded corners
- **Persistent Storage**: All data stored locally in JSON and text files

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

## Data Storage

All data is stored in `protocol_clipboard/data/`:
- `models.json`: List of models and their order
- `{model_name}/order.json`: Protocol order for each model
- `{model_name}/{protocol_name}.txt`: Protocol content

## UI Features

- Black background (#0b0b0d)
- Dark grey panels (#141418)
- Rounded editor (#1f1f24)
- No default Qt blue highlights
- Status bar shows clipboard confirmation
