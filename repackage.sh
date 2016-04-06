#!/usr/bin/env bash
# Download and the PyQt4 Windows installer and unpack files from it into
# pynsist_pkgs

set -e

export PY_VERSION=3.4
export PYQT_VERSION=4.11.3
export PY_BITNESS=32
QT_VERSION=4.8.6

INSTALLER_FILE=PyQt4-${PYQT_VERSION}-gpl-Py${PY_VERSION}-Qt${QT_VERSION}-x${PY_BITNESS}.exe
URL=http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-${PYQT_VERSION}/${INSTALLER_FILE}
if [ ! -f "$INSTALLER_FILE" ]; then
  wget -O "$INSTALLER_FILE" "$URL"
fi

rm -rf pyqt4-windows
mkdir pyqt4-windows
7z x -opyqt4-windows "$INSTALLER_FILE"

# Trim some unnecessary files
rm -r pyqt4-windows/Lib/site-packages/PyQt4/doc
rm -r pyqt4-windows/Lib/site-packages/PyQt4/examples
rm -r pyqt4-windows/Lib/site-packages/PyQt4/assistant.exe
rm -r pyqt4-windows/Lib/site-packages/PyQt4/designer.exe

python3 make_wheel.py pyqt4-windows/Lib/site-packages/PyQt4

rm -r pyqt4-windows
echo "Done"
