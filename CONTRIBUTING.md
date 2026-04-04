# Contributing to The Hydration Narc

Thank you for your interest in making someone's day significantly worse.

The Hydration Narc is built on a shared belief: people will not drink water unless a Python script makes their life genuinely unpleasant. If you share this belief, you belong here.

---

## Ground rules

1. **Contributions should match the product's tone** — Daniel is calm, certain, disappointed. No "mercy" features that gut the premise without discussion.
2. **Reversible by design where possible** — the intended escape is **sip + smile** (full compliance), not a hidden killswitch in the UI.
3. **Keep the stack minimal** — Python, shell, AppleScript, optional `sounds/*.mp3`. No marketing site in this repo.

---

## Where logic lives

| Area | File | Notes |
|------|------|--------|
| Threat actions | `actions.py` | `say`, Slack, hide apps, sleep, Rickroll |
| Health / decay / nuclear | `narc.py` | `HealthScore`, sip detector, MediaPipe loop |
| Ledger | `ledger.py` | Append-only JSON, threaded writes |

To add a consequence at a given score, extend **`HealthScore`** in `narc.py` (e.g. in `_on_decay_level` or the `score == 0` block) and implement the side effect in **`actions.py`**. Use **non-blocking** calls (threads or detached processes) so the camera loop stays responsive.

---

## Voice line guidelines

- Daniel does not shout. Disappointment is quieter than anger.
- Good: *"You have made a series of poor choices."*
- Bad: *"DRINK WATER NOW!!!"*

---

## Testing locally

There is no formal test suite. To stress thresholds without waiting ~50 minutes, temporarily lower **`DECAY_INTERVAL_SEC`** and raise **`DECAY_AMOUNT`** in `narc.py`. **Revert before opening a PR.**

```bash
uv sync
uv run python narc.py   # foreground; press q to quit
```

---

## Code style

- Type-annotated signatures where it helps.
- Side effects that touch the network, disk, or shell should not block the main CV loop.
- Prefer small, explicit functions over frameworks.

---

## Pull requests

Use a title that describes the **behavior**, not the plumbing.

- Good: `feat: foghorn at health ≤ 40 via sounds/foghorn.mp3`
- Bad: `feat: add subprocess wrapper`

Maintainers will try the change on macOS before merging.

Welcome to the team.
