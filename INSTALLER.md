# Windows Installer Build Guide

## Prerequisites
1. Python 3.8+
2. PyInstaller: `pip install pyinstaller`
3. NSIS (for installer): https://nsis.sourceforge.io/Download
4. Optional: `resources/icon.ico` for custom app icon

## Building Locally

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Step 2: Add icon (optional)
Place a Windows icon file at `resources/icon.ico`

### Step 3: Run build script
```bash
bash ./scripts/build_windows.sh onefile
```

This creates:
- Standalone `.exe` in `dist/`
- NSIS installer (if NSIS is installed): `ProtocolClipboardManager_Setup_0.1.0.exe`

## Using GitHub Actions

1. Go to **Actions** tab in your repo
2. Click **"Build Windows Installer"**
3. Click **"Run workflow"**
4. Wait for completion (5-10 minutes)
5. Download artifacts from the workflow run

## Installing

1. Download `ProtocolClipboardManager_Setup_X.X.X.exe`
2. Run the installer (click "Run anyway" if SmartScreen warns)
3. Install to `C:\Program Files\ProtocolClipboardManager\`
4. Launch from Start Menu or Desktop shortcut

## Distributing

### GitHub Releases
1. Tag a release: `git tag v0.1.0 && git push origin v0.1.0`
2. GitHub Actions builds automatically
3. Download artifact and attach to GitHub Release

### Code Signing (Optional)
For production, sign the executable to avoid SmartScreen warnings:
```bash
signtool sign /f cert.pfx /p password /tr http://timestamp.digicert.com /td sha256 ProtocolClipboardManager.exe
```

## Troubleshooting

**makensis not found**
- Install NSIS and add to PATH

**icon.ico not found**
- Add icon to `resources/` or build will use default

**Module import errors**
- Add missing modules to `hiddenimports` in `protocol_clipboard.spec`
