#!/usr/bin/env bash
#
# serverctl-tui bootstrap script.
# Creates a virtual environment, installs dependencies, and launches the app.
#
# Usage:
#   ./run.sh            # set up (if needed) and run
#   ./run.sh --setup    # set up only, do not launch

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$SCRIPT_DIR/requirements.txt"

if [ "${1:-}" = "--setup" ]; then
    echo "Setup complete. Run './run.sh' to launch."
    exit 0
fi

echo "Launching serverctl-tui..."
exec "$VENV_DIR/bin/python" "$SCRIPT_DIR/apps/app.py"
