# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

project_name = "ProtocolClipboardManager"
icon_file = os.path.join('resources', 'icon.ico')

a = Analysis(
    ['protocol_clipboard/main.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('resources', 'resources')],
    hiddenimports=[],
    hookspath=[],
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=project_name,
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon_file,
)
