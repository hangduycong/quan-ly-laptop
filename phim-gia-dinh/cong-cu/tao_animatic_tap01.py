#!/usr/bin/env python3
"""Dựng animatic tập 1: mỗi cảnh một thẻ (khung 16:9 có hình bóng người theo cỡ cảnh, mô tả tiếng Việt,
mức rủi ro, phụ đề thoại), đúng thời lượng trong danh sách cảnh quay, kèm âm nền tổng hợp theo bối cảnh.
Không dùng dịch vụ trả phí; chỉ cần Python + Pillow + ffmpeg.

Chạy:  python3 phim-gia-dinh/cong-cu/tao_animatic_tap01.py [--out DUONG_DAN.mp4]
Mặc định ghi phim-gia-dinh/animatic/tap-01-animatic.mp4 (không commit vào git; chạy lại để tạo).
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from tap01_du_lieu import LOC, SCENES, SHOTS  # noqa: E402

W, H, FPS = 1280, 720, 24
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BAND_COLOR = {"Xanh": (70, 160, 95), "Vàng": (215, 165, 40), "Đỏ": (200, 60, 50)}
# màu nền khung theo bối cảnh (lạnh ở bệnh viện, ấm ở nhà, vàng đục ở trường gà)
TINT = {"bv_hanhlang": (58, 72, 78), "bv_phong": (62, 74, 80), "bv_hien": (52, 62, 70), "truongga": (60, 50, 30),
        "nha_san": (70, 66, 46), "nha_ban": (78, 58, 38), "nha_phongme": (48, 40, 34), "nha_sansau": (72, 74, 60)}
SIZE_H = {"extreme wide": 0.16, "wide": 0.42, "medium close": 1.25, "medium": 0.85, "extreme close": 2.6, "close": 1.7}
# âm nền: bộ lọc ffmpeg cho từng bối cảnh
AMB = {
    "bv_hanhlang": "anoisesrc=c=brown:a=0.02,lowpass=f=400[n];sine=f=100:sample_rate=48000,volume=0.015[h];[n][h]amix=inputs=2",
    "bv_phong": "anoisesrc=c=brown:a=0.02,lowpass=f=400[n];sine=f=100:sample_rate=48000,volume=0.012[h];[n][h]amix=inputs=2",
    "bv_hien": "anoisesrc=c=pink:a=0.25,highpass=f=300,lowpass=f=6000",
    "truongga": "anoisesrc=c=brown:a=0.35,bandpass=f=700:w=600,tremolo=f=0.7:d=0.6",
    "nha_san": "anoisesrc=c=pink:a=0.03,highpass=f=2000,lowpass=f=8000",
    "nha_ban": "anoisesrc=c=brown:a=0.01,lowpass=f=300[n];aevalsrc='0.25*sin(2*PI*1800*t)*exp(-60*mod(t\\,1))':s=48000[c];[n][c]amix=inputs=2",
    "nha_phongme": "anoisesrc=c=pink:a=0.06,highpass=f=300,lowpass=f=5000",
    "nha_sansau": "anoisesrc=c=pink:a=0.012,highpass=f=1500",
}


def table_rows():
    md = (HERE.parent / "tap" / "tap-01-danh-sach-canh-quay.md").read_text(encoding="utf-8")
    rows = {}
    for line in md.splitlines():
        m = re.match(r"^\| (\d\d) \| (\d+)s \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", line)
        if m:
            rows[int(m.group(1))] = {"beat": m.group(3), "noi_dung": m.group(4), "co": m.group(5), "rui_ro": m.group(6)}
    return rows


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def size_scale(framing):
    f = framing.lower()
    for k in ["extreme wide", "extreme close", "medium close", "close", "medium", "wide"]:
        if k in f:
            return SIZE_H[k]
    return 0.85


def silhouettes(d, box, n, scale, label):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    if n == 0:
        d.text((x0 + bw / 2, y0 + bh / 2), label, font=ImageFont.truetype(FONT_B, 22), fill=(230, 225, 210), anchor="mm")
        return
    col = (205, 200, 185)
    for k in range(n):
        cx = x0 + bw * (k + 1) / (n + 1)
        if scale < 0.8:  # toàn cảnh: cả người đứng trên đáy khung
            fig_h = bh * scale
            head_r = fig_h * 0.11
            head_cy = y1 - fig_h + head_r * 1.2
        else:  # trung cảnh trở vào: đầu ở khoảng một phần ba trên, chừa khoảng trống trên đầu
            head_r = bh * {0.85: 0.09, 1.25: 0.14, 1.7: 0.21, 2.6: 0.42}.get(scale, 0.12) / max(1, n * 0.6)
            head_cy = y0 + bh * 0.36
        body_top = head_cy + head_r * 1.1
        d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=col)
        d.rounded_rectangle([cx - head_r * 1.9, body_top, cx + head_r * 1.9, y1 + bh], radius=int(head_r), fill=col)


def card(shot, row, scene_name, sub, idx_in_scene, t0):
    i, d, loc, chars, framing, kf, mv, motif, dlg, ai = shot
    img = Image.new("RGB", (W, H), (18, 18, 20))
    dr = ImageDraw.Draw(img)
    f_s, f_m, f_b, f_t = (ImageFont.truetype(FONT, 18), ImageFont.truetype(FONT, 22),
                          ImageFont.truetype(FONT_B, 26), ImageFont.truetype(FONT_B, 30))
    dr.text((40, 26), "MÙA CUỐI CỦA MẸ · Tập 1: Về nhà", font=f_s, fill=(150, 150, 150))
    dr.text((40, 52), scene_name, font=f_t, fill=(240, 236, 225))
    tc = f"{int(t0 // 60)}:{int(t0 % 60):02d}"
    dr.text((W - 40, 30), f"Cảnh {i:02d} · {d}s · {tc}", font=f_b, fill=(240, 236, 225), anchor="ra")
    # khung 16:9
    box = (40, 110, 40 + 640, 110 + 360)
    names = {"minh": "Minh", "ba-thu": "Bà Thu", "nhung": "Nhung", "yen": "Yến", "trang": "Trang", "ong-hai": "Ông Hải", "thang": "Thắng"}
    label = "CHÈN CHI TIẾT" if "insert" in framing or "hand" in framing else "KHÔNG MẶT NGƯỜI"
    frame = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), TINT[loc])  # vẽ riêng rồi dán: hình bóng không tràn khung
    silhouettes(ImageDraw.Draw(frame), (0, 0, frame.width, frame.height), len(chars), size_scale(framing), label)
    img.paste(frame, box[:2])
    dr.rectangle(box, outline=(120, 120, 120), width=2)
    if chars:
        dr.text((box[0] + 10, box[3] - 30), " · ".join(names[c] for c in chars), font=f_s, fill=(255, 255, 255))
    if "push-in" in framing:
        dr.text((box[2] - 10, box[1] + 10), "↗ đẩy vào chậm", font=f_s, fill=(255, 220, 120), anchor="ra")
    elif "pan" in framing:
        dr.text((box[2] - 10, box[1] + 10), "→ lia theo", font=f_s, fill=(255, 220, 120), anchor="ra")
    if not ai:
        dr.text((box[0] + 10, box[1] + 10), "KHÔNG TẠO AI · đạo cụ / đồ họa", font=f_s, fill=(255, 150, 120))
    # cột phải: cỡ cảnh, beat, nội dung, rủi ro
    x, y, wcol = 710, 112, W - 750
    dr.text((x, y), row["co"], font=f_m, fill=(255, 220, 120))
    y += 34
    for ln in wrap(dr, row["beat"], f_s, wcol):
        dr.text((x, y), ln, font=f_s, fill=(170, 170, 170)); y += 24
    y += 8
    for ln in wrap(dr, row["noi_dung"], f_m, wcol)[:9]:
        dr.text((x, y), ln, font=f_m, fill=(235, 232, 222)); y += 30
    band = row["rui_ro"].split()[0]
    dr.rounded_rectangle([x, 440, x + 300, 470], radius=6, fill=BAND_COLOR.get(band, (90, 90, 90)))
    dr.text((x + 10, 445), "Rủi ro: " + row["rui_ro"], font=f_s, fill=(15, 15, 15))
    # phụ đề
    if sub:
        sp, text = sub
        lines = wrap(dr, f"{sp}: {text}", ImageFont.truetype(FONT_B, 30), W - 160)[:3]
        yy = H - 40 - 42 * len(lines)
        dr.rectangle([60, yy - 14, W - 60, H - 28], fill=(0, 0, 0))
        for ln in lines:
            dr.text((W / 2, yy), ln, font=ImageFont.truetype(FONT_B, 30), fill=(255, 255, 255), anchor="ma"); yy += 42

    # thanh tiến độ trong cảnh lớn
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(HERE.parent / "animatic" / "tap-01-animatic.mp4"))
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("thiếu ffmpeg")
    rows = table_rows()
    scene_of = {}
    for s0, s1, name in SCENES:
        for k in range(s0, s1 + 1):
            scene_of[k] = name
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        concat, t = [], 0.0
        n = 0
        for shot in SHOTS:
            i, d = shot[0], shot[1]
            dlg = shot[8]
            parts = [(None, d)] if not dlg else [((sp, tx), d / len(dlg)) for sp, tx in dlg]
            for sub, dur in parts:
                p = td / f"c{n:04d}.png"
                card(shot, rows[i], scene_of[i], sub, 0, t).save(p)
                concat.append(f"file '{p}'\nduration {dur:.4f}\n")
                n += 1
            t += d
        concat.append(f"file '{td / f'c{n - 1:04d}.png'}'\n")
        (td / "v.txt").write_text("".join(concat))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(td / "v.txt"),
                        "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-tune", "stillimage", "-crf", "24",
                        str(td / "video.mp4")], check=True)
        # âm nền theo từng cảnh, ghép liền
        alist = []
        for shot in SHOTS:
            i, d, loc = shot[0], shot[1], shot[2]
            wav = td / f"a{i:03d}.wav"
            fc = AMB[loc] + f",atrim=0:{d},afade=t=in:d=0.15,afade=t=out:st={max(0, d - 0.15)}:d=0.15,aformat=sample_rates=48000:channel_layouts=stereo[out]"
            # nguồn lavfi cần độ dài; dùng -t
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-t", str(d), "-i", "anullsrc=r=48000:cl=stereo",
                            "-filter_complex", fc.replace("anoisesrc=", f"anoisesrc=d={d}:r=48000:").replace("sine=", f"sine=d={d}:")
                            .replace("aevalsrc=", "aevalsrc=").replace(":s=48000[c]", f":s=48000:d={d}[c]"),
                            "-map", "[out]", "-c:a", "pcm_s16le", str(wav)], check=True)
            alist.append(f"file '{wav}'\n")
        (td / "a.txt").write_text("".join(alist))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(td / "a.txt"),
                        "-c:a", "pcm_s16le", str(td / "amb.wav")], check=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(td / "video.mp4"), "-i", str(td / "amb.wav"),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
                        "-movflags", "+faststart", str(out)], check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                         capture_output=True, text=True).stdout.strip()
    print(f"animatic: {out} · {float(dur):.1f}s (bảng: {sum(s[1] for s in SHOTS)}s) · {n} thẻ")


if __name__ == "__main__":
    main()
