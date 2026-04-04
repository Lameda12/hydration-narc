"""Persistent JSON settings store for Hydration Narc tuning parameters."""

from __future__ import annotations

import json
import threading
from pathlib import Path

# Default tuning parameters (mirrors narc.py constants).
DEFAULTS: dict = {
    "DECAY_INTERVAL_SEC": 60,
    "DECAY_AMOUNT": 2,
    "SIP_HOLD_TIME": 1.5,
    "SIP_THRESHOLD": 0.12,
    "SMILE_THRESHOLD": 0.28,
    "NUCLEAR_DELAY_SEC": 60,
    "WAKE_GAP_SEC": 15.0,
    "THREAT_OBSERVED": 75,
    "THREAT_HOSTAGE": 30,
    "DAILY_WATER_GOAL_SIPS": 8,
}

# Settings file: ~/Library/Application Support/HydrationNarc/settings.json
_SETTINGS_DIR = Path.home() / "Library" / "Application Support" / "HydrationNarc"
SETTINGS_PATH = _SETTINGS_DIR / "settings.json"


class SettingsStore:
    """Thread-safe persistent settings store."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._settings: dict = DEFAULTS.copy()

    def load(self) -> None:
        """Load settings from file, merging with defaults for missing keys."""
        with self._lock:
            if SETTINGS_PATH.is_file():
                try:
                    with open(SETTINGS_PATH) as f:
                        loaded = json.load(f)
                    # Merge: loaded + missing defaults
                    for key, default_val in DEFAULTS.items():
                        if key in loaded:
                            self._settings[key] = loaded[key]
                except Exception:
                    pass  # Fall back to defaults

    def save(self) -> None:
        """Write current settings to file."""
        with self._lock:
            _SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
            with open(SETTINGS_PATH, "w") as f:
                json.dump(self._settings, f, indent=2)

    def get(self, key: str) -> float | int | str | bool:
        """Thread-safe read of a single setting."""
        with self._lock:
            return self._settings.get(key, DEFAULTS.get(key))

    def set(self, key: str, value: float | int | str | bool) -> None:
        """Thread-safe write of a single setting + persist to file."""
        with self._lock:
            self._settings[key] = value
        self.save()

    def get_all(self) -> dict:
        """Return a shallow copy of all settings."""
        with self._lock:
            return self._settings.copy()
