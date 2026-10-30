#!/usr/bin/env bash
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc" ]; then
        sed -i.bak '/# Ghost Shell/d' "$rc" 2>/dev/null || sed -i '' '/# Ghost Shell/d' "$rc" 2>/dev/null || true
        sed -i.bak '/ghost\.\(bash\|zsh\)/d' "$rc" 2>/dev/null || sed -i '' '/ghost\.\(bash\|zsh\)/d' "$rc" 2>/dev/null || true
        rm -f "${rc}.bak"
    fi
done
echo "Ghost Shell uninstalled."
