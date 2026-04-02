#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.narc.pid"

if [[ ! -f "$PID_FILE" ]]; then
    echo "No PID file found. Is the Narc running?"
    exit 1
fi

PID="$(cat "$PID_FILE")"

if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    rm "$PID_FILE"
    echo "Narc stopped (PID $PID). Coward."
else
    echo "Narc (PID $PID) was not running. Cleaning up."
    rm "$PID_FILE"
fi
