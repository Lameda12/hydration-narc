import { interpolate, useCurrentFrame } from "remotion";

interface Props {
  /** 0–100 */
  targetHealth: number;
  /** frame within the decay scene at which this health value is reached */
  startFrame?: number;
}

export const HealthBar: React.FC<Props> = ({ targetHealth, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const elapsed = frame - startFrame;

  // Animate health from 100 → targetHealth over 120 frames
  const health = interpolate(elapsed, [0, 120], [100, targetHealth], {
    extrapolateLeft:  "clamp",
    extrapolateRight: "clamp",
  });

  const isCritical  = health <= 15;
  const isDanger    = health <= 40;

  // Bar color: green → orange → red → deep red
  const barColor = isCritical
    ? "#7f1d1d"
    : isDanger
    ? "#ef4444"
    : health <= 60
    ? "#f97316"
    : "#22c55e";

  // Crack effect: jitter opacity when critical
  const crackOpacity = isCritical
    ? interpolate(Math.sin(elapsed * 0.8), [-1, 1], [0.6, 1])
    : 1;

  // Crack lines: rendered as pseudo-SVG scratches when health is low
  const cracks = isCritical ? (
    <svg
      style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }}
      viewBox="0 0 400 40"
      preserveAspectRatio="none"
    >
      <polyline points="80,0 90,20 75,40"  stroke="white" strokeWidth="1.5" fill="none" opacity="0.5" />
      <polyline points="200,5 210,25 195,40" stroke="white" strokeWidth="1"   fill="none" opacity="0.4" />
      <polyline points="310,0 320,18 305,40" stroke="white" strokeWidth="1.5" fill="none" opacity="0.5" />
    </svg>
  ) : null;

  return (
    <div style={{ width: "100%", fontFamily: "'Courier New', monospace" }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
        <span style={{ color: isCritical ? "#ef4444" : "#e5e7eb", fontSize: 18, fontWeight: "bold", letterSpacing: 2 }}>
          HEALTH
        </span>
        <span style={{
          color: isCritical ? "#ef4444" : "#e5e7eb",
          fontSize: 18,
          fontWeight: "bold",
          animation: isCritical ? "pulse 0.5s infinite" : "none",
        }}>
          {Math.round(health)}%
        </span>
      </div>

      {/* Track */}
      <div style={{
        position: "relative",
        width: "100%",
        height: 40,
        background: "#1f2937",
        borderRadius: 4,
        border: `2px solid ${isCritical ? "#ef4444" : "#374151"}`,
        overflow: "hidden",
        opacity: crackOpacity,
      }}>
        {/* Fill */}
        <div style={{
          width: `${health}%`,
          height: "100%",
          background: `linear-gradient(90deg, ${barColor}, ${barColor}cc)`,
          transition: "width 0.1s linear, background 0.3s ease",
          boxShadow: isCritical ? `0 0 16px ${barColor}` : "none",
        }} />

        {/* Segment notches */}
        {[25, 50, 75].map(p => (
          <div key={p} style={{
            position: "absolute",
            left: `${p}%`,
            top: 0, bottom: 0,
            width: 2,
            background: "#111827",
            opacity: 0.6,
          }} />
        ))}

        {cracks}
      </div>

      {isCritical && (
        <p style={{
          color: "#ef4444",
          fontSize: 14,
          marginTop: 6,
          letterSpacing: 3,
          textAlign: "center",
          fontWeight: "bold",
          opacity: interpolate(Math.sin(elapsed * 1.2), [-1, 1], [0.4, 1]),
        }}>
          ⚠ KEYBOARD SEIZURE IMMINENT ⚠
        </p>
      )}
    </div>
  );
};
