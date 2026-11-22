import {Composition} from "remotion";
import {Intro} from "./Intro";
import {Outro} from "./Outro";
import {Audiogram} from "./Audiogram";
import brandProps from "../brand.json";
import audiogramProps from "../audiogram.json";
import type {AudiogramProps, IntroProps, OutroProps} from "./types";

const FPS = 30;

const ag = (props: AudiogramProps) => ({durationInFrames: Math.max(1, Math.round(props.durationInSeconds * FPS))});

export const RemotionRoot = () => (
  <>
    {/* Intro 3.5 s: windup → hit (logo bật lên đúng tiếng hit) → settle → giữ */}
    <Composition id="Intro" component={Intro} durationInFrames={Math.round(3.5 * FPS)} fps={FPS}
      width={1920} height={1080} defaultProps={brandProps as IntroProps} />
    {/* Outro 20 s: thương hiệu ở 1/3 trái, 2/3 phải để trống cho end screen của YouTube */}
    <Composition id="Outro" component={Outro} durationInFrames={20 * FPS} fps={FPS}
      width={1920} height={1080} defaultProps={brandProps as OutroProps} />
    {/* Audiogram: 16:9, 1:1, 9:16 từ cùng một component */}
    <Composition id="Audiogram" component={Audiogram} fps={FPS} width={1920} height={1080}
      durationInFrames={450} defaultProps={audiogramProps as AudiogramProps}
      calculateMetadata={({props}) => ag(props)} />
    <Composition id="AudiogramSquare" component={Audiogram} fps={FPS} width={1080} height={1080}
      durationInFrames={450} defaultProps={audiogramProps as AudiogramProps}
      calculateMetadata={({props}) => ag(props)} />
    <Composition id="AudiogramVertical" component={Audiogram} fps={FPS} width={1080} height={1920}
      durationInFrames={450} defaultProps={audiogramProps as AudiogramProps}
      calculateMetadata={({props}) => ag(props)} />
  </>
);
