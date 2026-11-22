#!/usr/bin/env python3
"""Check the editing environment. Prints a short report; never prints key values.

Usage: python3 doctor.py [--workspace DIR]
"""
from __future__ import annotations

import argparse
import shutil
import sys

from common import find_workspace, load_config, load_key, raw_dir, run, say, workspace_arg


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    workspace_arg(ap)
    args = ap.parse_args()
    ok = True
    say(f"python {sys.version.split()[0]}" + ("" if sys.version_info >= (3, 9) else "  ← cần 3.9+"))
    ok &= sys.version_info >= (3, 9)
    for t in ("ffmpeg", "ffprobe"):
        if shutil.which(t):
            ver = run([t, "-version"]).stdout.splitlines()[0].split(" Copyright")[0]
            say(f"{t}: {ver}")
        else:
            say(f"{t}: THIẾU  ← cài ffmpeg")
            ok = False
    if shutil.which("ffmpeg"):
        filters = run(["ffmpeg", "-hide_banner", "-filters"]).stdout
        for f in ("subtitles", "loudnorm", "lut3d"):
            say(f"  filter {f}: {'có' if f' {f} ' in filters else 'không có'}")
    ws = find_workspace(args.workspace)
    cfg = load_config(ws)
    say(f"workspace: {ws}")
    rd = raw_dir(ws, cfg)
    n = len([p for p in rd.iterdir()]) if rd.exists() else 0
    say(f"raw video/: {n} mục")
    key = load_key(ws)
    say("speech-to-text key: " + ("có (không in ra)" if key else
        "CHƯA CÓ ← tạo system/keys.env với SPEECH_TO_TEXT_API_KEY=..., hoặc lưu key trong môi trường"))
    say("node (chỉ cho motion overlays): " + ("có" if shutil.which("node") else "không có (tùy chọn)"))
    say("DaVinci Resolve Studio: tùy chọn, xem davinci/README.md khi đã mua")
    say("KẾT QUẢ: " + ("sẵn sàng" if ok and key else "thiếu điều kiện, xem các dòng trên"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
