#!/usr/bin/env bash
MDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../models" && pwd)"
BIN="$MDIR/llama-server"
[ -x "$BIN" ] || BIN="$(which llama-server 2>/dev/null || true)"
if [ -z "$BIN" ]; then echo "llama-server binary not found. Download it from https://github.com/ggerganov/llama.cpp/releases"; exit 1; fi
exec "$BIN" --model "$MDIR/qwen2.5-0.5b-instruct-q4_k_m.gguf" --host 127.0.0.1 --port 8080 --ctx-size 2048 --threads 4
