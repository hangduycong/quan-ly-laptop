#!/usr/bin/env python3
"""Ghép ảnh bố cục 3D tập 1 thành các bảng theo cảnh (mỗi ảnh có số cảnh quay) để xem nhanh.

Chạy: python3 ghep_bang_canh_3d.py [THU_MUC_ANH] [THU_MUC_RA]
Mặc định: tap/hinh-3d-tap01 → cùng thư mục, file bang-canh-<n>.jpg
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from tap01_du_lieu import SCENES  # noqa: E402

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "tap" / "hinh-3d-tap01"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src
    cols, tw = 3, 480
    th = tw * 9 // 16
    f = ImageFont.truetype(FONT_B, 18)
    done = 0
    for n, (a, b, name) in enumerate(SCENES, 1):
        files = [(i, src / f"{i:02d}.jpg") for i in range(a, b + 1) if (src / f"{i:02d}.jpg").exists()]
        if not files:
            continue
        rows = (len(files) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * (th + 26) + 44), (22, 22, 24))
        d = ImageDraw.Draw(sheet)
        d.text((12, 10), name, font=ImageFont.truetype(FONT_B, 22), fill=(245, 240, 228))
        for k, (i, p) in enumerate(files):
            x, y = (k % cols) * tw, 44 + (k // cols) * (th + 26)
            sheet.paste(Image.open(p).convert("RGB").resize((tw, th)), (x, y + 24))
            d.text((x + 8, y + 2), f"Cảnh quay {i:02d}", font=f, fill=(255, 220, 120))
        sheet.save(out / f"bang-canh-{n}.jpg", quality=86)
        done += len(files)
    print(f"{done} ảnh → {len(SCENES)} bảng trong {out}")


if __name__ == "__main__":
    main()
