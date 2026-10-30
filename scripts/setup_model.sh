#!/usr/bin/env bash
set -e
MDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../models" && pwd)"
mkdir -p "$MDIR"
URL="https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf"
DEST="$MDIR/qwen2.5-0.5b-instruct-q4_k_m.gguf"
if [ ! -f "$DEST" ]; then
    echo "Downloading lightweight model (~397 MB)..."
    curl -L "$URL" -o "$DEST"
fi
echo "Model ready at $DEST"
