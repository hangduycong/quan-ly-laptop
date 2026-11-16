#!/usr/bin/env python3
"""Ghép ảnh render Blender (trước / ba phần tư / sau / cận mặt) thành bảng nhân vật có nhãn.

Chạy:  python3 ghep_bang_nhan_vat.py RAW_DIR [OUT_DIR]
RAW_DIR chứa <khóa>_truoc.png, _ba-phan-tu.png, _sau.png, _mat.png do dung_nhan_vat_blender.py tạo.
Kết quả: OUT_DIR/<khóa>_bang.jpg (từng nhân vật) và OUT_DIR/tap01_dan-nhan-vat.jpg (tất cả).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

INFO = {
    "minh": ("Minh", "em út, 27 tuổi · cao 1,72 m", "sẹo 1,5 cm xuyên lông mày TRÁI · mắt một mí · áo khoác dạ đen dài tới gối"),
    "ba-thu": ("Bà Thu (Mẹ)", "58 tuổi · cao 1,52 m", "nốt ruồi nâu trên gò má PHẢI · tóc muối tiêu búi thấp · áo bà ba nâu nhạt"),
    "nhung": ("Nhung (chị Hai)", "36 tuổi · cao 1,60 m", "sẹo rỗ tròn ở chóp cằm · hàm vuông, lông mày đậm · sơ mi trắng xắn tay"),
    "yen": ("Yến (chị Ba)", "34 tuổi · cao 1,55 m", "nốt ruồi dưới mắt TRÁI · tóc dài kẹp càng cua · áo hồng, váy dài"),
    "trang": ("Trang (chị Tư)", "31 tuổi · cao 1,58 m", "mắt dài hẹp · tóc ngang vai · tạp dề xanh ngọc đeo ngoài áo trắng"),
    "ong-hai": ("Ông Hải", "62 tuổi · cao 1,68 m · hơi còng", "vết đồi mồi ở thái dương TRÁI · râu lún phún bạc · áo sơ mi xanh xám"),
    "thang": ("Thắng", "30 tuổi · cao 1,78 m", "sẹo mảnh ngang sống mũi · tóc vuốt dựng · dây chuyền vàng · áo thun đen"),
}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def sheet(raw: Path, key: str) -> Image.Image:
    name, line1, line2 = INFO[key]
    views = [Image.open(raw / f"{key}_{v}.png").convert("RGB") for v in ("truoc", "ba-phan-tu", "sau")]
    w, h = views[0].size
    face = Image.open(raw / f"{key}_mat.png").convert("RGB")
    face = face.resize((int(face.width * h / face.height), h))
    W = w * 3 + face.width
    img = Image.new("RGB", (W, h + 110), (24, 24, 26))
    x = 0
    for v in views + [face]:
        img.paste(v, (x, 70))
        x += v.width
    d = ImageDraw.Draw(img)
    d.text((24, 14), name, font=ImageFont.truetype(FONT_B, 32), fill=(245, 240, 228))
    d.text((24 + 40 + d.textlength(name, font=ImageFont.truetype(FONT_B, 32)), 22), line1, font=ImageFont.truetype(FONT, 20), fill=(200, 200, 190))
    for i, t in enumerate(("TRƯỚC", "BA PHẦN TƯ", "SAU", "CẬN MẶT")):
        d.text((i * w + 16, 76), t, font=ImageFont.truetype(FONT_B, 16), fill=(60, 60, 60))
    d.text((24, h + 78), line2, font=ImageFont.truetype(FONT, 20), fill=(220, 215, 200))
    return img


def main():
    raw = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "nhan-vat-3d" / "blender"
    out.mkdir(parents=True, exist_ok=True)
    sheets = []
    for key in INFO:
        im = sheet(raw, key)
        im.save(out / f"{key}_bang.jpg", quality=88)
        sheets.append(im)
    # bảng tổng: mỗi hàng một nhân vật (thu nhỏ)
    W = max(s.width for s in sheets)
    scale = 0.55
    rows = [s.resize((int(s.width * scale), int(s.height * scale))) for s in sheets]
    total = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), (24, 24, 26))
    y = 0
    for r in rows:
        total.paste(r, (0, y))
        y += r.height
    total.save(out / "tap01_dan-nhan-vat.jpg", quality=86)
    print(f"{len(sheets)} bảng + bảng tổng {total.size} → {out}")


if __name__ == "__main__":
    main()
