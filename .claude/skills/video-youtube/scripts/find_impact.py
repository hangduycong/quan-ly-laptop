#!/usr/bin/env python3
"""Tìm thời điểm tiếng "hit" (đỉnh mạnh nhất) trong file sting để logo bật lên đúng khung đó.

Dùng:
  python3 find_impact.py sting.mp3 [--fps 30] [--props brand.json]
  --props: ghi luôn giá trị vào khóa "impact" của file props (Remotion --props).
Cách tính: giải mã mono 8 kHz, năng lượng theo cửa sổ 10 ms, lấy cửa sổ có độ TĂNG năng lượng lớn nhất
(transient) trong vùng đỉnh; in thời điểm (giây) và số khung.
"""
import argparse, array, json, subprocess, sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("audio"); ap.add_argument("--fps", type=float, default=30); ap.add_argument("--props")
a = ap.parse_args()
raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", a.audio, "-ac", "1", "-ar", "8000",
                      "-f", "s16le", "-"], stdout=subprocess.PIPE, check=True).stdout
s = array.array("h"); s.frombytes(raw[: len(raw) // 2 * 2])
if not s:
    sys.exit("file không có âm thanh")
W = 80  # 10 ms
env = [sum(x * x for x in s[i:i + W]) / W for i in range(0, len(s) - W, W)]
peak = max(env)
# transient: cửa sổ đầu tiên vượt 50% đỉnh với bước nhảy năng lượng lớn nhất trong 100 ms quanh đó
cands = [i for i, e in enumerate(env) if e >= 0.5 * peak]
best = max(cands, key=lambda i: env[i] - (env[i - 1] if i else 0))
t = round(best * W / 8000, 3)
frame = round(t * a.fps)
print(f"impact ≈ {t}s → khung {frame} @ {a.fps:g} fps (đỉnh năng lượng ở {round(env.index(peak) * W / 8000, 3)}s)")
if a.props:
    p = Path(a.props); d = json.loads(p.read_text(encoding="utf-8")); d["impact"] = t
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"đã ghi impact={t} vào {p}")
