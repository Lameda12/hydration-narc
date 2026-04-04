# The Hydration Narc™

### *Drink water. Smile about it. Or face consequences.*

<p align="center">
  <video src="https://hydration-narc.vercel.app/narc_trailer.mp4" controls width="100%"></video>
</p>

<p align="center"><em>If the clip does not load, open the <a href="https://hydration-narc.vercel.app">live site</a>.</em></p>

> **IMPORTANT LEGAL NOTICE:** By running `start.sh`, you acknowledge that you have read, understood, and emotionally accepted this document. The Hydration Narc™ is not responsible for lost productivity, hidden Spotify sessions, involuntary rickrolls, or the slow erosion of your sense of personal autonomy. Hydration is non-negotiable. Happiness is now also non-negotiable.

---

## What this is

A **macOS** utility that uses your **webcam**, **MediaPipe** face and hand landmarks, and a **health score** that decays over time. A drink only counts as **full compliance** when you **smile enough** at the moment of the sip (mouth spread ÷ face width **≥ 0.28**). Otherwise Daniel explains the error of your ways and nothing resets.

This repository is the **Python daemon** only. The landing page and trailer live elsewhere (e.g. Vercel).

---

## Threat level chart

| Health | Level | What happens |
|--------|--------|----------------|
| **100** | Compliant | Peace. |
| **≤ 75** | Observed | Daniel speaks (`say -v Daniel`). Optional `sounds/observed.mp3`. |
| **≤ 30** | Hostage | AppleScript hides **Spotify**, **Discord**, and **YouTube** if they are running. Optional `sounds/hostage.mp3`. |
| **= 0** | Social shame | Drought post to your **Slack incoming webhook** (`actions.py` / `HYDRATION_NARC_SLACK_WEBHOOK`). Optional `sounds/shame_zero.mp3`. |
| **0 for 60s** | Nuclear | Machine sleeps. |
| **After wake** | Finale | System volume max, then **`sounds/rickroll.mp3`** if present, else the Rickroll URL opens. |

---

## The vibe check (sip + smile)

**A sip alone is not enough.** You must hold a sip pose long enough, **and** meet the smile threshold, to reset health to **100**. Below threshold, you get a voice line and a ledger entry — **no** health reset.

---

## Setup

```bash
uv sync
./start.sh    # background: nohup + uv run python narc.py → narc.log, .narc.pid
./stop.sh     # respects mortal-sin tally; see script
```

1. Set your Slack webhook: environment variable **`HYDRATION_NARC_SLACK_WEBHOOK`**, or edit **`SLACK_WEBHOOK_URL`** in `actions.py`. Placeholder URLs skip Slack quietly.
2. Optional MP3s: drop files listed in `sounds/README.txt`.
3. First run downloads MediaPipe `.task` models to `~/Library/Caches/HydrationNarc/`.

---

## Parameters

| Constant | Value |
|----------|--------|
| Decay | **−2** every **60** seconds |
| Smile threshold **S** | **0.28** |
| Sip hold | **1.5** s near mouth |
| Nuclear delay at 0 | **60** s before sleep |

---

## Trailer manifesto (short)

The trailer was built with **[Remotion](https://remotion.dev)** — compositions in TypeScript, rendered to MP4. Voiceover is **Daniel** (`say -v Daniel`, then ffmpeg). The **daemon** in this repo is separate: **Python**, **OpenCV**, **MediaPipe Tasks** (face + hand landmark models), **`osascript`**, **`say`**, and your **webhook**.

The trailer was vibe-coded. The Narc was built with intent.

---

## FAQ

**Close the camera window?** With `start.sh`, the process keeps running until `./stop.sh` (or you kill the PID).

**GDPR?** Landmarks are processed locally in memory for inference; this app does not upload your face.

**Water only?** Water.

---

*The Hydration Narc™ is a personal project. Any resemblance to corporate wellness software is coincidental and deeply concerning.*
