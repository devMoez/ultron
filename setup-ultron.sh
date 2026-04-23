#!/usr/bin/env bash
# setup-ultron.sh
# Run this script ONCE to register 'ultron' as a global command.
# Usage: bash setup-ultron.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/packages/opencode"

if [ ! -d "$PACKAGE_DIR" ]; then
  echo "Error: Could not find packages/opencode relative to this script. Run from the repo root." >&2
  exit 1
fi

echo "Linking 'ultron' globally from: $PACKAGE_DIR"
cd "$PACKAGE_DIR"

# Try bun link first, fall back to npm link
if command -v bun &>/dev/null; then
  echo "Using bun link..."
  bun link
elif command -v npm &>/dev/null; then
  echo "Using npm link..."
  npm link
else
  echo "Error: Neither 'bun' nor 'npm' found. Please install Node.js or Bun first." >&2
  exit 1
fi

echo ""
echo "Done! You can now run 'ultron' from any directory."
echo "Try: ultron --help"
