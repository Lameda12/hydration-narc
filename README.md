# The Hydration Narc™
### *Drink water. Smile about it. Or face consequences.*

<video src="media/narc_trailer.mp4" controls width="100%"></video>

> **IMPORTANT LEGAL NOTICE:** By running `start.sh`, you acknowledge that you have read, understood, and emotionally accepted this document. The Hydration Narc™ is not responsible for lost productivity, dimmed screens, hidden Spotify sessions, involuntary rickrolls, or the slow erosion of your sense of personal autonomy. Hydration is non-negotiable. Happiness is now also non-negotiable.

---

## The Manifesto

The trailer above was built using **[Remotion](https://remotion.dev)** — a framework for creating videos programmatically in React — in a single session of what the industry is calling "Vibe Coding."

No timeline editor was opened. No keyframes were dragged. The entire 30-second production — five scenes, a cracking health bar, an animated Mortal Sins registry, a nuclear failure sequence, and four voice lines recorded live from the macOS `say` command — was written as TypeScript and rendered to MP4 at the command line.

The voiceover is Daniel. It is always Daniel.

**The stack:**
- `Remotion 4` — composition, sequencing, interpolation
- `MediaPipe Face Mesh` — smile detection (the Narc watches the trailer too)
- `macOS say -v Daniel` — voice synthesis, converted to MP3 via `ffmpeg`
- `<Sequence from={N}>` — frame-accurate audio placement
- `osascript` — everything else

The trailer was vibe coded. The Narc was not. The Narc was built with intent, conviction, and a specific contempt for people who don't drink enough water.

---

## What Is This

A macOS webcam utility that watches you through your own camera, judges you in real time, and escalates its response to your negligence using a graduated system of psychological, auditory, and computational punishment.

It uses your face against you. Specifically, your mouth.

---

## Threat Level Chart

*The following table constitutes the full and binding behavioral contract between you ("the User," "the Raisin," "the Accused") and the Hydration Narc™ ("the Narc," "Daniel," "your last warning").*

| Health Score | Threat Level | What Happens | Escape Route |
|---|---|---|---|
| **100** | 🟢 **Compliant** | Nothing. You are a good person. | Keep drinking. |
| **≤ 75** | 🟡 **Observed** | Daniel clears his throat audibly. *"I see you getting thirsty. Don't make me dim the lights."* | Drink something. |
| **≤ 60** | 🟠 **Punished** | Screen dims to 20%. Mouse begins to spasm. Daniel insults your discipline using one of five (5) curated affronts. Repeats. | Drink and smile. |
| **≤ 30** | 🔴 **Hostage Situation** | Your frontmost application — specifically Spotify, Discord, or YouTube — is hidden without warning. Daniel says *"No music for raisins. Drink up."* He means it. | Drink and smile. |
| **= 0** | ☢️ **Social Consequences** | A webhook fires to your designated Slack channel announcing your dehydration to colleagues. Daniel says *"I'm telling your coworkers you're dying of thirst. Goodnight."* | You cannot undo this. |
| **0 for 60s** | 💀 **Nuclear** | The machine sleeps. Not you. The machine. You are now sitting in front of a black screen. | Contemplate your choices. |
| **Wake + 30s, no sip** | 🎵 **The Finale** | Rick Astley opens in your browser at full system volume. This is not a threat. This already happened. | There is no escape route for this one. |

---

## The Vibe Check Clause

*Section 4(b) of the Hydration Narc™ Terms of Emotional Compliance*

Effective immediately, **a sip alone is no longer sufficient.**

The Narc employs MediaPipe Face Mesh landmark analysis to measure the ratio of your mouth-corner spread to your face width at the moment of drinking. If this ratio meets or exceeds the Smile Threshold (currently `0.28`), your sip is recognized as a **Full Compliance Event** and your Health Score resets to 100.

If you drink while looking like you'd rather be anywhere else:

- Your Health Score recovers only to **50%**
- Daniel will say: *"You look miserable. Smile while you drink or it doesn't count."*
- The Narc logs this internally as a **Grumpy Sip™** and judges you accordingly

**The Narc does not want your hydration. It wants your joy.**

---

## App Hostage Protocol

*Section 7(a): Collateral Entertainment Seizure*

When your Health Score drops below 30, the Narc audits your current focused application. If it is one of the following:

- **Spotify** — your music
- **Discord** — your friends
- **YouTube** — your videos

...it will be hidden. Not closed. Hidden. It will still be running. You will just be unable to access it. Daniel will explain why.

The Narc considers this proportionate.

---

## Setup

```bash
# Install dependencies
uv sync

# Start the Narc (detached, persistent, cannot be Ctrl+C'd)
./start.sh

# Stop the Narc (if you can bring yourself to do it)
./stop.sh
```

Configure your Slack webhook in `actions.py → social_shame()` before first run. Failure to do so means the social shaming will silently fail, and you will have only yourself to blame.

---

## Health Decay Rate

Health drops **2 points every 60 seconds**. Full drain takes **50 minutes**. This is intentional. You have been warned at the 37-minute mark, the 30-minute mark, and every subsequent minute until the machine sleeps.

---

## Frequently Asked Questions

**Q: Can I just close the window?**
A: `start.sh` launches the Narc with `nohup`. Closing the terminal does nothing. The Narc persists.

**Q: Can I kill the process?**
A: Yes. `./stop.sh`. Daniel will call you a coward. The script agrees.

**Q: What if I'm genuinely smiling but the Narc doesn't recognize it?**
A: Smile bigger. The threshold is `0.28`. You know what you did.

**Q: Is this GDPR compliant?**
A: The Narc processes your facial geometry locally, in memory, in real time, and discards it immediately. It does not store your face. It simply *watches* your face. Continuously. With judgment.

**Q: What if I'm lactose intolerant / fasting / doing a juice cleanse?**
A: Water. The answer is always water.

---

*The Hydration Narc™ is a personal project. Any resemblance to actual corporate wellness software is coincidental and deeply concerning.*
