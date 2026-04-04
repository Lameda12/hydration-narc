#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.narc.pid"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Hydration Narc is already running (PID $(cat "$PID_FILE"))."
  exit 1
fi

cd "$SCRIPT_DIR"
nohup uv run python "$SCRIPT_DIR/main.py" \
  >"$SCRIPT_DIR/narc.log" 2>&1 </dev/null &

echo $! >"$PID_FILE"
echo "Hydration Narc started (PID $!). Log: $SCRIPT_DIR/narc.log"
