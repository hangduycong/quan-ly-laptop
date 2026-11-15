import {useAudioData, visualizeAudio, visualizeAudioWaveform} from "@remotion/media-utils";
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {fontFamily} from "./font";
import type {AudiogramProps} from "./types";

const N = 32; // lũy thừa của 2

// Chiều cao cột là hàm của khung hình hiện tại (giải mã cả file một lần), không dùng analyser thời gian thực.
const Bars = ({src, color, height}: {src: string; color: string; height: number}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const data = useAudioData(staticFile(src));
  if (!data) return null;
  const spec = visualizeAudio({audioData: data, frame, fps, numberOfSamples: N, smoothing: true});
  const half = spec.slice(0, N / 2);
  const bars = [...half.slice().reverse(), ...half];
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", gap: 8, height}}>
      {bars.map((v, i) => (
        <div key={i} style={{width: 14, height: Math.max(8, Math.min(1, v * 4) * height), borderRadius: 7, background: color}} />
      ))}
    </div>
  );
};

const Wave = ({src, color, width, height}: {src: string; color: string; width: number; height: number}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const data = useAudioData(staticFile(src));
  if (!data) return null;
  const w = visualizeAudioWaveform({audioData: data, frame, fps, numberOfSamples: 128, windowInSeconds: 0.25});
  const pts = w.map((v, i) => `${(i / (w.length - 1)) * width},${height / 2 + v * height * 0.9}`).join(" ");
  return (
    <svg width={width} height={height}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth={5} strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  );
};

export const Audiogram = (p: AudiogramProps) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const t = frame / fps;
  const vertical = height > width;
  const cap = p.captions.find((c) => t >= c.start && t < c.end);
  const progress = frame / durationInFrames;
  const unit = Math.min(width, height) / 1080;
  return (
    <AbsoluteFill style={{background: p.bg, fontFamily, color: p.fg}}>
      <Audio src={staticFile(p.audio)} />
      <div style={{position: "absolute", top: (vertical ? 260 : 80) * unit, left: 0, right: 0, display: "flex",
        alignItems: "center", justifyContent: "center", gap: 32 * unit}}>
        {p.cover ? <Img src={staticFile(p.cover)} style={{width: 160 * unit, height: 160 * unit, borderRadius: 24 * unit, objectFit: "cover"}} /> : null}
        <div>
          {p.show ? <div style={{color: p.accent, fontSize: 30 * unit, fontWeight: 700}}>{p.show}</div> : null}
          <div style={{fontSize: 54 * unit, fontWeight: 900, maxWidth: (vertical ? 760 : 1100) * unit, lineHeight: 1.15}}>{p.title}</div>
        </div>
      </div>
      <div style={{position: "absolute", top: height * (vertical ? 0.42 : 0.38), left: 0, right: 0, display: "flex", justifyContent: "center"}}>
        {p.look === "wave"
          ? <Wave src={p.audio} color={p.accent} width={width * 0.8} height={260 * unit} />
          : <Bars src={p.audio} color={p.accent} height={260 * unit} />}
      </div>
      {/* phụ đề: tránh 18% dưới cùng (giao diện Shorts/Reels) */}
      <div style={{position: "absolute", left: 60 * unit, right: 60 * unit, bottom: height * (vertical ? 0.24 : 0.16),
        textAlign: "center", fontSize: (vertical ? 64 : 58) * unit, fontWeight: 900, lineHeight: 1.2,
        textShadow: "0 4px 18px rgba(0,0,0,.6)"}}>{cap?.text ?? ""}</div>
      <div style={{position: "absolute", left: 0, bottom: 0, height: 8 * unit, width: `${progress * 100}%`, background: p.fg}} />
    </AbsoluteFill>
  );
};
