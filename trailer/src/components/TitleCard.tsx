import { interpolate, useCurrentFrame } from "remotion";

export const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity  = interpolate(frame, [0, 20],  [0, 1], { extrapolateRight: "clamp" });
  const subtitleDelay = interpolate(frame, [25, 45], [0, 1], { extrapolateRight: "clamp" });
  const taglineDelay  = interpolate(frame, [45, 65], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100%",
      gap: 16,
      fontFamily: "'Courier New', monospace",
    }}>
      <h1 style={{
        fontSize: 88,
        fontWeight: "900",
        color: "#f9fafb",
        letterSpacing: 4,
        margin: 0,
        opacity: titleOpacity,
        textShadow: "0 0 40px rgba(239,68,68,0.6)",
        textTransform: "uppercase",
      }}>
        The Hydration Narc
      </h1>

      <p style={{
        fontSize: 26,
        color: "#ef4444",
        letterSpacing: 8,
        margin: 0,
        opacity: subtitleDelay,
        textTransform: "uppercase",
        fontWeight: "bold",
      }}>
        Drink water. Smile about it. Or face consequences.
      </p>

      <p style={{
        fontSize: 16,
        color: "#6b7280",
        letterSpacing: 4,
        margin: 0,
        opacity: taglineDelay,
        fontStyle: "italic",
      }}>
        A macOS utility that watches you. Continuously. With judgment.
      </p>
    </div>
  );
};
