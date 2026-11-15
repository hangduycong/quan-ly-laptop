#!/usr/bin/env python3
"""Turn keep.json (+ moments.json) into frame-exact cuts: pads, silence-refined edges, scene room,
pause shortening, jump-cut zoom alternation, punch-ins, markers. Writes cuts.json + review.md.

Usage:
  python3 plan.py <video>                  plan from system/videos/<video>/keep.json
  python3 plan.py <video> --pause-report   what-if table for max_pause, writes nothing

keep.json  (word indices are inclusive; see references/rough-cut.md)
  {"segments": [{"clip": "C0001", "from": 12, "to": 57, "why": "...", "lead_in": 0.8, "tail": 1.0},
                {"clip": "C0002", "broll": true, "in": 0.0, "out": 4.0, "why": "...", "gain_db": -8}],
   "flags": [{"clip": "C0001", "at": 141, "note": "..."}], "summary": "..."}
moments.json
  {"moments": [{"type": "note", "clip": "C0001", "from": 1964, "to": 1994, "label": "...", "note": "..."},
               {"type": "punch", "clip": "C0001", "from": 812, "to": 818, "label": "..."}]}
"""
from __future__ import annotations

import argparse
from fractions import Fraction

from common import (die, find_workspace, fmt_tc, frame_ceil, frame_floor, load_config, read_json,
                    say, video_dir, workspace_arg, write_json)


# --------------------------------------------------------------- helpers ----
def coverage(sil: list, a: float, b: float) -> float:
    if b <= a:
        return 0.0
    tot = sum(max(0.0, min(b, e) - max(a, s)) for s, e in sil)
    return tot / (b - a)


def silence_end_before(sil: list, t: float, window: float) -> float | None:
    best = None
    for s, e in sil:
        if t - window <= e <= t:
            best = e if best is None else max(best, e)
    return best


def silence_start_after(sil: list, t: float, window: float) -> float | None:
    best = None
    for s, e in sil:
        if t <= s <= t + window:
            best = s if best is None else min(best, s)
    return best


class Clip:
    def __init__(self, entry: dict, toks: list, sil: list):
        self.id = entry["id"]
        self.entry = entry
        self.dur = float(entry["probe"]["duration"])
        self.toks = toks
        self.sil = sil
        self.spoken = [t for t in toks if t["type"] == "word"]

    def prev_spoken_end(self, i: int) -> float | None:
        prev = [t for t in self.spoken if t["i"] < i]
        return prev[-1]["end"] if prev else None

    def next_spoken_start(self, i: int) -> float | None:
        nxt = [t for t in self.spoken if t["i"] > i]
        return nxt[0]["start"] if nxt else None


def speech_pieces(clip: Clip, seg: dict, scene_first: bool, scene_last: bool, c: dict,
                  max_pause: float, pause_keep: float, pauses: bool) -> tuple[list[dict], int]:
    lo, hi = int(seg["from"]), int(seg["to"])
    if lo > hi or lo < 0 or hi >= len(clip.toks):
        die(f"{clip.id}: khoảng từ {lo}-{hi} không hợp lệ (clip có {len(clip.toks)} token)")
    rng = clip.toks[lo:hi + 1]
    sp = [t for t in rng if t["type"] == "word"] or rng
    first, last = sp[0], sp[-1]
    pe, ns = clip.prev_spoken_end(lo), clip.next_spoken_start(hi)
    # start edge
    if scene_first:
        s = first["start"] - float(seg.get("lead_in", c["scene_lead_in"]))
    else:
        s = first["start"] - c["pre_pad"]
        se = silence_end_before(clip.sil, first["start"], c["onset_window"])
        if se is not None:
            s = min(s, se)
    if pe is not None:
        s = max(s, pe + 0.02)
    s = max(0.0, s)
    # end edge
    if scene_last:
        e = last["end"] + float(seg.get("tail", c["scene_tail"]))
    else:
        e = last["end"] + c["post_pad"]
        ss = silence_start_after(clip.sil, last["end"], c["offset_window"])
        if ss is not None:
            e = max(e, ss)
    if ns is not None:
        e = min(e, ns - 0.02)
    e = min(clip.dur, e)
    # pause shortening inside the range
    cuts, n_pause = [], 0
    if pauses:
        for a, b in zip(sp, sp[1:]):
            gap = b["start"] - a["end"]
            if gap > max_pause and gap >= c["silence_min"] and coverage(clip.sil, a["end"], b["start"]) >= c["silence_cover"]:
                ce = a["end"] + max(c["post_pad"], 0.4 * pause_keep)
                cs = b["start"] - max(c["pre_pad"], 0.6 * pause_keep)
                if cs > ce:
                    cuts.append((ce, cs, a["i"], b["i"]))
                    n_pause += 1
    pieces, cur_s, cur_lo = [], s, lo
    for ce, cs, ai, bi in cuts:
        pieces.append({"start": cur_s, "end": ce, "w": [cur_lo, ai]})
        cur_s, cur_lo = cs, bi
    pieces.append({"start": cur_s, "end": e, "w": [cur_lo, hi]})
    for k, p in enumerate(pieces):
        p["join"] = "pause" if k > 0 else None
    return pieces, n_pause


