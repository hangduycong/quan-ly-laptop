#!/usr/bin/env python3
"""Export a finished render to `export edited video/` (new file name every time, never overwrite).

Without overlays or burned captions the render is copied as-is (no re-encode; it is already
H.264 High, CRF 18 with a bitrate cap, BT.709 tags, AAC 320k 48 kHz, +faststart: YouTube-ready).
With overlays and/or burned captions it re-encodes once: overlays first (frame 0 shifted to its
start), captions LAST so nothing covers them.

Usage:
  python3 export.py <video>                                   latest non-draft render
  python3 export.py <video> --captions latest                 + sidecar .srt (upload to YouTube)
  python3 export.py <video> --captions latest --burn          burn captions into the picture
  python3 export.py <video> --overlays overlays.json          {"overlays":[{"file":"x.mov","at":12.0}]}
  python3 export.py <video> --render <v>_v3.mp4
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from common import (die, export_dir, ffmpeg, find_workspace, latest_version, load_config, need_tools,
                    next_version, probe_clip, read_json, say, video_dir, video_encode_args, workspace_arg)


def srt_to_ass(srt: Path, ass: Path, W: int, H: int, st: dict) -> None:
    size = round(st["size_at_1080"] * H / 1080)
    margin = round(st["position_y_from_bottom"] * H)
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\nWrapStyle: 2\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
            "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
            "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: Default,{st['font']},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,"
            f"{-1 if st.get('bold') else 0},0,0,0,100,100,0,0,1,{st['outline']},{st['shadow']},2,"
            f"{round(W * 0.06)},{round(W * 0.06)},{margin},1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

    def tc(s):
        h, m, rest = s.split(":")
        sec, ms = rest.split(",")
        return f"{int(h)}:{m}:{sec}.{int(ms) // 10:02d}"

    ev = []
    for block in re.split(r"\n\s*\n", srt.read_text(encoding="utf-8").strip()):
        lines = block.splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            a, b = [x.strip() for x in lines[1].split("-->")]
            text = r"\N".join(lines[2:]).replace("{", "(").replace("}", ")")
            ev.append(f"Dialogue: 0,{tc(a)},{tc(b)},Default,,0,0,0,,{text}")
    ass.write_text(head + "\n".join(ev) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--render")
    ap.add_argument("--captions", help="'latest' hoặc đường dẫn .srt")
    ap.add_argument("--burn", action="store_true")
    ap.add_argument("--overlays")
    workspace_arg(ap)
    a = ap.parse_args()
    need_tools()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    rd = vd / "renders"
    src = (rd / Path(a.render).name) if a.render else latest_version(rd, a.video, ".mp4")
    if not src or not src.exists():
        die("chưa có bản render (không tính draft) — chạy render.py")
    srt = None
    if a.captions:
        srt = latest_version(vd / "captions", "captions", ".srt") if a.captions == "latest" else Path(a.captions)
        if not srt or not srt.exists():
            die("không thấy file phụ đề — chạy captions.py")
    ovs = (read_json(vd / a.overlays if not Path(a.overlays).is_absolute() else Path(a.overlays)) or {}).get("overlays", []) \
        if a.overlays else []
    out = next_version(export_dir(ws, cfg), a.video, ".mp4")
    info = probe_clip(src)
    W, H = info["width"], info["height"]
    if not ovs and not (srt and a.burn):
        shutil.copy2(src, out)
        say(f"đã xuất (copy, không encode lại): {out.relative_to(ws)}")
    else:
        ins, fc, last = ["-i", str(src)], [], "[0:v]"
        for k, o in enumerate(ovs, 1):
            f = Path(o["file"])
            f = f if f.is_absolute() else (vd / f if (vd / f).exists() else ws / f)
            if not f.exists():
                die(f"overlay {o['file']} không tồn tại")
            t = float(o["at"])
            dur = probe_clip(f)["duration"]
            ins += ["-i", str(f)]
            fc.append(f"[{k}:v]format=yuva420p,scale={W}:{H},setpts=PTS-STARTPTS+{t}/TB[o{k}]")
            fc.append(f"{last}[o{k}]overlay=eof_action=pass:enable='between(t,{t},{t + dur})'[v{k}]")
            last = f"[v{k}]"
        if srt and a.burn:
            ass = vd / "captions" / (srt.stem + ".ass")
            srt_to_ass(srt, ass, W, H, cfg["captions"]["style"])
            esc = str(ass).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
            fc.append(f"{last}subtitles=filename='{esc}'[vout]")  # captions LAST
            last = "[vout]"
        ffmpeg([*ins, "-filter_complex", ";".join(fc), "-map", last, "-map", "0:a:0",
                *video_encode_args(cfg, False, H), "-c:a", "copy", "-movflags", "+faststart", str(out)])
        say(f"đã xuất (encode lại: {len(ovs)} overlay{', phụ đề burn' if srt and a.burn else ''}): {out.relative_to(ws)}")
    if srt and not a.burn:
        side = out.with_suffix(".srt")
        shutil.copy2(srt, side)
        say(f"phụ đề rời: {side.relative_to(ws)} (tải lên YouTube làm closed captions)")
    got = probe_clip(out)
    say(f"  {got['duration']:.2f}s {got['width']}x{got['height']} @{got['fps_float']} {got['vcodec']}/{got.get('acodec')}")


if __name__ == "__main__":
    main()
