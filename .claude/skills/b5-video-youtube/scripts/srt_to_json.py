#!/usr/bin/env python3
"""Chuyển phụ đề SRT thành mảng captions cho audiogram.json.

Dùng: python3 srt_to_json.py captions.srt [--offset -12.5] [--into audiogram.json]
--offset: cộng vào mọi mốc thời gian (khi đã cắt clip từ giữa tập).
--into: ghi vào khóa "captions" của file props; không có thì in JSON ra màn hình.
Muốn phụ đề sạch (bỏ ờ/à, nói lắp, một dòng ≤ 42 ký tự): tạo SRT bằng skill bien-tap (captions.py).
"""
import argparse, json, re
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("srt"); ap.add_argument("--offset", type=float, default=0.0); ap.add_argument("--into")
a = ap.parse_args()

def sec(tc):
    h, m, rest = tc.strip().replace(".", ",").split(":"); s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

caps = []
for block in re.split(r"\n\s*\n", Path(a.srt).read_text(encoding="utf-8-sig").strip()):
    lines = block.splitlines()
    i = next((k for k, l in enumerate(lines) if "-->" in l), None)
    if i is None:
        continue
    st, en = lines[i].split("-->")
    caps.append({"start": round(sec(st) + a.offset, 3), "end": round(sec(en) + a.offset, 3),
                 "text": " ".join(lines[i + 1:]).strip()})
caps = [c for c in caps if c["end"] > 0]
if a.into:
    p = Path(a.into); d = json.loads(p.read_text(encoding="utf-8")); d["captions"] = caps
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(caps)} dòng → {p}")
else:
    print(json.dumps(caps, ensure_ascii=False, indent=2))
