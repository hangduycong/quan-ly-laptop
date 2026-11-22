#!/usr/bin/env python3
"""Self-check a render before showing it: duration vs plan, format, loudness, and a strip of
frames around every cut (before | after) to spot flashes, jumps and wrong zoom.

Usage:
  python3 check.py <video>                 latest render (draft or not)
  python3 check.py <video> --render FILE   a specific render
  python3 check.py <video> --max-cuts 40   at most N cut points in the strip (sampled evenly)
Writes system/videos/<v>/verify/<render>_cuts.png. Open it with the Read tool and look.
"""
from __future__ import annotations

import argparse
import math
import shutil
from pathlib import Path

from common import (die, ffmpeg, find_workspace, fmt_tc, load_config, loudness, need_tools, probe_clip,
                    read_json, say, video_dir, workspace_arg)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--render")
    ap.add_argument("--max-cuts", type=int, default=40)
    workspace_arg(ap)
    a = ap.parse_args()
    need_tools()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    rd = vd / "renders"
    if a.render:
        r = rd / Path(a.render).name
    else:
        cands = sorted(rd.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        r = cands[-1] if cands else None
    if not r or not r.exists():
        die("không có bản render để kiểm tra")
    plan = read_json(r.with_suffix(".cuts.json")) or die(f"thiếu {r.with_suffix('.cuts.json').name}")
    info = probe_clip(r)
    ok = True
    say(f"{r.name}: {info['duration']:.3f}s (kế hoạch {plan['duration']:.3f}s) {info['width']}x{info['height']} "
        f"@{info['fps_float']} {info['vcodec']}/{info.get('acodec')} {info.get('channels')}ch")
    if abs(info["duration"] - plan["duration"]) > 0.1:
        say("  ! độ dài lệch > 0.1 s")
        ok = False
    ld = loudness(r)
    say(f"  âm lượng: {ld.get('lufs')} LUFS, true peak {ld.get('true_peak')} dBTP "
        f"(mục tiêu {cfg['audio']['voice']['target_lufs']} / ≤ {cfg['audio']['voice']['true_peak']})")
    if ld.get("true_peak") is not None and ld["true_peak"] > -0.5:
        say("  ! true peak quá cao (nguy cơ vỡ tiếng)")
        ok = False
    # sections: first speech / first B-roll
    fps = float(plan["fps_float"])
    for kind in ("speech", "broll"):
        p = next((p for p in plan["pieces"] if p["kind"] == kind and p["frames"] / fps > 3), None)
        if p:
            l2 = loudness(r, p["out_start"] + 0.5, p["frames"] / fps - 1.0)
            say(f"  đoạn {kind} đầu tiên ({fmt_tc(p['out_start'])}): {l2.get('lufs')} LUFS")
    cuts = [p["out_start"] for p in plan["pieces"][1:] if p["cut_before"]]
    if cuts:
        if len(cuts) > a.max_cuts:
            step = len(cuts) / a.max_cuts
            cuts = [cuts[int(i * step)] for i in range(a.max_cuts)]
        tmp = vd / "verify" / f".tmp_{r.stem}"
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        k = 0
        for t in cuts:
            for dt in (-2 / fps, 1 / fps):
                ffmpeg(["-ss", f"{max(0.0, t + dt):.3f}", "-i", str(r), "-frames:v", "1", "-vf", "scale=320:-2",
                        str(tmp / f"{k:04d}.png")], check=False)
                k += 1
        rows = int(math.ceil(k / 8))
        out = vd / "verify" / f"{r.stem}_cuts.png"
        ffmpeg(["-framerate", "1", "-i", str(tmp / "%04d.png"), "-vf", f"tile=8x{rows}:padding=4:color=red",
                "-frames:v", "1", "-update", "1", str(out)], check=False)
        shutil.rmtree(tmp, ignore_errors=True)
        say(f"  ảnh điểm cắt: {out.relative_to(ws)} — mỗi cặp = trước | sau một điểm cắt "
            f"({len(cuts)} điểm, thời điểm: {', '.join(fmt_tc(c) for c in cuts[:12])}{' …' if len(cuts) > 12 else ''})")
    say("KẾT QUẢ: " + ("đạt các kiểm tra tự động (vẫn phải xem ảnh)" if ok else "CÓ VẤN ĐỀ, xem các dòng !"))


if __name__ == "__main__":
    main()
