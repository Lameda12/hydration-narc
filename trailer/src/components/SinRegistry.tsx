import { interpolate, useCurrentFrame } from "remotion";
import { SINS } from "../constants";

const FRAMES_PER_SIN = 30; // each sin gets ~1 second

export const SinRegistry: React.FC = () => {
  const frame = useCurrentFrame();

  // How many sins are currently revealed (fractional for partial animation)
  const revealed = Math.min(SINS.length, frame / FRAMES_PER_SIN);

  return (
    <div style={{
      width: "100%",
      fontFamily: "'Courier New', monospace",
      display: "flex",
      flexDirection: "column",
      gap: 6,
    }}>
      <h2 style={{
        color: "#f9fafb",
        fontSize: 22,
        letterSpacing: 6,
        fontWeight: "bold",
        marginBottom: 12,
        textAlign: "center",
        textTransform: "uppercase",
      }}>
        Mortal Sins Registry
      </h2>

      {SINS.map((sin, i) => {
        const sinProgress = Math.max(0, Math.min(1, revealed - i));
        if (sinProgress === 0) return null;

        const opacity = interpolate(sinProgress, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
        const translateX = interpolate(sinProgress, [0, 1], [-40, 0], { extrapolateRight: "clamp" });

        return (
          <div key={i} style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            opacity,
            transform: `translateX(${translateX}px)`,
            background: "rgba(17, 24, 39, 0.8)",
            borderLeft: `4px solid ${sin.color}`,
            borderRadius: 4,
            padding: "6px 14px",
          }}>
            <span style={{
              fontSize: 10,
              color: sin.color,
              fontWeight: "bold",
              letterSpacing: 2,
              minWidth: 52,
            }}>
              {sin.tier}
            </span>

            <span style={{
              fontSize: 15,
              color: "#f9fafb",
              fontWeight: "bold",
              flex: 1,
            }}>
              {sin.label}
            </span>

            <span style={{
              fontSize: 11,
              color: "#6b7280",
              fontFamily: "monospace",
              whiteSpace: "nowrap",
            }}>
              score {sin.score}
            </span>
          </div>
        );
      })}
    </div>
  );
};
