"""Punishment actions for the Hydration Narc."""

import os
import subprocess
import random
import threading
import pyautogui
from pynput import keyboard as _kb

pyautogui.FAILSAFE = True


def dim_screen(brightness: float = 0.3) -> None:
    """Dim the screen via osascript. brightness is 0.0–1.0."""
    value = int(brightness * 100)
    script = f'tell application "System Events" to set brightness of display 1 to {value}'
    subprocess.run(["osascript", "-e", script], check=False)


def restore_screen(brightness: float = 0.8) -> None:
    """Restore screen brightness."""
    value = int(brightness * 100)
    script = f'tell application "System Events" to set brightness of display 1 to {value}'
    subprocess.run(["osascript", "-e", script], check=False)


def shame_user(message: str) -> None:
    """Speak a shame message via macOS TTS in a background thread."""
    # Sanitize: strip quotes so the shell interpolation can't be broken
    safe = message.replace('"', "").replace("'", "")
    threading.Thread(
        target=lambda: os.system(f'say -v "Daniel" "{safe}"'),
        daemon=True,
    ).start()


def nuclear_penalty() -> None:
    """Put the machine to sleep via osascript."""
    os.system("osascript -e 'tell application \"System Events\" to sleep'")


def social_shame(webhook_url: str = "https://hooks.slack.com/services/PLACEHOLDER") -> None:
    """POST a dehydration alert to a webhook (e.g. Slack incoming webhook)."""
    import json
    import urllib.request

    payload = json.dumps({
        "text": (
            "\U0001f6a8 DEHYDRATION ALERT: [User] has ignored me for 10 minutes. "
            "They are officially a raisin."
        )
    }).encode()

    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    threading.Thread(
        target=lambda: urllib.request.urlopen(req, timeout=10),
        daemon=True,
    ).start()


_HOSTAGE_APPS = {"Spotify", "Discord", "YouTube"}

# ── Keyboard lockdown ─────────────────────────────────────────────────────────
_kb_listener: _kb.Listener | None = None
_kb_lock = threading.Lock()


def lock_keyboard() -> None:
    """Suppress all keyboard input until unlock_keyboard() is called."""
    global _kb_listener
    with _kb_lock:
        if _kb_listener is not None:
            return  # already locked
        shame_user(
            "Your words are worthless. Only water matters now. Keyboard privileges revoked."
        )
        _kb_listener = _kb.Listener(
            suppress=True,
            on_press=lambda key: None,
            on_release=lambda key: None,
        )
        _kb_listener.start()


def unlock_keyboard() -> None:
    """Restore keyboard input."""
    global _kb_listener
    with _kb_lock:
        if _kb_listener is None:
            return
        _kb_listener.stop()
        _kb_listener = None


def take_hostage(health_score: int) -> None:
    """Hide a fun app if health is critically low."""
    if health_score >= 30:
        return
    get_app = (
        'tell application "System Events" to get name of first process '
        'whose frontmost is true'
    )
    result = subprocess.run(
        ["osascript", "-e", get_app], capture_output=True, text=True
    )
    app = result.stdout.strip()
    if app in _HOSTAGE_APPS:
        subprocess.run(
            ["osascript", "-e", f'tell application "{app}" to set visible to false'],
            check=False,
        )
        shame_user("No music for raisins. Drink up.")


def post_to_x(message: str) -> None:
    """Open a browser to x.com/intent/tweet so the user must manually post their confession."""
    import urllib.parse
    url = "https://x.com/intent/tweet?text=" + urllib.parse.quote(message)
    os.system(f"open '{url}'")


def mouse_jitter(iterations: int = 5, magnitude: int = 40) -> None:
    """Rapidly jitter the mouse cursor to annoy the user."""
    x, y = pyautogui.position()
    for _ in range(iterations):
        dx = random.randint(-magnitude, magnitude)
        dy = random.randint(-magnitude, magnitude)
        pyautogui.moveTo(x + dx, y + dy, duration=0.05)
    pyautogui.moveTo(x, y, duration=0.1)
