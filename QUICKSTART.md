# 💧 Hydration Narc — Quick Start Guide

## What is this?
**Hydration Narc** is a macOS menu bar app that tracks your water intake using your camera. It detects when you drink water and gives you sassy audio feedback.

---

## 🚀 Getting Started (3 steps)

### 1️⃣ **Run the App**
```bash
python main.py
```
You'll see a water droplet **💧** in your menu bar (top right).

### 2️⃣ **Click the Menu Bar Icon**
Opens a dropdown showing:
- 📊 **STATUS** — Your health score, water intake, last sip time
- 📷 **CAMERA** — Live preview + detection status (face, smile, hand)
- ⚙️ **SETTINGS** — Tune detection thresholds
- ❓ **HOW TO USE** — Quick instructions

### 3️⃣ **Take a Sip & Get Feedback**
- Hold a glass near your mouth
- Smile at the camera
- App detects and plays audio: **✅ Celebration sound!**
- Your water count increments: `💦 Water: 1/8 sips`

---

## 📊 What You'll See

### Menu Bar Status
```
💧100          ← Health score (100 = full, 0 = locked)
```

### Dropdown Menu Layout
```
📊 STATUS
  💧 Health: 100 🟢
  💦 Water: 0/8 sips ░░░░░░░░░░ 0%
  🥤 Sips today: 0 (0 ✓) ⚠️
  ⏰ Last sip: never

📷 CAMERA
  👁️ Open Live Preview        ← Click to see live feed
  👤 Face: detecting ✓
  😊 Smile: 0.00 / 0.28 ✗
  👆 Hand: away ✗

⚙️ Settings
  (10 tuning parameters)

▶️ Pause monitoring
❓ How to Use
❌ Quit Hydration Narc
```

---

## 🎯 How Detection Works

| Action | Detection | Audio | Result |
|--------|-----------|-------|--------|
| **Drink + Smile** ✅ | Hand near mouth + Smile detected | sip_success.mp3 | Health = 100 |
| **Drink NO Smile** ❌ | Hand near mouth + NO Smile | sip_fail.mp3 | Sip logged (no health gain) |
| **Idle 60+ seconds** | Health decays | (nothing yet) | Health goes down |
| **Health ≤ 75** ⚠️ | Once | observed.mp3 | "I see you!" |
| **Health ≤ 30** 🔒 | Once | hostage.mp3 | Apps hide, ominous warning |
| **Health = 0** 💀 | Once | shame_zero.mp3 | 60s until forced sleep |
| **Wake from sleep** | System wakes | rickroll.mp3 | 😏 Rickroll |

---

## 🎤 Audio & Customization

### Default Sounds Included
- ✅ **sip_success.mp3** — celebratory cheer
- ❌ **sip_fail.mp3** — sassy disappointment
- ⚠️ **observed.mp3** — judgmental gasp
- 🔒 **hostage.mp3** — menacing warning
- 💀 **shame_zero.mp3** — dramatic failure
- 🎵 **rickroll.mp3** — Never Gonna Give You Up

### Add Custom Audio
1. Find clips from [Voicemod Tuna](https://tuna.voicemod.net/sounds/) or YouTube
2. Convert to MP3 (use ffmpeg or online converter)
3. Rename to match: `sip_success.mp3`, `observed.mp3`, etc.
4. Drop into `sounds/` folder
5. Restart app — custom audio plays!

See `sounds/README.txt` for details.

---

## 🎮 Camera Preview

Click **👁️ Open Live Preview** to see what the camera detects:

- Live 240×180 floating window
- Updates 10 times per second
- Shows what's being analyzed
- Debug detection issues (smile threshold too high? face not detected?)
- Close anytime, reopen from menu

---

## ⚙️ Settings (Tuning)

In menu → Settings, you can adjust:

| Setting | Purpose | Default |
|---------|---------|---------|
| **Decay interval** | How often health goes down | 60s |
| **Decay amount** | How much health lost per interval | 2 points |
| **Sip threshold** | How close hand must be to mouth | 0.12 |
| **Smile threshold** | How much to smile to count as "smile" | 0.28 |
| **Nuclear delay** | Time before forced sleep | 60s |
| **Warn at** | Health score triggers warning | 75 |
| **Hostage at** | Health score hides apps | 30 |
| **Daily water goal** | Target sips per day | 8 |

**Typical tuning:**
- Smile too easily detected? → Increase **Smile threshold** to 0.35+
- Won't detect smile? → Decrease to 0.20
- Hand detection off? → Adjust **Sip threshold**

Open **👁️ Live Preview** while tuning to see the numbers in real-time.

---

## 📱 Health System

Your **Health Score** (0–100) represents hydration status:

```
100         🟢 Perfect — fully compliant
75–99       🟢 Good — sipped recently
50–74       🟡 Okay — needs a drink soon
30–49       🟡 Bad — apps hide when ≤30
1–29        🔴 Critical — warning sounds
0           💀 Locked — forced sleep for 60s
```

Health decays every 60 seconds by default. Taking a compliant sip (with smile) resets it to 100.

---

## 🛑 Pause / Resume

Click **▶️ Pause monitoring** to stop tracking. Menu bar shows **⏸** instead of 💧.

Click **Resume monitoring** to restart without closing the app.

---

## ❌ Quit

Click **❌ Quit Hydration Narc** to close the app completely.

---

## 🐛 Troubleshooting

**No audio playing?**
- Check `sounds/` folder — audio files must be present
- Open Live Preview to confirm camera is detecting
- Check system volume isn't muted

**Camera not detecting?**
- Click **👁️ Open Live Preview** — see if camera works
- Check lighting — MediaPipe needs decent brightness
- Verify face is centered in frame

**Smile never detected?**
- Smile threshold too high — lower in Settings
- Try a bigger smile
- Check lighting

**Hand detection off?**
- Get closer to camera
- Increase hand visibility
- Check Settings → Sip threshold

---

## 📖 More Info

- Full audio guide: See `sounds/README.txt`
- Architecture: See `README.md` (if available)
- Report bugs: Open GitHub issue

Enjoy tracking hydration! 💧✨
