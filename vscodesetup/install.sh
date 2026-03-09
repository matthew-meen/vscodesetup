#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# ── Python ──────────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 not found. Install it with: brew install python" >&2
  exit 1
fi

# ── Venv ─────────────────────────────────────────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
  echo "▶ Creating Python venv at $VENV_DIR …"
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# ── Dependencies ─────────────────────────────────────────────────────────────
echo "▶ Installing Python dependencies …"
pip install --quiet --upgrade pip
pip install --quiet -r "$SCRIPT_DIR/requirements.txt"

# ── Run setup ────────────────────────────────────────────────────────────────
python3 "$SCRIPT_DIR/setup.py"
