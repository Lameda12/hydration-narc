# Contributing to The Hydration Narc

Thank you for your interest in making someone's day significantly worse.

The Hydration Narc is a community project built on a shared belief: that people will not drink water unless a Python script makes their life genuinely unpleasant. If you share this belief, you belong here.

---

## Ground Rules

1. **All contributions must make the experience worse for the user, not better.** PRs that add a "snooze" button, a grace period, or any form of mercy will be closed without comment.
2. **The Narc's tone is non-negotiable.** Daniel is disappointed. Daniel is always disappointed.
3. **All new punishments must be reversible by a Smile + Sip.** We are sadists, not monsters.

---

## How to Add More Pain

This is the section you came for.

The punishment pipeline lives in `actions.py`. Adding a new punishment is straightforward:

1. Write a function in `actions.py`
2. Import and call it from `HealthScore.apply_punishment()` in `narc.py` at the appropriate threshold
3. Add a corresponding voice line via `shame_user()` if the action benefits from narration (it does)
4. Update the Threat Level Chart in `README.md`

### Approved punishment ideas (seeking PRs)

| Idea | Trigger Threshold | Notes |
|------|------------------|-------|
| **Change desktop wallpaper to a raisin** | score ≤ 20 | Use `osascript` to set `desktopPicture`. Restore on sip. |
| **Close the frontmost Chrome tab** | score ≤ 25 | AppleScript: `tell app "Google Chrome" to close active tab of front window` |
| **Invert display colors** | score ≤ 10 | `osascript -e 'tell app "System Events" to key code 8 using {command down, option down, control down}'` |
| **Set system volume to max, play a foghorn** | score ≤ 30 | `afplay` a local sound at volume 10. Restore after. |
| **Email a "hydration incident report" to yourself** | mortal sin | SMTP via `smtplib`. Configurable recipient. |
| **Change Slack status to "💀 Dehydrated and Struggling"** | score ≤ 40 | Slack API. Revert on sip. |
| **Type "DRINK WATER" into the active text field** | score ≤ 15 | `pynput` keyboard controller. |
| **Move all desktop icons into a folder called "Shame"** | nuclear | AppleScript + Finder. Restore on full recovery. |

### Punishment function template

```python
def your_punishment() -> None:
    """One-line description of the misery inflicted."""
    # do the thing
    shame_user("A contextually appropriate insult.")
```

### Voice line guidelines

- Daniel does not shout. Daniel is **calm** and **certain**.
- Avoid exclamation marks. Disappointment is quieter than anger.
- Good: *"You have made a series of poor choices."*
- Bad: *"DRINK WATER NOW!!!"*

---

## Adding to the Ledger

If your punishment represents a new category of sin, add a new `log_*` function to `ledger.py` following the existing pattern. All ledger writes must be non-blocking (daemon thread).

---

## Shame Report Extensions

`shame_report.py` calculates the Purity Score. If you add a new sin category, update:
- `_tally()` to count it
- `purity_score()` if the sin warrants a point penalty
- `generate_confession()` to reference it in the output tweet

---

## Testing

There is no test suite. The Narc tests you.

If you want to verify a punishment without waiting 50 minutes for health to decay, temporarily lower `DECAY_INTERVAL` to `5` and `DECAY_AMOUNT` to `20` in `narc.py`. Revert before committing.

---

## Code Style

- Minimal. No abstractions for one-time operations.
- Type-annotated function signatures.
- Non-blocking side effects (threading or shell `&`) to keep the camera loop at full frame rate.
- Comments only where the logic isn't obvious from the code.

---

## Submitting

Open a PR with a title that describes the punishment, not the implementation.

Good title: `feat: close active Chrome tab at score ≤ 25`
Bad title: `feat: added new AppleScript integration for browser tab management`

The Narc's maintainers will review your contribution, test it on themselves, and merge it if it causes sufficient discomfort.

Welcome to the team.
