#!/usr/bin/env python3
"""Contact sheet of a clip (default 2 frames per second, 8 per row, small) to *watch* B-roll.

Usage:
  python3 contact_sheet.py <video> <clip> [--fps 2] [--start S --end S] [--width 240]
Writes system/videos/<video>/frames/<clip>_sheet[_N].png and prints the path(s). Open them with
the Read tool and look: action start/resolve, natural transitions (black-to-black), soft focus,
operator fumbling, vertical framing. Each sheet holds at most 64 frames.
"""
from __future__ import annotations

import argparse
import math

from common import (die, ffmpeg, find_workspace, fmt_tc, load_config, need_tools, read_json, say,
                    video_dir, workspace_arg)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("clip")
    ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float)
    ap.add_argument("--width", type=int, default=240)
    workspace_arg(ap)
    a = ap.parse_args()
    need_tools()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    man = read_json(vd / "manifest.json") or die("chưa có manifest.json — chạy ingest.py")
    clip = next((c for c in man["clips"] if c["id"] == a.clip), None) or die(f"không có clip {a.clip}")
    src = ws / clip["path"] if not clip["path"].startswith("/") else clip["path"]
    end = a.end or clip["probe"]["duration"]
    per = 64
    total = max(1, int(math.ceil((end - a.start) * a.fps)))
    out_dir = vd / "frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    sheets = []
    for k in range(int(math.ceil(total / per))):
        s = a.start + k * per / a.fps
        n = min(per, total - k * per)
        rows = int(math.ceil(n / 8))
        out = out_dir / (f"{a.clip}_sheet.png" if total <= per else f"{a.clip}_sheet_{k + 1}.png")
        ffmpeg(["-ss", f"{s:.3f}", "-t", f"{n / a.fps:.3f}", "-i", str(src), "-vf",
                f"fps={a.fps},scale={a.width}:-2,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize=14:"
                f"fontcolor=white:box=1:boxcolor=black@0.5,tile=8x{rows}:padding=2",
                "-frames:v", "1", "-update", "1", str(out)], check=False)
        if not out.exists():  # drawtext may be missing: retry without the timestamp
            ffmpeg(["-ss", f"{s:.3f}", "-t", f"{n / a.fps:.3f}", "-i", str(src), "-vf",
                    f"fps={a.fps},scale={a.width}:-2,tile=8x{rows}:padding=2", "-frames:v", "1",
                    "-update", "1", str(out)])
        sheets.append(out)
        say(f"{out.relative_to(ws)}  ({fmt_tc(s)}–{fmt_tc(s + n / a.fps)}, {n} khung, "
            f"mỗi khung {1 / a.fps:.2f}s, đọc trái→phải, trên→dưới)")


if __name__ == "__main__":
    main()