def build(ws, video: str, cfg: dict, max_pause=None, pause_keep=None, quiet=False) -> dict:
    vd = video_dir(ws, video, cfg)
    man = read_json(vd / "manifest.json") or die("chưa có manifest.json — chạy ingest.py")
    keep = read_json(vd / "keep.json") or die("chưa có keep.json — viết nó theo references/rough-cut.md")
    moments = (read_json(vd / "moments.json", {}) or {}).get("moments", [])
    c = cfg["cut"]
    max_pause = c["max_pause"] if max_pause is None else max_pause
    pause_keep = c["pause_keep"] if pause_keep is None else pause_keep
    entries = {e["id"]: e for e in man["clips"]}
    clips: dict[str, Clip] = {}

    def get_clip(cid: str) -> Clip:
        if cid not in clips:
            if cid not in entries:
                die(f"keep.json nhắc clip '{cid}' không có trong manifest")
            clips[cid] = Clip(entries[cid], read_json(vd / "words" / f"{cid}.json", []) or [],
                              read_json(vd / "silences" / f"{cid}.json", []) or [])
        return clips[cid]

    # timeline format
    tl = cfg["timeline"]
    guess = man.get("timeline_guess") or {}
    fps = Fraction(str(tl["fps"])) if tl.get("fps") else (Fraction(guess["fps"]) if guess.get("fps") else None)
    if not fps:
        die("không xác định được fps timeline — settings.py <v> set timeline.fps=\"30\"")
    width = int(tl.get("width") or guess.get("width") or 1920)
    height = int(tl.get("height") or guess.get("height") or 1080)
    width, height = width - width % 2, height - height % 2
    segs = keep.get("segments", [])
    if not segs:
        die("keep.json không có segment nào")
    used = {s["clip"] for s in segs}
    if not tl.get("fps"):
        bad = sorted({cid for cid in used if entries.get(cid, {}).get("probe", {}).get("fps")
                      and Fraction(entries[cid]["probe"]["fps"]) != fps})
        if bad:
            die(f"frame rate lệch với timeline ({float(fps):.3f}): {', '.join(bad)}. HỎI người dùng chọn fps, "
                "rồi settings.py <v> set timeline.fps=\"<fps>\". Không tự chọn.")
    # speech/broll pieces in keep order
    pieces: list[dict] = []
    n_pause = 0
    for k, seg in enumerate(segs):
        clip = get_clip(seg["clip"])
        if seg.get("broll"):
            s, e = max(0.0, float(seg["in"])), min(clip.dur, float(seg["out"]))
            if e <= s:
                die(f"B-roll {clip.id}: in/out không hợp lệ")
            pieces.append({"clip": clip.id, "kind": "broll", "start": s, "end": e, "w": None,
                           "join": None, "why": seg.get("why", ""), "gain_db": float(seg.get("gain_db", 0)),
                           "seg": k})
            continue
        prev = segs[k - 1] if k > 0 else None
        nxt = segs[k + 1] if k + 1 < len(segs) else None
        scene_first = not prev or prev.get("broll") or prev["clip"] != seg["clip"]
        scene_last = not nxt or nxt.get("broll") or nxt["clip"] != seg["clip"]
        ps, np_ = speech_pieces(clip, seg, scene_first, scene_last, c, max_pause, pause_keep,
                                bool(c["pauses_enabled"]))
        n_pause += np_
        for j, p in enumerate(ps):
            p.update({"clip": clip.id, "kind": "speech", "why": seg.get("why", "") if j == 0 else "",
                      "gain_db": float(seg.get("gain_db", 0)), "seg": k})
            if j == 0:
                p["join"] = "scene" if scene_first else "range"
        pieces.extend(ps)
    # frame snap (timeline grid), merge touching pieces of the same clip
    snapped: list[dict] = []
    for p in pieces:
        sf, ef = frame_floor(p["start"], fps), frame_ceil(p["end"], fps)
        if ef <= sf:
            continue
        p["sf"], p["ef"] = sf, ef
        q = snapped[-1] if snapped else None
        if q and q["clip"] == p["clip"] and q["kind"] == p["kind"] and sf <= q["ef"] and sf >= q["sf"]:
            q["ef"] = max(q["ef"], ef)
            if p["w"] and q["w"]:
                q["w"][1] = p["w"][1]
            continue
        snapped.append(p)
    pieces = snapped
    # zoom: new scene 100 %, jump cuts alternate, B-roll 100 %
    z = cfg["zoom"]
    prev = None
    for p in pieces:
        new_scene = (prev is None or p["kind"] == "broll" or prev["kind"] == "broll"
                     or prev["clip"] != p["clip"])
        if p["kind"] == "broll" or not z["enabled"]:
            p["zoom"] = 1.0
        elif new_scene:
            p["zoom"] = 1.0
        else:
            p["zoom"] = z["jump"] if prev["zoom"] == 1.0 else 1.0
        p["scene_start"] = new_scene
        p["cut_before"] = True
        prev = p
    # punch-ins: split for the line only
    for m in [m for m in moments if m.get("type") == "punch"]:
        clip = get_clip(m["clip"])
        try:
            ps_t = clip.toks[int(m["from"])]["start"] - c["pre_pad"]
            pe_t = clip.toks[int(m["to"])]["end"] + c["post_pad"]
        except IndexError:
            die(f"punch {m}: chỉ số từ ngoài phạm vi")
        psf, pef = frame_floor(ps_t, fps), frame_ceil(pe_t, fps)
        out: list[dict] = []
        for p in pieces:
            if p["clip"] != clip.id or p["kind"] != "speech" or pef <= p["sf"] or psf >= p["ef"]:
                out.append(p)
                continue
            a, b = max(psf, p["sf"]), min(pef, p["ef"])
            parts = []
            if a > p["sf"]:
                parts.append(dict(p, ef=a))
            parts.append(dict(p, sf=a, ef=b, why=p.get("why", "") if a == p["sf"] else "", zoom=z["punch"] if z["enabled"] else 1.0,
                              cut_before=(a == p["sf"] and p["cut_before"]), punch=m.get("label", "")))
            if b < p["ef"]:
                parts.append(dict(p, sf=b, cut_before=False, why=""))
            if len(parts) > 1 and a > p["sf"]:
                parts[1]["cut_before"] = False
            out.extend(parts)
        pieces = out
    # output times
    t_f = 0
    for n, p in enumerate(pieces, 1):
        p["n"] = n
        p["start"], p["end"] = p["sf"] / fps, p["ef"] / fps
        p["frames"] = p["ef"] - p["sf"]
        p["out_start_f"] = t_f
        t_f += p["frames"]
    total = t_f / fps
    # markers for notes: on the join where the cut words were
    markers = []
    for m in [m for m in moments if m.get("type") == "note"]:
        clip = get_clip(m["clip"])
        try:
            note_t = clip.toks[int(m["from"])]["start"]
        except IndexError:
            die(f"note {m}: chỉ số từ ngoài phạm vi")
        at_f = 0
        for p in pieces:
            if p["clip"] == clip.id and p["start"] <= note_t + 1e-6:
                at_f = p["out_start_f"] + p["frames"] if p["end"] <= note_t + 1e-6 else p["out_start_f"]
        markers.append({"at": round(float(at_f / fps), 3), "label": m.get("label", "note"),
                        "note": m.get("note", ""), "color": "pink"})
    for p in pieces:
        if p.get("punch"):
            markers.append({"at": round(float(p["out_start_f"] / fps), 3), "label": f"PUNCH: {p['punch']}",
                            "note": "", "color": "blue"})
    raw = sum(cl.dur for cl in clips.values())
    joins = {"scene": 0, "range": 0, "pause": 0}
    for p in pieces[1:]:
        if p.get("cut_before") and p.get("join") in joins:
            joins[p["join"]] += 1
    def words_in(p):
        if p["kind"] != "speech":
            return None
        idx = [t["i"] for t in clips[p["clip"]].toks
               if p["start"] <= (t["start"] + t["end"]) / 2 < p["end"]]
        return [idx[0], idx[-1]] if idx else None

    out_pieces = []
    for p in pieces:
        out_pieces.append({
            "n": p["n"], "clip": p["clip"], "src": entries[p["clip"]]["path"], "kind": p["kind"],
            "start": round(float(p["start"]), 6), "end": round(float(p["end"]), 6), "frames": p["frames"],
            "out_start": round(float(p["out_start_f"] / fps), 6), "zoom": p["zoom"],
            "scene_start": p["scene_start"], "cut_before": p["cut_before"], "join": p.get("join"),
            "words": words_in(p), "gain_db": p["gain_db"], "why": p.get("why", ""),
            **({"punch": p["punch"]} if p.get("punch") else {}),
        })
    return {"video": video, "fps": str(fps), "fps_float": round(float(fps), 3), "width": width,
            "height": height, "duration": round(float(total), 3), "frames": t_f,
            "pieces": out_pieces, "markers": sorted(markers, key=lambda m: m["at"]),
            "flags": keep.get("flags", []), "summary": keep.get("summary", ""),
            "stats": {"raw_s": round(raw, 2), "cut_s": round(float(total), 2), "pieces": len(out_pieces),
                      "pause_cuts": n_pause, "joins": joins,
                      "broll": sum(1 for p in out_pieces if p["kind"] == "broll"),
                      "max_pause": max_pause, "pause_keep": pause_keep}}


