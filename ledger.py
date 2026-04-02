"""The Hydration Ledger — a permanent record of your sins and virtues."""

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
    def _write():
        with _lock:
            records = _load()
            records.append(entry)
            with open(_LEDGER_PATH, "w") as f:
                json.dump(records, f, indent=2)
    threading.Thread(target=_write, daemon=True).start()


def log_sip(smile_intensity: float, full_recovery: bool) -> None:
    """Record a sip event with its smile intensity."""
    _append({
        "event":          "sip",
        "timestamp":      datetime.now(timezone.utc).isoformat(),
        "smile_intensity": round(smile_intensity, 4),
        "full_recovery":  full_recovery,
    })


def log_mortal_sin() -> None:
    """Record a nuclear penalty (sleep) as a Mortal Sin."""
    _append({
        "event":     "mortal_sin",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "note":      "Machine put to sleep. You had every opportunity.",
    })
