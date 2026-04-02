#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.narc.pid"
LEDGER="$SCRIPT_DIR/ledger.json"

# ── Mortal Sin gate ───────────────────────────────────────────────────────────
if [[ -f "$LEDGER" ]]; then
    TODAY="$(date -u +%Y-%m-%d)"
    SINS="$(python3 - <<EOF
import json, sys
with open("$LEDGER") as f:
    records = json.load(f)
count = sum(
    1 for r in records
    if r.get("event") == "mortal_sin" and r.get("timestamp", "").startswith("$TODAY")
)
print(count)
EOF
)"
    if [[ "$SINS" -gt 3 ]]; then
        echo "You haven't earned the right to stop. Keep drinking."
        echo "(${SINS} Mortal Sins today. The threshold is 3. You need kill -9 if you're desperate.)"
        exit 1
    fi
fi

# ── Normal shutdown ───────────────────────────────────────────────────────────
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
