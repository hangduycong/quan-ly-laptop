#!/usr/bin/env python3
"""Print a clip's tokens with their word index and time, to write exact keep.json ranges.

Usage:
  python3 words.py <video> <clip> [FROM] [TO]       index range (inclusive)
  python3 words.py <video> <clip> --at 02:14        tokens around a clip time (mm:ss or seconds)
"""
from __future__ import annotations

import argparse

from common import die, find_workspace, fmt_tc, read_json, say, video_dir, workspace_arg


def parse_t(s: str) -> float:
    parts = [float(p) for p in s.split(":")]
    t = 0.0
    for p in parts:
        t = t * 60 + p
    return t


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("clip")
    ap.add_argument("frm", nargs="?", type=int)
    ap.add_argument("to", nargs="?", type=int)
    ap.add_argument("--at")
    workspace_arg(ap)
    a = ap.parse_args()
    ws = find_workspace(a.workspace)
    toks = read_json(video_dir(ws, a.video) / "words" / f"{a.clip}.json")
    if toks is None:
        die(f"chưa có words/{a.clip}.json — chạy ingest.py trước")
    if a.at:
        t = parse_t(a.at)
        idx = min(range(len(toks)), key=lambda i: abs(toks[i]["start"] - t)) if toks else 0
        lo, hi = max(0, idx - 15), idx + 15
    else:
        lo = a.frm or 0
        hi = a.to if a.to is not None else lo + 60
    for t in toks[lo:hi + 1]:
        mark = "" if t["type"] == "word" else "  (event)"
        say(f"{t['i']:>6}  {fmt_tc(t['start'])}-{fmt_tc(t['end'])}  {t['text']}{mark}")


if __name__ == "__main__":
    main()
