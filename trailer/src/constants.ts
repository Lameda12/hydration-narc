export const FPS = 30;
export const DURATION_FRAMES = 900; // 30 seconds

// Scene frame ranges
export const SCENES = {
  intro:    { start: 0,   end: 90  }, // 0–3s   : Title card
  decay:    { start: 90,  end: 240 }, // 3–8s   : Health bar draining
  sins:     { start: 240, end: 570 }, // 8–19s  : Sin registry tiers
  nuclear:  { start: 570, end: 720 }, // 19–24s : Nuclear / raisin failure
  cta:      { start: 720, end: 900 }, // 24–30s : CTA
};

export const SINS = [
  { tier: "TIER 1",  label: "Verbal Shaming",     color: "#facc15", score: "≤ 100" },
  { tier: "TIER 1",  label: "Screen Dimming",      color: "#facc15", score: "≤ 60"  },
  { tier: "TIER 1",  label: "Mouse Jitter",        color: "#facc15", score: "≤ 60"  },
  { tier: "TIER 2",  label: "App Hostage",         color: "#f97316", score: "≤ 30"  },
  { tier: "TIER 2",  label: "Keyboard Seizure",    color: "#f97316", score: "≤ 15"  },
  { tier: "TIER 3",  label: "Slack Webhook Alert", color: "#ef4444", score: "= 0"   },
  { tier: "TIER 3",  label: "Grumpy Sip Penalty",  color: "#ef4444", score: "no smile" },
  { tier: "TIER 4",  label: "Forced Sleep",        color: "#dc2626", score: "0 × 60s" },
  { tier: "TIER 4",  label: "The Rickroll",        color: "#dc2626", score: "wake +30s" },
  { tier: "TIER 5",  label: "Unstoppable Clause",  color: "#7f1d1d", score: "> 3 sins" },
  { tier: "TIER 5",  label: "Public Confession",   color: "#7f1d1d", score: "negative purity" },
];
