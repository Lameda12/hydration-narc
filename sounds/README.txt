🎵 HYDRATION NARC — Audio Guide

💧 How to Use:
1. Drink water with camera detecting your smile + hand near mouth
2. App plays audio feedback based on what happened
3. Drop custom MP3 files here to replace default sounds (optional)
4. Missing files? App runs silent — no TTS robot voice

❌ NO SETUP NEEDED — Audio triggers automatically based on your actions!

📋 AUDIO TRIGGERS & FILE GUIDE:

✅ sip_success.mp3 — YOU DRANK! 🎉
  When: Hand near mouth + Smile detected ✓
  Vibe: Celebration! Catgirl cheer, anime "yatta!", energy approval
  Ideas: Voicemod Tuna, Yamato Kudasai soundboards

❌ sip_fail.mp3 — CHEATER! 😤
  When: Hand near mouth BUT no smile ✗
  Vibe: Sassy disappointment — "ara ara?", buzzer, confused anime
  Ideas: Voicemod Tuna, disappointed sighs

⚠️ observed.mp3 — I SEE YOU 👀
  When: Health score drops to 75 (you're slacking)
  Vibe: Judgmental stare — anime gasp, "excuse me?", suspicious tone
  Ideas: Anime suspicious reactions, voice acting clips

🔒 hostage.mp3 — LOCKED DOWN 🚫
  When: Health score drops to 30 (apps get hidden)
  Vibe: Threatening — villain laugh, dramatic sting, menacing whisper
  Ideas: Anime villain, boss music, dramatic trailers

💀 shame_zero.mp3 — NUCLEAR 💥
  When: Health hits 0 (Slack alert + 60s till forced sleep)
  Vibe: Full shame — "L + ratio", failure horns, dramatic collapse
  Ideas: Voicemod fail sounds, sad anime OST, notification chaos

🎵 rickroll.mp3 — WELCOME BACK 😏
  When: System wakes after nuclear sleep lockout
  Vibe: "Never gonna give you up..." (classic or sassy remix)
  Source: rickroll.mp3 or anime parodies

🛠️ HOW TO ADD CUSTOM AUDIO:

1. Find clips you like from:
   - Voicemod Tuna: https://tuna.voicemod.net/sounds/ (free soundboard)
   - YouTube: Download MP3 converters or use ffmpeg
   - Sound effects: Freesound.org, Zapsplat, etc.

2. Convert to MP3 (if needed):
   ffmpeg -i video.mp4 -q:a 0 -map a output.mp3

3. Rename file to match trigger (sip_success.mp3, observed.mp3, etc.)

4. Drop into this folder — app picks it up automatically!

5. Check menu bar — should show progress with emojis 💧🥤😊

⚡ AUTOMATIC FEATURES:
✓ Audio deduplication (prevents overlapping/stacking sounds)
✓ Health status with color emoji (🟢 good, 🟡 okay, 🔴 critical)
✓ Water progress bar with percentage 💦 ████░░░░
✓ Live camera preview window to debug detection
✓ One-click pause/resume monitoring

🎯 NEXT STEPS:
→ Open menu bar (top right) to see live stats
→ Click "📷 Open Live Preview" to see what camera detects
→ Take a sip with smile → should play sip_success.mp3
→ Wait for audio feedback based on detection!
