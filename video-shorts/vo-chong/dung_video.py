#!/usr/bin/env python3
"""Dựng Shorts 30 giây 1080x1920 "3 câu nói giữ lửa hôn nhân".
Đầu vào: loi-doc.txt, giong.mp3, moc-thoi-gian.json (mốc từng ký tự từ ElevenLabs).
Chạy: python3 dung_video.py  → shorts-vo-chong-30s.mp4 (cần Pillow, numpy, ffmpeg)."""
import json, math, random, subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H, FPS, DUR = 1080, 1920, 30, 30.0
OFFSET = 0.5  # giọng đọc vào sau 0.5 giây
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

text = (HERE / "loi-doc.txt").read_text(encoding="utf-8").strip()
al = json.loads((HERE / "moc-thoi-gian.json").read_text())
cs = [t + OFFSET for t in al["character_start_times_seconds"]]
ce = [t + OFFSET for t in al["character_end_times_seconds"]]
AUDIO_END = ce[-1]

# từ + mốc thời gian
words, i = [], 0
for part in text.replace("\n", " ").split(" "):
    j = text.find(part, i)
    if part:
        words.append((part, cs[j], ce[j + len(part) - 1], j))
    i = j + len(part)


def at(anchor):
    return cs[text.find(anchor)]


# cảnh: (mốc bắt đầu, màu nền trên, màu nền dưới, nội dung)
SC = [
    (0.0, (58, 18, 44), (150, 52, 84), dict(kind="hook")),
    (at("Ba câu nói") - 0.15, (30, 22, 66), (122, 56, 130), dict(kind="title")),
    (at("Một:") - 0.15, (62, 20, 40), (176, 70, 82), dict(num="1", quote="“Anh nghe em\nnói đây.”", sub="Lắng nghe trước khi phản bác")),
    (at("Hai:") - 0.15, (20, 40, 70), (62, 120, 150), dict(num="2", quote="“Cảm ơn em\nhôm nay.”", sub="Lời cảm ơn nhỏ nuôi sống tình yêu lớn")),
    (at("Ba:") - 0.15, (54, 30, 24), (190, 112, 70), dict(num="3", quote="“Mình cùng\ngiải quyết nhé.”", sub="Là đồng đội, không phải đối thủ")),
    (at("Hôm nay") - 0.15, (58, 18, 44), (170, 56, 96), dict(kind="cta")),
]
SC.append((DUR, None, None, None))

random.seed(7)
HEARTS = [dict(x=random.uniform(0, W), y=random.uniform(0, H), s=random.uniform(18, 54), v=random.uniform(40, 110),
               ph=random.uniform(0, 6.28), a=random.uniform(0.10, 0.28)) for _ in range(22)]


def font(p, s):
    return ImageFont.truetype(p, s)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def gradient(top, bot, t):
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    y = np.clip(y + 0.06 * math.sin(t * 0.8), 0, 1)
    top, bot = np.array(top, np.float32), np.array(bot, np.float32)
    col = top[None, :] * (1 - y) + bot[None, :] * y
    return Image.fromarray(np.repeat(col[:, None, :], W, axis=1).astype(np.uint8), "RGB")


def heart(d, cx, cy, s, fill):
    pts = []
    for k in range(60):
        a = k / 60 * 2 * math.pi
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * s / 16, cy + y * s / 16))
    d.polygon(pts, fill=fill)


def text_c(d, xy, s, f, fill, alpha=1.0, spacing=14, stroke=0):
    """Chữ căn giữa nhiều dòng; alpha áp bằng cách trộn màu với nền không có nên dùng lớp RGBA."""
    d.multiline_text(xy, s, font=f, fill=fill + (int(255 * alpha),), anchor="ma", align="center", spacing=spacing,
                     stroke_width=stroke, stroke_fill=(0, 0, 0, int(120 * alpha)))


def draw_scene(img, sc, t, t0):
    k = t - t0
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    p = ease(k / 0.45)
    dy = int((1 - p) * 60)
    cx = W // 2
    kind = sc.get("kind")
    if kind == "hook":
        text_c(d, (cx, 520 + dy), "CÃI NHAU", font(FB, 150), (255, 255, 255), p)
        text_c(d, (cx, 690 + dy), "KHÔNG ĐÁNG SỢ", font(FB, 92), (255, 226, 232), p)
        p2 = ease((k - 1.6) / 0.5)
        d.rounded_rectangle((90, 950, W - 90, 1190), 40, fill=(255, 255, 255, int(235 * p2)))
        text_c(d, (cx, 975 + int((1 - p2) * 40)), "ĐÁNG SỢ LÀ", font(FB, 76), (140, 40, 70), p2)
        text_c(d, (cx, 1062 + int((1 - p2) * 40)), "IM LẶNG", font(FB, 112), (200, 30, 80), p2)
    elif kind == "title":
        text_c(d, (cx, 520 + dy), "3 CÂU NÓI", font(FB, 170), (255, 255, 255), p)
        text_c(d, (cx, 740 + dy), "GIỮ LỬA", font(FB, 150), (255, 214, 224), ease((k - 0.2) / 0.45))
        text_c(d, (cx, 910 + dy), "HÔN NHÂN", font(FB, 150), (255, 214, 224), ease((k - 0.4) / 0.45))
    elif kind == "cta":
        text_c(d, (cx, 480 + dy), "HÔM NAY", font(FB, 130), (255, 255, 255), p)
        text_c(d, (cx, 640 + dy), "HÃY NÓI MỘT CÂU", font(FB, 92), (255, 226, 232), ease((k - 0.2) / 0.45))
        text_c(d, (cx, 760 + dy), "VỚI NGƯỜI ẤY", font(FB, 92), (255, 226, 232), ease((k - 0.35) / 0.45))
        p2 = ease((k - 1.4) / 0.5)
        d.rounded_rectangle((120, 1000, W - 120, 1240), 120, fill=(255, 255, 255, int(235 * p2)))
        text_c(d, (cx, 1040), "LƯU LẠI", font(FB, 84), (200, 30, 80), p2)
        text_c(d, (cx, 1136), "& GỬI CHO NỬA KIA", font(FB, 58), (140, 40, 70), p2)
        heart(d, cx, 1400 + 12 * math.sin(k * 4), 150 + 8 * math.sin(k * 4), (255, 255, 255, int(235 * p2)))
    else:
        r = 96
        pc = ease(k / 0.35)
        d.ellipse((cx - r, 392 - r, cx + r, 392 + r), fill=(255, 255, 255, int(235 * pc)))
        d.text((cx, 392), sc["num"], font=font(FB, 130), fill=(190, 40, 80, int(255 * pc)), anchor="mm")
        text_c(d, (cx, 640 + dy), sc["quote"], font(FB, 112), (255, 255, 255), p, spacing=22, stroke=2)
        p3 = ease((k - 0.7) / 0.5)
        d.rounded_rectangle((70, 1070, W - 70, 1230), 40, fill=(0, 0, 0, int(80 * p3)))
        text_c(d, (cx, 1105 + int((1 - p3) * 30)), sc["sub"], font(FR, 50), (255, 244, 246), p3)
    img.alpha_composite(ov)


