# 🚀 START HERE — How to Run Hydration Narc v2

## Step 1: Open Terminal

Open **Terminal.app** (or any terminal you prefer)

## Step 2: Navigate to Project

```bash
cd /Users/amadi/Summer26/hydration-narc
```

## Step 3: Run the App

```bash
python main.py
```

**You should see:** App starts silently (no output in terminal)

## Step 4: Look for Menu Bar Icon

Look at the **top right corner of your screen** in the menu bar.

You should see: **💧100**

(It's a water droplet with the number 100 — your health score)

## Step 5: Click the Icon

Click **💧100** in the menu bar → **Dropdown menu appears**

## Menu Structure

```
📊 STATUS
  💧 Health: 100 🟢
  💦 Water: 0/8 sips ░░░░░░░░░░ 0%
  🥤 Sips today: 0 (0 ✓) ⚠️
  ⏰ Last sip: never

📷 CAMERA
  👁️ Open Live Preview        ← Click here to see camera
  👤 Face: detecting ✓
  😊 Smile: 0.00 / 0.28 ✗
  👆 Hand: away ✗

⚙️ Settings
▶️ Pause monitoring
❓ How to Use
❌ Quit Hydration Narc
```

## Step 6: Test Camera Preview

1. Click **👁️ Open Live Preview**
2. A small window (240×180) should pop up showing your camera
3. Move around — you should see yourself in the window
4. Close the window anytime (app keeps running)

## Step 7: Test Audio & Water Tracking

1. **Smile at the camera** with your hand near your mouth
2. **Hold for ~1.5 seconds** (sip detection window)
3. Should hear: **✅ Celebration sound!** (sip_success.mp3)
4. Menu bar should update: **💦 Water: 1/8 sips**

## Step 8: Check Documentation

Open the `sounds/` folder:
- **README.txt** — Audio trigger guide with emojis
- All 6 MP3 files are there

Or read:
- **QUICKSTART.md** — Full user guide
- **CHANGELOG.md** — What's new in v2

## ❌ To Stop the App

Press `Ctrl + C` in the terminal where it's running.

Or:
1. Click menu bar icon
2. Click **❌ Quit Hydration Narc**

---

## 🎯 What Should Happen

| Action | Result |
|--------|--------|
| Run `python main.py` | App starts silently |
| Look at menu bar | See 💧100 icon (top right) |
| Click icon | Dropdown menu with stats appears |
| Click "Open Live Preview" | Camera window pops up |
| Smile + hand near mouth | Hear celebration sound + water count increases |
| Wait 60 seconds | Health score decreases |
| Health hits 75 | Hear "observed" warning sound |

---

## 🐛 If Menu Bar Icon Doesn't Appear

1. **Check terminal** — Is the app still running?
   ```bash
   ps aux | grep "python main.py" | grep -v grep
   ```

2. **Try clicking top menu bar** — Sometimes the icon is tiny, look carefully

3. **Check System Preferences** → Dock & Menu Bar → App might be hidden

4. **Restart the app:**
   ```bash
   pkill -f "python main.py"
   sleep 2
   python main.py
   ```

---

## 🎵 Audio Files

All 6 sounds are already in `sounds/` folder:
- ✅ sip_success.mp3 (celebration)
- ✅ sip_fail.mp3 (disappointment)
- ✅ observed.mp3 (warning)
- ✅ hostage.mp3 (threatening)
- ✅ shame_zero.mp3 (shame)
- ✅ rickroll.mp3 (wake from sleep)

No setup needed — they play automatically!

---

## 📚 Documentation

- **START_HERE.md** ← You are here
- **QUICKSTART.md** — Complete beginner guide
- **CHANGELOG.md** — Version history & features
- **sounds/README.txt** — Audio guide with emoji triggers

---

Enjoy! 💧✨

**Questions?** Check QUICKSTART.md or sounds/README.txt
