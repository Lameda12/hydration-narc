import { interpolate, useCurrentFrame } from "remotion";

export const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();

  const reveal  = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const pulse   = interpolate(Math.sin(frame * 0.12), [-1, 1], [0.85, 1]);
  const subReveal = interpolate(frame, [35, 55], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100%",
      gap: 20,
      fontFamily: "'Courier New', monospace",
    }}>
      <h2 style={{
        fontSize: 52,
        fontWeight: "900",
        color: "#22c55e",
        letterSpacing: 4,
        margin: 0,
        opacity: reveal,
        transform: `scale(${pulse})`,
        textShadow: "0 0 30px rgba(34,197,94,0.5)",
        textAlign: "center",
      }}>
        github.com/Lameda12/hydration-narc
      </h2>

      <p style={{
        fontSize: 20,
        color: "#9ca3af",
        letterSpacing: 3,
        margin: 0,
        opacity: subReveal,
        textAlign: "center",
      }}>
        Open source. MIT licensed. Hostile by design.
      </p>

      <div style={{
        opacity: subReveal,
        display: "flex",
        gap: 24,
        marginTop: 12,
      }}>
        {["#HydrationNarc", "#MortalSin", "#DrinkWater"].map(tag => (
          <span key={tag} style={{
            color: "#3b82f6",
            fontSize: 16,
            letterSpacing: 2,
            fontWeight: "bold",
          }}>
            {tag}
          </span>
        ))}
      </div>

      <p style={{
        opacity: interpolate(frame, [60, 80], [0, 1], { extrapolateRight: "clamp" }),
        color: "#374151",
        fontSize: 13,
        letterSpacing: 2,
        fontStyle: "italic",
        marginTop: 20,
      }}>
        By running start.sh you acknowledged this document. You knew.
      </p>
    </div>
  );
};
