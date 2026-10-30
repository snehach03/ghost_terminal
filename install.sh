#!/usr/bin/env bash
set -e
RDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$(which python3 2>/dev/null || which python 2>/dev/null)"
"$PY" "$RDIR/sounds/generate_sounds.py"

RC="$HOME/.bashrc"
HOOK="$RDIR/hooks/ghost.bash"
if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
    RC="$HOME/.zshrc"; HOOK="$RDIR/hooks/ghost.zsh"
fi

echo "Adding hook to $RC..."
if grep -q "ghost-shell" "$RC" 2>/dev/null; then
    echo "Already installed in $RC."
else
    echo "" >> "$RC"
    echo "# Ghost Shell" >> "$RC"
    echo "source "$HOOK"" >> "$RC"
    echo "Successfully installed! Run: source $RC"
fi
