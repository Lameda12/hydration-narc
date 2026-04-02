import { interpolate, useCurrentFrame } from "remotion";

export const NuclearScene: React.FC = () => {
  const frame = useCurrentFrame();

  const flashOpacity  = interpolate(frame, [0, 8, 16], [0, 1, 0], { extrapolateRight: "clamp" });
  const textReveal    = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: "clamp" });
  const raisinReveal  = interpolate(frame, [50, 80], [0, 1], { extrapolateRight: "clamp" });
  const warningPulse  = interpolate(Math.sin(frame * 0.18), [-1, 1], [0.5, 1]);

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100%",
      background: "radial-gradient(ellipse at center, #3b0000 0%, #000 70%)",
      fontFamily: "'Courier New', monospace",
      gap: 24,
      position: "relative",
    }}>
      {/* Flash on scene entry */}
      <div style={{
        position: "absolute",
        inset: 0,
        background: "white",
        opacity: flashOpacity,
        pointerEvents: "none",
      }} />

      <div style={{ opacity: textReveal, textAlign: "center" }}>
        <p style={{
          fontSize: 14,
          letterSpacing: 8,
          color: "#ef4444",
          textTransform: "uppercase",
          margin: 0,
          opacity: warningPulse,
        }}>
          ☢ Nuclear Option Triggered ☢
        </p>
        <h2 style={{
          fontSize: 64,
          fontWeight: "900",
          color: "#f9fafb",
          margin: "8px 0",
          textShadow: "0 0 60px rgba(220,38,38,0.8)",
        }}>
          GOODNIGHT.
        </h2>
        <p style={{ color: "#9ca3af", fontSize: 18, margin: 0, fontStyle: "italic" }}>
          The machine is asleep. You did this.
        </p>
      </div>

      {/* Raisin emoji as stand-in asset */}
      <div style={{
        fontSize: 120,
        opacity: raisinReveal,
        transform: `scale(${interpolate(raisinReveal, [0, 1], [0.5, 1])})`,
        filter: "drop-shadow(0 0 30px rgba(220,38,38,0.6))",
      }}>
        🍇
      </div>

      <div style={{ opacity: raisinReveal, textAlign: "center" }}>
        <p style={{ color: "#6b7280", fontSize: 14, letterSpacing: 4, margin: 0 }}>
          PURITY SCORE: <span style={{ color: "#ef4444" }}>-250</span>
        </p>
        <p style={{ color: "#4b5563", fontSize: 12, letterSpacing: 2, margin: "4px 0 0" }}>
          You are a cautionary tale.
        </p>
      </div>
    </div>
  );
};
