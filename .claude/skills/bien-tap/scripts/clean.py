#!/usr/bin/env python3
"""Move a finished video's work files (system/videos/<v>/) to system/.trash/ — only after the
creator said yes. Raw footage and exports are never touched.

Usage: python3 clean.py <video> --yes
"""
from __future__ import annotations

import argparse
import shutil
import time

from common import die, find_workspace, load_config, say, video_dir, workspace_arg


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("--yes", action="store_true", help="người dùng đã đồng ý")
    workspace_arg(ap)
    a = ap.parse_args()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws)
    vd = video_dir(ws, a.video, cfg)
    if not vd.exists():
        die(f"không có {vd.relative_to(ws)}")
    size = sum(p.stat().st_size for p in vd.rglob("*") if p.is_file()) / 1e9
    if not a.yes:
        say(f"sẽ chuyển {vd.relative_to(ws)} ({size:.2f} GB) vào system/.trash/. Hỏi người dùng, rồi chạy lại với --yes")
        return
    dst = ws / "system" / ".trash" / f"{a.video}-{time.strftime('%Y%m%d-%H%M%S')}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(vd), str(dst))
    say(f"đã chuyển vào {dst.relative_to(ws)} ({size:.2f} GB). Xóa hẳn thư mục đó khi chắc chắn.")


if __name__ == "__main__":
    main()
