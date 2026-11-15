#!/usr/bin/env python3
"""Sinh prompt cho tập 1 từ tap01_du_lieu.py + chuoi_nhan_dang.py:
  - 8 prompt ảnh bối cảnh trống (GPT Image 2.5)
  - prompt keyframe cho từng cảnh tạo AI (GPT Image 2.5, có ảnh tham chiếu)
  - prompt chuyển động image-to-video cho từng cảnh (Kling 3.0, tắt âm thanh)
Kết quả: ../tap/tap-01-prompt-hinh-anh.md

Chạy: python3 phim-gia-dinh/cong-cu/tao_prompt_tap01.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chuoi_nhan_dang import IDS  # noqa: E402
from tap01_du_lieu import ANCHORS, END, LOC, SCENES, SHOTS  # noqa: E402

NAME = {"minh": "MINH", "ba-thu": "BÀ THU", "nhung": "NHUNG", "yen": "YẾN", "trang": "TRANG",
        "ong-hai": "ÔNG HẢI", "thang": "THẮNG"}
BANNED = re.compile(r"\b(cinematic|masterpiece|stunning|epic|4k|8k|ultra|hyper|flawless|perfect|sharp focus|crisp|"
                    r"beautiful lighting|dynamic camera|intense moment)\b", re.I)


def plate(key):
    vn, place, light, motif = LOC[key]
    return "\n".join([
        f"Scene: {place}",
        "Subject: the empty location itself, no people",
        f"Important Details: {light}; {motif}; real wear: scuffs, water stains, faded paint, dust in corners; "
        "a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour",
        "Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots",
        "Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, "
        "16:9 composition with the main action area left clear",
    ])


def keyframe(s):
    i, d, loc, chars, framing, kf, mv, motif, dlg, ai = s
    vn, place, light, lmotif = LOC[loc]
    refs = [f"Image 1: location plate `{loc}` — use for the room, perspective, light direction and colour; ignore any people in it"]
    for n, c in enumerate(chars, 2):
        refs.append(f"Image {n}: locked portrait of {NAME[c]} — use only face, hair and clothing; ignore its background and pose")
    subj = kf
    if chars:
        subj += ". " + " ".join(f"{IDS[c]}." for c in chars)
    count = len(chars)
    people = ("no faces visible" if count == 0 else
              ("exactly one person with a visible face" if count == 1 else
               f"exactly {count} people with visible faces, each appearing once"))
    return "\n".join([
        "References: " + "; ".join(refs),
        f"Scene: {place}; {light}",
        f"Subject: {subj}",
        f"Important Details: {framing}; first frame of the shot, before the action starts; {lmotif}; {motif}; "
        "a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, "
        "fabric creases, low contrast, muted colour",
        "Use Case: keyframe (first frame) for image-to-video generation, 16:9",
        f"Constraints: {people}; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; "
        "EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration",
    ])


def clauses(mv):
    return [c.strip() for c in re.split(r";|, then | and then ", mv) if c.strip()]


def motion(s):
    i, d, loc, chars, framing, kf, mv, motif, dlg, ai = s
    if "push-in" in framing:
        cam = "Slow push-in."
    elif "pan" in framing:
        cam = "Slow pan following the subject."
    else:
        cam = "Locked camera."
    acts = [c for c in clauses(mv) if not c.lower().startswith("the camera")]
    act = "; ".join(acts)
    act = act[0].upper() + act[1:]
    lines = ["Preserve faces, wardrobe, room and light from the image."]
    for k, c in enumerate(chars):
        lines.append(f"[Character {chr(65 + k)}: {NAME[c]}, as in the image]")
    talk = " Lips move with quiet speech." if dlg else ""
    lines.append(f"Shot (0-{d}s). {cam} {act}.{talk} Background: {LOC[loc][3]}.")
    lines.append(f"Ends on: {END.get(i, acts[-1])}.")
    lines.append("Audio: none.")
    lines.append("Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, "
                 "text, subtitles, watermark, jitter")
    return "\n".join(lines)


def main():
    out = ["# Prompt hình ảnh — Tập 1: Về nhà", "",
           "> Sinh tự động bởi `cong-cu/tao_prompt_tap01.py` từ `cong-cu/tap01_du_lieu.py` (93 cảnh, khớp `tap-01-danh-sach-canh-quay.md`) "
           "và `cong-cu/chuoi_nhan_dang.py`. Viết theo skill `mo-phong-cong-viec-dao-dien` (Visual Skills của **Serge Shima**, CC BY 4.0 — "
           "https://github.com/smixs/visual-skills) và `ho-tro-danh-sach-canh-quay` (DirectorSKILL). Sửa dữ liệu rồi chạy lại script; đừng sửa tay file này.", "",
           "## Quy trình", "",
           "1. **Ảnh bối cảnh trống** (mục A): GPT Image 2.5 Sunburst, `quality: medium`, `size: 1536x864`. Chọn một ảnh mỗi bối cảnh, dùng lại cho mọi cảnh.",
           "2. **Chân dung khóa nhận dạng**: theo `../nhan-vat-3d/prompt-anh-nhan-vat.md`.",
           "3. **Keyframe từng cảnh** (mục B): GPT Image 2.5 Sunburst chế độ edit, đính kèm đúng các ảnh tham chiếu ghi ở dòng `References`. "
           "`quality: medium`, `size: 1536x864`. Kiểm tra: đúng số người, dấu nhận dạng đúng chỗ, không có chữ.",
           "4. **Clip** (mục B, khối Kling): Kling 3.0 image-to-video, keyframe làm ảnh đầu, `duration` = số giây ghi ở cảnh (tối thiểu theo công cụ, cắt lại khi dựng), "
           "`aspect_ratio: 16:9`, `cfg_scale: 0.6`, **`generate_audio: false`**. Cảnh Vàng: tạo 2–3 bản, chọn một; Xanh: 1–2 bản.",
           "5. **Tiếng**: thu giọng diễn viên (hoặc lồng tiếng) theo thoại ghi ở từng cảnh; nhép môi khi dựng hoặc bằng chức năng lip-sync của công cụ nếu có. "
           "Không tin vào âm thanh do model video tự sinh cho tiếng Việt.",
           "6. **Dựng**: ghép theo thứ tự cảnh bằng skill `bien-tap` (phụ đề tiếng Việt, nhạc nền, chuẩn âm lượng).", "",
           "Cảnh **không tạo AI** (có chữ tiếng Việt trong khung): 02, 42, 72, 78, 79 — quay đạo cụ thật hoặc làm đồ họa khi dựng. "
           "Cảnh 47: bảng chỉ đường thêm khi dựng.", "",
           "## A. Ảnh bối cảnh trống (8)", ""]
    for k, v in LOC.items():
        out += [f"### `{k}` — {v[0]}", "", "```text", plate(k), "```", ""]
    out += ["## B. Keyframe + chuyển động theo từng cảnh", ""]
    words = []
    for a, b, name in SCENES:
        emo, mot, obj, brk, fin = ANCHORS[name]
        out += [f"### {name} (cảnh {a:02d}–{b:02d})", "",
                f"Năm điểm neo — cảm xúc: {emo} · mô-típ: {mot} · đồ vật: {obj} · điểm vỡ: {brk} · hình cuối: {fin}", ""]
        for s in SHOTS:
            if not a <= s[0] <= b:
                continue
            i, d, loc, chars, framing, kf, mv, motif, dlg, ai = s
            head = f"#### {i:02d} · {d}s · {', '.join(NAME[c] for c in chars) or 'không mặt người'}"
            out += [head, ""]
            if dlg:
                out += ["Thoại (thu riêng): " + " / ".join(f"**{sp}:** {t}" for sp, t in dlg), ""]
            if not ai:
                out += [f"*Không tạo AI* — {kf}. Làm bằng đạo cụ thật hoặc đồ họa khi dựng.", ""]
                continue
            k, m = keyframe(s), motion(s)
            words.append((i, len(" ".join(l for l in m.splitlines() if not l.startswith("Negative")).split())))
            out += ["Keyframe (GPT Image 2.5):", "", "```text", k, "```", "", "Chuyển động (Kling 3.0, image-to-video):", "", "```text", m, "```", ""]
    out += ["## Kiểm tra trước khi tạo", "",
            "- Mỗi cảnh AI có đủ ba chi tiết: áp lực môi trường (dòng Scene / chi tiết bối cảnh), cử động trên cơ thể (dòng hành động), mô-típ (Important Details).",
            "- Mỗi clip có một chuyển động máy và một hành động chính, kết thúc bằng dòng `Ends on`.",
            "- Chuỗi nhận dạng được chép nguyên văn từ `chuoi_nhan_dang.py`; không sửa trong file này.",
            "- Đổi model khác (Veo, Seedance): giữ keyframe, viết lại khối chuyển động theo file model tương ứng trong skill `mo-phong-cong-viec-dao-dien`.", ""]
    text = "\n".join(out)
    bad = BANNED.findall(text.split("## A.")[1])
    dst = HERE.parent / "tap" / "tap-01-prompt-hinh-anh.md"
    dst.write_text(text, encoding="utf-8")
    print(f"{dst.name}: {len(LOC)} bối cảnh, {len(words)} cảnh AI; từ cấm: {bad or 'không'}; "
          f"độ dài prompt chuyển động (không tính negative) {min(w for _, w in words)}–{max(w for _, w in words)} từ")


if __name__ == "__main__":
    main()
