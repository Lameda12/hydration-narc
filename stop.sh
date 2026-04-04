#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.narc.pid"
LEDGER="$SCRIPT_DIR/ledger.json"

if [[ -f "$LEDGER" ]]; then
  TODAY="$(date -u +%Y-%m-%d)"
  SINS="$(python3 - <<EOF
import json
with open("$LEDGER") as f:
    records = json.load(f)
count = sum(
    1 for r in records
    if r.get("event") == "mortal_sin" and r.get("timestamp", "").startswith("$TODAY")
)
print(count)
EOF
)"
  if [[ "${SINS:-0}" -gt 3 ]]; then
    echo "You have not earned the right to stop. (${SINS} mortal sins today; threshold is 3.)"
    exit 1
  fi
fi

if [[ ! -f "$PID_FILE" ]]; then
  echo "No PID file. Is Hydration Narc running?"
  exit 1
fi

PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  rm "$PID_FILE"
  echo "Hydration Narc stopped (PID $PID)."
else
  echo "Process $PID not running; removing stale PID file."
  rm "$PID_FILE"
fi
