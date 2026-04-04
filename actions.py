"""Threat automation for Hydration Narc — TTS, AppleScript, Slack, and finale."""

from __future__ import annotations

import json
import os
import subprocess
import threading
import urllib.request
from pathlib import Path

# Set via env or edit for your Slack incoming webhook.
SLACK_WEBHOOK_URL = os.environ.get(
    "HYDRATION_NARC_SLACK_WEBHOOK",
    "https://hooks.slack.com/services/PLACEHOLDER",
)

_REPO_ROOT = Path(__file__).resolve().parent
SOUNDS_DIR = _REPO_ROOT / "sounds"

_RICKROLL_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Track running sound processes per slot to prevent audio stacking
_sound_procs: dict[str, subprocess.Popen] = {}


def _run_applescript(source: str) -> None:
    subprocess.run(["osascript", "-e", source], check=False, capture_output=True)


def play_sound_if_exists(filename: str, slot: str | None = None) -> None:
    """Play an MP3 from ./sounds if present (non-blocking, deduplicated by slot)."""
    path = SOUNDS_DIR / filename
    if not path.is_file():
        return

    key = slot or filename
    prev = _sound_procs.get(key)
    if prev and prev.poll() is None:
        # Previous process for this slot still running, skip to avoid stacking
        return

    def _play() -> None:
        proc = subprocess.Popen(["afplay", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _sound_procs[key] = proc

    threading.Thread(target=_play, daemon=True).start()


def hide_hostage_apps() -> None:
    """Level 30 — hide Spotify, Discord, and YouTube via AppleScript."""
    for app in ("Spotify", "Discord", "YouTube"):
        _run_applescript(
            f'tell application "{app}" to if running then set visible to false'
        )


def post_drought_slack(webhook_url: str | None = None) -> None:
    """Level 0 — post drought / dehydration alert to Slack."""
    url = webhook_url or SLACK_WEBHOOK_URL
    if "PLACEHOLDER" in url:
        return

    payload = json.dumps(
        {
            "text": (
                "DEHYDRATION ALERT: The Narc reports critical drought. "
                "The subject has hit health 0. Hydrate immediately."
            )
        }
    ).encode()

    def _post() -> None:
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=10)
        except OSError:
            pass

    threading.Thread(target=_post, daemon=True).start()


def nuclear_sleep() -> None:
    """Put the Mac to sleep (System Events)."""
    _run_applescript('tell application "System Events" to sleep')


def rickroll_full_volume() -> None:
    """Finale — system volume max, then Rickroll (file or browser)."""
    _run_applescript("set volume output volume 100")
    rick = SOUNDS_DIR / "rickroll.mp3"
    if rick.is_file():
        play_sound_if_exists("rickroll.mp3", slot="rickroll")
    else:
        subprocess.Popen(
            ["open", _RICKROLL_URL],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
