#!/usr/bin/env python3
"""Clean, one-line captions (SRT) on the OUTPUT timeline, from the verbatim transcript.

Cleans: stutters ("pro-product" -> "product"), cut-off words ("es--"), filler sounds (per language,
config captions.fillers), global word/phrase maps (config captions.standard_language) and per-video
fixes (system/videos/<v>/caption_fixes.json: {"words": {...}, "phrases": {...}}, phrases applied last).
Lines: max 42 chars (a sentence's last word may stretch to ~50), new cue at a pause >= 0.6 s, at a
sentence end once the line is substantial, or after 3.2 s; min 0.9 s on screen; end 0.25 s after
the last word; never overlapping; a lone small word after a pause joins the next line.
Words on B-roll are dropped. Every cue is printed: READ THEM ALL before handing the file over.

Usage:
  python3 captions.py <video>                    from cuts.json -> captions/captions_vN.srt
  python3 captions.py <video> --render FILE.mp4  map onto that render's cuts (renders/<name>.cuts.json)
  python3 captions.py <video> --resolve          first cue starts at 00:00:00,000 (DaVinci import quirk)
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import (die, find_workspace, load_config, next_version, read_json, say, srt_tc,
                    video_dir, workspace_arg)

LANG3 = {"eng": "en", "vie": "vi", "por": "pt", "spa": "es", "fra": "fr", "deu": "de"}
END = re.compile(r"[.!?…]['\")\]]*$")
PUNCT = "\"'“”‘’()[]{}.,!?…:;"


def split_punct(w: str) -> tuple[str, str, str]:
    i, j = 0, len(w)
    while i < j and w[i] in PUNCT:
        i += 1
    while j > i and w[j - 1] in PUNCT:
        j -= 1
    return w[:i], w[i:j], w[j:]


def clean_word(w: str, fillers: set, wmap: dict) -> str | None:
    pre, core, post = split_punct(w)
    if not core:
        return None
    if core.endswith("-") or core.endswith("–"):
        return None  # cut-off word
    m = re.fullmatch(r"(\w+)-(\w[\w'-]*)", core)
    if m and (m.group(2).casefold().startswith(m.group(1).casefold()) or m.group(1).casefold() == m.group(2).casefold()):
        core = m.group(2)  # stutter
    low = core.casefold()
    collapsed = re.sub(r"(.)\1{2,}", r"\1", low)
    if low in fillers or collapsed in fillers or re.fullmatch(r"(.)\1{2,}", low):
        return None
    if low in wmap:
        rep = wmap[low]
        core = rep[:1].upper() + rep[1:] if core[:1].isupper() else rep
    return pre + core + post


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--render", help="file render (để dùng đúng cuts của bản đó)")
    ap.add_argument("--resolve", action="store_true")
    ap.add_argument("--language", help="vi/en/pt… (mặc định: theo transcript)")
    workspace_arg(ap)
    a = ap.parse_args()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    if a.render:
        rp = Path(a.render)
        rp = rp if rp.is_absolute() else (vd / "renders" / rp.name)
        plan = read_json(rp.with_suffix(".cuts.json")) or die(f"không có {rp.with_suffix('.cuts.json').name}")
    else:
        plan = read_json(vd / "cuts.json") or die("chưa có cuts.json — chạy plan.py")
    cc = cfg["captions"]
    fixes = read_json(vd / "caption_fixes.json", {}) or {}
    wmap = {k.casefold(): v for k, v in {**cc["standard_language"].get("words", {}), **fixes.get("words", {})}.items()}
    phrases = {**cc["standard_language"].get("phrases", {}), **fixes.get("phrases", {})}
    lang = a.language
    words: list[dict] = []
    cache: dict = {}
    for p in plan["pieces"]:
        if p["kind"] != "speech":
            continue
        cid = p["clip"]
        if cid not in cache:
            cache[cid] = read_json(vd / "words" / f"{cid}.json", []) or []
            if not lang:
                raw = read_json(vd / "transcripts" / f"{cid}.json", {}) or {}
                lc = raw.get("language_code") or ""
                lang = LANG3.get(lc, lc[:2]) or None
        for t in cache[cid]:
            mid = (t["start"] + t["end"]) / 2
            if t["type"] != "word" or not (p["start"] <= mid < p["end"]):
                continue
            off = p["out_start"] - p["start"]
            words.append({"text": t["text"], "start": max(p["out_start"], t["start"] + off),
                          "end": min(p["out_start"] + p["frames"] / float(plan["fps_float"]), t["end"] + off)})
    fillers = {f.casefold() for f in cc["fillers"].get(lang or "", [])}
    cleaned = []
    prev_end = None  # end of the previous ORIGINAL word: a removed filler is speech, not a pause
    for w in words:
        txt = clean_word(w["text"], fillers, wmap)
        if txt:
            cleaned.append(dict(w, text=txt, gap_before=(w["start"] - prev_end) if prev_end is not None else 99))
        prev_end = w["end"]
    # cues
    cues: list[dict] = []
    cur: list[dict] = []

    def text_of(ws_):
        return " ".join(x["text"] for x in ws_)

    for w in cleaned:
        if cur:
            gap = min(w["gap_before"], w["start"] - cur[-1]["end"])
            line = text_of(cur)
            new_len = len(line) + 1 + len(w["text"])
            too_long = new_len > cc["chars_per_line"] and not (END.search(w["text"]) and new_len <= cc["stretch_to"])
            if (gap >= cc["pause_split"] or too_long or (END.search(cur[-1]["text"]) and len(line) >= 20)
                    or (w["end"] - cur[0]["start"] > cc["max_cue"]
                        and not (END.search(w["text"]) and new_len <= cc["stretch_to"]
                                 and w["end"] - cur[0]["start"] <= cc["max_cue"] + 1.0))):
                cues.append({"words": cur, "pause_after": gap})
                cur = []
        cur.append(w)
    if cur:
        cues.append({"words": cur, "pause_after": 99})
    # lone small word after a pause joins the next line
    merged: list[dict] = []
    i = 0
    while i < len(cues):
        c = cues[i]
        if (len(c["words"]) == 1 and len(c["words"][0]["text"].strip(PUNCT)) <= 5 and not END.search(c["words"][0]["text"])
                and i + 1 < len(cues) and c["pause_after"] < 1.2
                and len(text_of(c["words"] + cues[i + 1]["words"])) <= cc["stretch_to"]):
            cues[i + 1]["words"] = c["words"] + cues[i + 1]["words"]
        else:
            merged.append(c)
        i += 1
    out = []
    for c in merged:
        txt = text_of(c["words"])
        for k, v in phrases.items():
            txt = txt.replace(k, v)
        txt = re.sub(r"\s+([,.!?…:;])", r"\1", txt).strip()
        if txt:
            out.append({"start": c["words"][0]["start"], "end": c["words"][-1]["end"] + cc["end_after_word"], "text": txt})
    for k, c in enumerate(out):
        c["end"] = max(c["end"], c["start"] + cc["min_cue"])
        if k + 1 < len(out):
            c["end"] = min(c["end"], out[k + 1]["start"] - 0.04)
    if a.resolve and out:
        out[0]["start"] = 0.0
    if not out:
        die("không có từ nào để làm phụ đề (toàn B-roll?)")
    dst = next_version(vd / "captions", "captions", ".srt")
    dst.write_text("".join(f"{k}\n{srt_tc(c['start'])} --> {srt_tc(c['end'])}\n{c['text']}\n\n"
                           for k, c in enumerate(out, 1)), encoding="utf-8")
    say(f"{dst.relative_to(ws)}: {len(out)} dòng, ngôn ngữ {lang or '?'} — ĐỌC HẾT từng dòng dưới đây:")
    issues = []
    for k, c in enumerate(out, 1):
        say(f"{k:>4} {srt_tc(c['start'])}  {c['text']}")
        if re.search(r"([,.!?])\1", c["text"]) or ",." in c["text"]:
            issues.append(f"#{k} dấu câu lặp")
        if re.search(r"[.!?] [a-zà-ỹ]", c["text"]):
            issues.append(f"#{k} chữ thường sau dấu chấm")
        if len(c["text"]) > cc["stretch_to"]:
            issues.append(f"#{k} dài {len(c['text'])} ký tự")
    say("cần sửa: " + ("; ".join(issues) if issues else "không thấy lỗi tự động (vẫn phải đọc)"))


if __name__ == "__main__":
    main()