def review_md(ws, video: str, cfg: dict, plan: dict) -> str:
    vd = video_dir(ws, video, cfg)
    man = read_json(vd / "manifest.json")
    st = plan["stats"]
    L = [f"# Review: {video}", "",
         f"Thô {fmt_tc(st['raw_s'])} → cắt {fmt_tc(st['cut_s'])} · {st['pieces']} đoạn · "
         f"{st['pause_cuts']} chỗ rút ngắn khoảng lặng (max_pause {st['max_pause']} / giữ {st['pause_keep']}) · "
         f"{st['broll']} B-roll · khung {plan['width']}x{plan['height']} @{plan['fps_float']}", ""]
    if plan.get("summary"):
        L += ["## Tóm tắt", plan["summary"], ""]
    L += ["## Timeline", "", "| # | Ra | Nguồn | Loại | Zoom | Ghi chú |", "|---|---|---|---|---|---|"]
    for p in plan["pieces"]:
        src = f"{p['clip']} {fmt_tc(p['start'])}–{fmt_tc(p['end'])}"
        note = p.get("why", "")
        if p.get("punch"):
            note = f"PUNCH: {p['punch']} {note}"
        if p["words"]:
            note = f"từ {p['words'][0]}–{p['words'][1]} {note}"
        cut = "" if p["cut_before"] else " (liền)"
        L.append(f"| {p['n']} | {fmt_tc(p['out_start'])}{cut} | {src} | {p['kind']} | {p['zoom']:.3g} | {note.strip()} |")
    if plan["markers"]:
        L += ["", "## Markers", ""] + [f"- {fmt_tc(m['at'])} [{m['color']}] {m['label']} {m['note']}"
                                         for m in plan["markers"]]
    if plan["flags"]:
        L += ["", "## Cần người dùng xem", ""] + [f"- {f.get('clip')} @từ {f.get('at')}: {f.get('note')}"
                                                   for f in plan["flags"]]
    L += ["", "## Transcript (~~gạch~~ = bị cắt)", ""]
    for e in man["clips"]:
        toks = read_json(vd / "words" / f"{e['id']}.json", []) or []
        if not toks:
            continue
        kept = set()
        for p in plan["pieces"]:
            if p["clip"] == e["id"] and p["kind"] == "speech":
                for t in toks:
                    if p["start"] <= (t["start"] + t["end"]) / 2 < p["end"]:
                        kept.add(t["i"])
        L.append(f"### {e['id']}")
        line, n = [], 0
        for t in toks:
            w = t["text"] if t["i"] in kept else f"~~{t['text']}~~"
            if not line:
                line.append(f"[{t['i']}] ")
            line.append(w + " ")
            n += 1
            if n >= 18 and t["text"][-1:] in ".!?…":
                L.append("".join(line).rstrip())
                line, n = [], 0
        if line:
            L.append("".join(line).rstrip())
        L.append("")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--pause-report", action="store_true")
    workspace_arg(ap)
    a = ap.parse_args()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    if a.pause_report:
        say("max_pause  pause_keep  chỗ cắt khoảng lặng  độ dài  tiết kiệm")
        base = None
        for mp in (0.4, 0.5, 0.75, 1.0, 1.5, 2.0):
            pk = round(mp * 0.6, 2)
            p = build(ws, a.video, cfg, mp, pk)
            st = p["stats"]
            if base is None:
                base = build(ws, a.video, dict(cfg, cut=dict(cfg["cut"], pauses_enabled=False)))["duration"]
            say(f"{mp:>8}  {pk:>10}  {st['pause_cuts']:>19}  {fmt_tc(p['duration']):>7}  {base - p['duration']:.1f}s")
        return
    plan = build(ws, a.video, cfg)
    vd = video_dir(ws, a.video, cfg)
    write_json(vd / "cuts.json", plan)
    (vd / "review.md").write_text(review_md(ws, a.video, cfg, plan), encoding="utf-8")
    st = plan["stats"]
    say(f"cuts.json: {st['pieces']} đoạn, {fmt_tc(st['raw_s'])} → {fmt_tc(st['cut_s'])}, "
        f"rút khoảng lặng {st['pause_cuts']}, nối: cảnh {st['joins']['scene']} / khoảng {st['joins']['range']} / "
        f"lặng {st['joins']['pause']}, B-roll {st['broll']}, markers {len(plan['markers'])}")
    say(f"đọc lại: {(vd / 'review.md').relative_to(ws)}")


if __name__ == "__main__":
    main()
