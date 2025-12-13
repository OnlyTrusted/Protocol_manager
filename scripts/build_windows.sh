#!/usr/bin/env bash
set -euo pipefail

DIST_MODE=${1:-onefile}
APP_NAME="ProtocolClipboardManager"
ICON="resources/icon.ico"
DIST_DIR="dist"
NSIS_TEMPLATE="installer/installer.nsi.template"
NSIS_SCRIPT="installer/installer.nsi"
VERSION=${VERSION:-"0.1.0"}

echo "Building ${APP_NAME} (mode=${DIST_MODE})"

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

if [ "$DIST_MODE" = "onefile" ]; then
  pyinstaller --noconfirm --clean --onefile --windowed --name "${APP_NAME}" --icon "${ICON}" protocol_clipboard/main.py
else
  pyinstaller --noconfirm --clean --onedir --windowed --name "${APP_NAME}" --icon "${ICON}" protocol_clipboard/main.py
fi

if [ "$DIST_MODE" = "onefile" ]; then
  EXE_PATH="${DIST_DIR}/${APP_NAME}.exe"
else
  EXE_PATH="${DIST_DIR}/${APP_NAME}/${APP_NAME}.exe"
fi

echo "Built exe at: ${EXE_PATH}"

STAGING="installer/staging"
rm -rf "${STAGING}"
mkdir -p "${STAGING}/bin"
cp "${EXE_PATH}" "${STAGING}/bin/${APP_NAME}.exe"
cp "${ICON}" "${STAGING}/" 2>/dev/null || true

if [ -f "${NSIS_TEMPLATE}" ]; then
  sed "s|{{APP_NAME}}|${APP_NAME}|g; s|{{VERSION}}|${VERSION}|g" "${NSIS_TEMPLATE}" > "${NSIS_SCRIPT}"
fi

if command -v makensis >/dev/null 2>&1; then
  echo "Running makensis..."
  makensis "${NSIS_SCRIPT}"
  echo "Installer created."
else
  echo "makensis not found; NSIS installer step skipped."
fi

echo "Windows build script complete."
