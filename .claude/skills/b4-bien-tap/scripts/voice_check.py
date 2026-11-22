#!/usr/bin/env python3
"""Diagnose a muffled / "underwater" voice before touching EQ (references/voice-and-audio.md).

Measures on ~20 s of talking: RMS per channel, L-R difference (phase / two different mics summed),
and band levels relative to the full signal: <300 Hz, ~1 kHz, >3 kHz, >6 kHz.
A clean voice has its >3 kHz band roughly 10-15 dB under the total; ~22 dB under means a covered
or badly placed mic.

Usage: python3 voice_check.py <video> <clip> [--start S] [--dur 20]
"""
from __future__ import annotations

import argparse
import re

from common import (channel_levels, die, find_workspace, load_config, need_tools, read_json, run, say,
                    video_dir, workspace_arg)


def mean_db(src, start, dur, af) -> float | None:
    r = run(["ffmpeg", "-hide_banner", "-nostdin", "-ss", f"{start:.2f}", "-t", f"{dur:.2f}", "-i", str(src),
             "-map", "0:a:0", "-af", f"{af},volumedetect", "-f", "null", "-"], check=False)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr or "")
    return float(m.group(1)) if m else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("clip")
    ap.add_argument("--start", type=float)
    ap.add_argument("--dur", type=float, default=20.0)
    workspace_arg(ap)
    a = ap.parse_args()
    need_tools()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    man = read_json(vd / "manifest.json") or die("chưa có manifest.json")
    c = next((c for c in man["clips"] if c["id"] == a.clip), None) or die(f"không có clip {a.clip}")
    src = ws / c["path"] if not c["path"].startswith("/") else c["path"]
    toks = read_json(vd / "words" / f"{a.clip}.json", []) or []
    start = a.start if a.start is not None else next((t["start"] for t in toks if t["type"] == "word"), 0.0)
    lv = channel_levels(src, start, a.dur)
    say(f"RMS theo kênh: {', '.join(f'{x:.1f} dB' for x in lv)}")
    if len(lv) >= 2:
        diff = mean_db(src, start, a.dur, "pan=mono|c0=c0-c1")
        full = mean_db(src, start, a.dur, "pan=mono|c0=0.5*c0+0.5*c1")
        if diff is not None and full is not None:
            say(f"L-R: {diff:.1f} dB so với tổng {full:.1f} dB → "
                + ("hai kênh giống hệt (dual mono), không phải lỗi pha" if diff < full - 40 else
                   "hai kênh KHÁC nhau: nếu là hai mic khác nhau bị cộng lại → chỉ dùng một kênh "
                   "(settings.py <v> set audio.voice.channel=...; ingest đã tự chọn nếu một kênh im)"))
    total = mean_db(src, start, a.dur, "aformat=channel_layouts=mono")
    bands = {"<300 Hz": "lowpass=f=300", "~1 kHz": "bandpass=f=1000:w=600", ">3 kHz": "highpass=f=3000",
             ">6 kHz": "highpass=f=6000"}
    if total is None:
        die("không đo được (clip không có tiếng?)")
    say(f"tổng: {total:.1f} dB")
    hi3 = None
    for name, f in bands.items():
        v = mean_db(src, start, a.dur, f"aformat=channel_layouts=mono,{f}")
        if v is not None:
            say(f"  {name}: {v - total:+.1f} dB so với tổng")
            if name == ">3 kHz":
                hi3 = v - total
    if hi3 is not None:
        if hi3 < -18:
            say(f"→ dải >3 kHz thấp ({hi3:.0f} dB): mic bị che / đặt sai. Bật EQ: settings.py <v> set audio.voice.eq=true "
                "(và denoise=true nếu ồn), nhắc người dùng kẹp mic ngoài áo, 15–20 cm dưới cằm.")
        else:
            say(f"→ dải >3 kHz bình thường ({hi3:.0f} dB): giọng không bị đục do mic.")


if __name__ == "__main__":
    main()
