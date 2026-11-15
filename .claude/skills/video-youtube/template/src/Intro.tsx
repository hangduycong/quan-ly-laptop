import {AbsoluteFill, Audio, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {fontFamily} from "./font";
import type {IntroProps} from "./types";

export const Intro = ({brand, impact}: IntroProps) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const IMPACT = Math.round(impact * fps); // logo bật lên ĐÚNG khung này (tiếng hit của sting)
  const f = frame - IMPACT;

  const windup = interpolate(frame, [0, IMPACT], [0, 1], {extrapolateRight: "clamp"});
  const scale = spring({frame: f, fps, from: 1.18, to: 1, config: {damping: 9, mass: 0.5}});
  const logoOpacity = f < 0 ? 0 : 1;
  const flash = interpolate(f, [0, 6], [0.9, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const tagline = interpolate(f, [10, 22], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});

  return (
    <AbsoluteFill style={{background: brand.bg, alignItems: "center", justifyContent: "center", fontFamily}}>
      <Audio src={staticFile(brand.sting)} />
      <div style={{position: "absolute", width: 600, height: 600, borderRadius: 999, background: brand.accent,
        filter: "blur(120px)", opacity: windup * 0.5}} />
      <div style={{textAlign: "center"}}>
        <Img src={staticFile(brand.logo)} style={{width: 360, opacity: logoOpacity, transform: `scale(${scale})`}} />
        <div style={{marginTop: 28, color: brand.fg, opacity: tagline, fontSize: 64, fontWeight: 900}}>{brand.name}</div>
        {brand.tagline ? (
          <div style={{marginTop: 8, color: brand.accent, opacity: tagline, fontSize: 34, fontWeight: 500}}>{brand.tagline}</div>
        ) : null}
      </div>
      <AbsoluteFill style={{background: "#fff", opacity: flash}} />
    </AbsoluteFill>
  );
};
