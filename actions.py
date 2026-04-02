"""Punishment actions for the Hydration Narc."""

import os
import subprocess
import random
import threading
import pyautogui

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


def mouse_jitter(iterations: int = 5, magnitude: int = 40) -> None:
    """Rapidly jitter the mouse cursor to annoy the user."""
    x, y = pyautogui.position()
    for _ in range(iterations):
        dx = random.randint(-magnitude, magnitude)
        dy = random.randint(-magnitude, magnitude)
        pyautogui.moveTo(x + dx, y + dy, duration=0.05)
    pyautogui.moveTo(x, y, duration=0.1)