def draw_caption(img, t):
    """Phụ đề bám theo giọng: hiện nhóm ~4 từ, từ đang đọc tô vàng."""
    idx = None
    for n, (w, a, b, _) in enumerate(words):
        if a - 0.05 <= t <= b + 0.25:
            idx = n
            break
    if idx is None:
        return
    g0 = (idx // 4) * 4
    grp = words[g0:g0 + 4]
    f = font(FB, 74)
    d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    ws = [d0.textlength(w + " ", font=f) for w, *_ in grp]
    total = sum(ws)
    x = (W - total) / 2
    y = 1540
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle((x - 34, y - 22, x + total + 24, y + 118), 36, fill=(0, 0, 0, 120))
    for n, (w, a, b, _) in enumerate(grp):
        on = (g0 + n) == idx
        d.text((x, y), w, font=f, fill=(255, 214, 64, 255) if on else (255, 255, 255, 255), stroke_width=3,
               stroke_fill=(0, 0, 0, 200))
        x += ws[n]
    img.alpha_composite(ov)


def frame(t):
    # cảnh hiện tại
    n = max(i for i, s in enumerate(SC[:-1]) if s[0] <= t)
    t0, top, bot, sc = SC[n]
    # chuyển cảnh mượt: trộn màu nền với cảnh trước trong 0.35s
    if n > 0 and t - t0 < 0.35:
        q = (t - t0) / 0.35
        pt, pb = SC[n - 1][1], SC[n - 1][2]
        top = tuple(pt[i] * (1 - q) + top[i] * q for i in range(3))
        bot = tuple(pb[i] * (1 - q) + bot[i] * q for i in range(3))
    img = gradient(top, bot, t).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for h in HEARTS:
        y = (h["y"] - h["v"] * t) % (H + 120) - 60
        x = h["x"] + 28 * math.sin(t * 0.9 + h["ph"])
        heart(d, x, y, h["s"], (255, 255, 255, int(255 * h["a"])))
    img.alpha_composite(ov)
    draw_scene(img, sc, t, t0)
    draw_caption(img, t)
    # mờ dần vào / ra
    f = min(1.0, t / 0.3, (DUR - t) / 0.4)
    if f < 1:
        black = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - f))))
        img.alpha_composite(black)
    return img.convert("RGB")


def main():
    out = HERE / "shorts-vo-chong-30s.mp4"
    music = HERE / "nhac-nen.wav"
    # nhạc nền tổng hợp: hợp âm Am-F-C-G êm, tremolo nhẹ
    chords = [(220.00, 261.63, 329.63), (174.61, 220.00, 261.63), (261.63, 329.63, 392.00), (196.00, 246.94, 293.66)]
    sr = 44100
    n = int(sr * DUR)
    tt = np.arange(n) / sr
    sig = np.zeros(n, np.float32)
    seg = DUR / 4
    for ci, ch in enumerate(chords):
        a, b = int(ci * seg * sr), int(min((ci + 1) * seg, DUR) * sr)
        local = tt[a:b] - tt[a]
        env = np.minimum(1, local / 0.8) * np.minimum(1, (seg - local) / 0.8)
        for fq in ch:
            sig[a:b] += (np.sin(2 * np.pi * fq * local) + 0.3 * np.sin(2 * np.pi * 2 * fq * local)).astype(np.float32) * env
    sig *= (0.8 + 0.2 * np.sin(2 * np.pi * 0.35 * tt))
    sig = sig / np.abs(sig).max() * 0.5
    import wave
    with wave.open(str(music), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((sig * 32767).astype(np.int16).tobytes())

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", str(HERE / "giong.mp3"), "-i", str(music),
           "-filter_complex",
           f"[1:a]adelay={int(OFFSET*1000)}|{int(OFFSET*1000)},apad,atrim=0:{DUR}[v];"
           f"[2:a]volume=0.16,afade=t=in:d=1,afade=t=out:st={DUR-1.5}:d=1.5[m];"
           f"[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-t", str(DUR), "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)):
        p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close()
    p.wait()
    print("xong", out, p.returncode)


if __name__ == "__main__":
    main()
