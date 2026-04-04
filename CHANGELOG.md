# 📝 Hydration Narc — Changelog

## Version 2.0 — April 4, 2026

### ✨ New Features

#### 1. 📷 **Live Camera Preview Window**
- Click "👁️ Open Live Preview" in menu bar to see what camera detects
- 240×180 floating window, always-on-top
- Updates 10 times per second
- Perfect for debugging smile/hand detection
- Can open/close without restarting app

#### 2. 💦 **Daily Water Tracking**
- New menu stat: "💦 Water: X/8 sips" with visual progress bar
- Percentage shown: ████░░░░ format
- Tracks sips throughout the day
- Resets at midnight UTC
- Customizable daily goal (default: 8 sips)

#### 3. 🎵 **Fixed Audio System**
- All 6 audio triggers working correctly (no double-plays)
- Audio deduplication prevents stacking/overlapping
- Graceful fallback if MP3 files missing (silent mode)
- No more robot TTS ("say -v Daniel")

### 🎨 **UI Improvements**

#### Menu Bar Organization
- **📊 STATUS** section → health, water, sips, last sip time
- **📷 CAMERA** section → live preview + real-time detection stats
- **❓ HOW TO USE** → Quick instructions for first-time users
- **⚙️ SETTINGS** → Tuning parameters
- **Control** → Pause/Resume monitoring
- **Help** → Quick start guide
- Better emoji indicators for status (🟢 good, 🟡 okay, 🔴 critical)

#### Status Indicators
- Health status emoji: 🟢 (good), 🟡 (okay), 🔴 (critical)
- Face detection: 👤✓ or 🚫✗
- Smile detection: 😊✓ or 😐✗
- Hand detection: 👆✓ near or 👇✗ away
- Compliance: ✅ (all smiles) or ⚠️ (some failures)

#### Visual Progress
- Water intake bar: `████░░░░ 40%`
- Real-time emoji feedback for all stats
- Toggle label changes: ▶️ Resume / ⏸️ Pause

### 📋 **Documentation**

#### New Files
- **QUICKSTART.md** — Step-by-step guide for new users
  - What is this app?
  - How to run
  - How detection works
  - Menu breakdown
  - Settings explanation
  - Troubleshooting

- **Updated sounds/README.txt**
  - Clearer audio trigger descriptions
  - Vibe guide for each sound
  - Links to Voicemod Tuna
  - Step-by-step custom audio setup
  - Feature highlights

### 🔧 **Technical Changes**

#### shared_state.py
- Added `last_frame: bytes | None` field
- Added `update_frame(jpeg_bytes)` method
- Frame data included in `get_snapshot()`

#### narc.py
- Fixed double shame_zero.mp3 bug (now uses same slot)
- Added JPEG frame encoding every loop
- Frames push to shared_state for camera preview
- No changes to detection logic

#### menubar.py
- Reorganized `_build_menu()` with sections & headers
- Added camera window: `showCameraPreview_()` action
- Added `cameraTimerFired_()` for 10fps refresh
- Improved `timerFired_()` with emoji indicators & progress bars
- Enhanced stats display with visual formatting
- Added help section with instructions
- Better toggle label (⏸️/▶️)
- Clean up on quit: close camera window, stop timer

#### settings_store.py
- Added `DAILY_WATER_GOAL_SIPS` (default: 8)

#### actions.py
- No changes (audio system already working)

---

## Bug Fixes

✅ **Audio stacking** — Both shame_zero calls now use same slot "warn"  
✅ **Menu visibility** — Stats now always visible (not hidden by camera window)  
✅ **User confusion** — Added clear labels, emoji, help text  
✅ **No TTS dependency** — Removed robot voice completely  

---

## Known Limitations

- Camera preview frame rate depends on detection processing (typically 5-10 fps)
- JPEG encoding adds ~2ms latency per frame
- Window stays open if app crashes (use Cmd+Q or Activity Monitor to force close)

---

## Future Ideas

- 📊 Weekly/monthly hydration statistics
- 🌙 Sleep schedule awareness (no nagging at night)
- 🔔 Slack integration for team accountability
- 🎨 Customizable menu bar color based on health
- 📱 iOS companion app for logging manual water intake
- 🌍 Cloud sync across devices
- 🎯 Habit streak tracking
- 🎨 Dark mode support

---

## Files Modified

| File | Changes |
|------|---------|
| `menubar.py` | Menu reorganization, camera window, emoji stats, help text |
| `narc.py` | Fixed audio slot, added JPEG frame encoding |
| `shared_state.py` | Added frame field + update method |
| `settings_store.py` | Added daily water goal setting |
| `sounds/README.txt` | Better documentation, emoji guide |

---

## New Files

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | User guide for new users |
| `CHANGELOG.md` | This file |

---

## How to Test

1. **Run the app:**
   ```bash
   python main.py
   ```

2. **Check menu bar:**
   - Look for 💧 icon in top right
   - Click to open menu
   - Verify emoji indicators show correctly

3. **Test camera preview:**
   - Click "👁️ Open Live Preview"
   - Window should appear (240×180)
   - Move around — should update live feed

4. **Test water tracking:**
   - Take a drink with smile detected
   - Check menu bar: "💦 Water: 1/8" should increment
   - Progress bar should update: `█░░░░░░░░░`

5. **Test audio:**
   - Sip with smile → should hear sip_success.mp3
   - Sip without smile → should hear sip_fail.mp3
   - Only ONE audio file plays per sip (no stacking)

6. **Check stats update:**
   - Health decreases every 60 seconds
   - Emoji indicators change color
   - "Last sip" timer updates

---

## Version 1.0 Summary

Original features (still working):
- ✅ Face + hand detection via MediaPipe
- ✅ Smile detection + hand-near-mouth
- ✅ Health decay system
- ✅ Sip compliance tracking
- ✅ Threat levels (warning at 75, hostage at 30, nuclear at 0)
- ✅ App hiding, Slack alerts, forced sleep
- ✅ Settings persistence (JSON)
- ✅ Pause/Resume monitoring
- ✅ Audio deduplication

---

Enjoy! 💧✨
