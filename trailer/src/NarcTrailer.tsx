import {
  AbsoluteFill,
  Audio,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { DURATION_FRAMES, FPS, SCENES } from "./constants";
import { TitleCard }    from "./components/TitleCard";
import { HealthBar }    from "./components/HealthBar";
import { SinRegistry }  from "./components/SinRegistry";
import { NuclearScene } from "./components/NuclearScene";
import { CTAScene }     from "./components/CTAScene";

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  // Subtle scanline / noise feel via repeating gradient
  const shift = (frame * 0.3) % 4;
  return (
    <AbsoluteFill style={{
      background: "#030712",
      backgroundImage: `repeating-linear-gradient(
        0deg,
        transparent,
        transparent 3px,
        rgba(255,255,255,0.012) 3px,
        rgba(255,255,255,0.012) 4px
      )`,
      backgroundPositionY: `${shift}px`,
    }} />
  );
};

const SceneLabel: React.FC<{ label: string }> = ({ label }) => (
  <div style={{
    position: "absolute",
    bottom: 28,
    left: 40,
    fontFamily: "'Courier New', monospace",
    fontSize: 11,
    letterSpacing: 4,
    color: "#374151",
    textTransform: "uppercase",
  }}>
    {label}
  </div>
);

export const NarcTrailer: React.FC = () => {
  const frame = useCurrentFrame();

  // Cross-scene vignette
  const vignetteStrength = interpolate(
    frame,
    [0, 60, DURATION_FRAMES - 60, DURATION_FRAMES],
    [1, 0.3, 0.3, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill>
      <Background />

      {/* ── 1. Title card (0–90) ─────────────────────────────────────── */}
      <Sequence from={SCENES.intro.start} durationInFrames={SCENES.intro.end - SCENES.intro.start}>
        <AbsoluteFill style={{ padding: "0 80px" }}>
          <TitleCard />
        </AbsoluteFill>
        <SceneLabel label="The Setup" />
      </Sequence>

      {/* ── 2. Health bar draining (90–240) ──────────────────────────── */}
      <Sequence from={SCENES.decay.start} durationInFrames={SCENES.decay.end - SCENES.decay.start}>
        <AbsoluteFill style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "0 160px",
          gap: 40,
        }}>
          <p style={{
            fontFamily: "'Courier New', monospace",
            fontSize: 20,
            letterSpacing: 6,
            color: "#6b7280",
            textTransform: "uppercase",
            margin: 0,
            opacity: interpolate(frame - SCENES.decay.start, [0, 15], [0, 1], { extrapolateRight: "clamp" }),
          }}>
            You forgot to drink. Again.
          </p>

          <HealthBar targetHealth={12} startFrame={SCENES.decay.start} />
        </AbsoluteFill>
        <SceneLabel label="The Descent" />
      </Sequence>

      {/* ── 3. Sin registry (240–570) ────────────────────────────────── */}
      <Sequence from={SCENES.sins.start} durationInFrames={SCENES.sins.end - SCENES.sins.start}>
        <AbsoluteFill style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "40px 100px",
        }}>
          <div style={{ width: "100%", maxWidth: 800 }}>
            <SinRegistry />
          </div>
        </AbsoluteFill>
        <SceneLabel label="The Reckoning" />
      </Sequence>

      {/* ── 4. Nuclear scene (570–720) ───────────────────────────────── */}
      <Sequence from={SCENES.nuclear.start} durationInFrames={SCENES.nuclear.end - SCENES.nuclear.start}>
        <AbsoluteFill>
          <NuclearScene />
        </AbsoluteFill>
        <SceneLabel label="The Consequence" />
      </Sequence>

      {/* ── 5. CTA (720–900) ────────────────────────────────────────── */}
      <Sequence from={SCENES.cta.start} durationInFrames={SCENES.cta.end - SCENES.cta.start}>
        <AbsoluteFill style={{ padding: "0 80px" }}>
          <CTAScene />
        </AbsoluteFill>
        <SceneLabel label="The Escape Route (There Isn't One)" />
      </Sequence>

      {/* ── Audio track ─────────────────────────────────────────────── */}
      <Sequence from={0}>
        <Audio src={staticFile("intro.mp3")} />
      </Sequence>
      <Sequence from={90}>
        <Audio src={staticFile("logic.mp3")} />
      </Sequence>
      <Sequence from={240}>
        <Audio src={staticFile("threat.mp3")} />
      </Sequence>
      <Sequence from={720}>
        <Audio src={staticFile("outro.mp3")} />
      </Sequence>

      {/* Global vignette overlay */}
      <AbsoluteFill style={{
        background: `radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,${vignetteStrength}) 100%)`,
        pointerEvents: "none",
      }} />
    </AbsoluteFill>
  );
};
