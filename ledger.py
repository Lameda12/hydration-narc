"""Append-only JSON ledger for sips and mortal sins."""

import json
import os
import threading
from datetime import datetime, timezone

_LEDGER_PATH = os.path.join(os.path.dirname(__file__), "ledger.json")
_lock = threading.Lock()


def _load() -> list:
    if not os.path.exists(_LEDGER_PATH):
        return []
    with open(_LEDGER_PATH) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _append(entry: dict) -> None:
    def _write() -> None:
        with _lock:
            records = _load()
            records.append(entry)
            with open(_LEDGER_PATH, "w") as f:
                json.dump(records, f, indent=2)

    threading.Thread(target=_write, daemon=True).start()


def log_sip(smile_intensity: float, full_compliance: bool) -> None:
    _append(
        {
            "event": "sip",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "smile_intensity": round(smile_intensity, 4),
            "full_compliance": full_compliance,
        }
    )


def log_mortal_sin() -> None:
    _append(
        {
            "event": "mortal_sin",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "note": "Nuclear sleep invoked.",
        }
    )
