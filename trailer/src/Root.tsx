import { Composition } from "remotion";
import { NarcTrailer } from "./NarcTrailer";
import { DURATION_FRAMES, FPS } from "./constants";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="NarcTrailer"
    component={NarcTrailer}
    durationInFrames={DURATION_FRAMES}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);
