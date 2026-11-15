import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from "remotion";
import {fontFamily} from "./font";
import type {OutroProps} from "./types";

// 1920×1080. Thẻ video kế tiếp 615×345 (right 90, top 110), nút đăng ký 294×294 (right 250, bottom 150).
// showGuides=true chỉ để xem bố cục; bản giao luôn tắt.
export const Outro = ({brand, showGuides}: OutroProps) => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [0, 18], [0, 1], {extrapolateRight: "clamp"});
  const drift = interpolate(frame, [0, 600], [0, 40]); // chuyển động rất nhẹ, không tranh với thẻ
  const guide = showGuides ? {border: "2px dashed rgba(255,255,255,.35)", borderRadius: 12} : {};
  return (
    <AbsoluteFill style={{background: brand.bg, opacity: fade, fontFamily}}>
      <div style={{position: "absolute", left: -200 + drift, top: 500, width: 700, height: 700, borderRadius: 999,
        background: brand.accent, filter: "blur(160px)", opacity: 0.25}} />
      <div style={{position: "absolute", left: 96, top: 110, width: 520}}>
        <Img src={staticFile(brand.logo)} style={{width: 200}} />
        <div style={{color: brand.fg, fontSize: 56, fontWeight: 900, marginTop: 28, lineHeight: 1.15}}>{brand.name}</div>
        <div style={{color: brand.accent, fontSize: 32, fontWeight: 700, marginTop: 14}}>{brand.cta ?? "Đăng ký kênh →"}</div>
      </div>
      <div style={{position: "absolute", width: 615, height: 345, right: 90, top: 110, ...guide}} />
      <div style={{position: "absolute", width: 294, height: 294, right: 250, bottom: 150, borderRadius: 999, ...guide}} />
    </AbsoluteFill>
  );
};
