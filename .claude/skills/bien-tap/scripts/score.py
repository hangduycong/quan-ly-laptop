#!/usr/bin/env python3
"""Build the music bed (one cue per section, crossfaded, ducking envelope baked in) and an SFX track,
on the OUTPUT timeline of the current cut. render.py mixes them in via music/current.json.

Envelope (references/music-and-sound.md): full level (-16 LUFS) on B-roll, -14 dB under speech;
rise 1.2 s starting 0.9 s before each B-roll, fall 1.0 s ending when speech resumes.

music/cues.json (times = output timeline seconds; files relative to the video folder or workspace):
  {"cues": [{"file": "music/src/opening.wav", "start": 0, "end": 95.5, "title": "...",
             "alternates": ["...", "..."]}],
   "sfx":  [{"file": "brand/sfx/riser.wav", "at": 41.2, "gain_db": -10, "peak": "auto"}]}
  "at" = where the SFX's loudest point lands (e.g. exactly on a B-roll cut).

Usage:
  python3 score.py <video>              build bed_vN.wav + sfx_vN.wav, update music/current.json
  python3 score.py <video> --bed-only   (or --sfx-only) rebuild one, keep the other
  python3 score.py <video> --off        stop using music (clears current.json)
Music must be licensed for the creator's use (Epidemic Sound, their own library, ...).
"""
from __future__ import annotations

import argparse
import array
import subprocess
from pathlib import Path

from common import (die, ffmpeg, find_workspace, fmt_tc, load_config, loudness, need_tools,
                    next_version, probe_clip, read_json, say, video_dir, workspace_arg, write_json)


def resolve(ws: Path, vd: Path, f: str) -> Path:
    for base in (vd, ws):
        p = Path(f) if Path(f).is_absolute() else base / f
        if p.exists():
            return p
    die(f"không thấy file {f}")
    raise SystemExit


def broll_windows(plan: dict) -> list[tuple[float, float]]:
    fps = float(plan["fps_float"])
    win: list[list[float]] = []
    for p in plan["pieces"]:
        if p["kind"] != "broll":
            continue
        a, b = p["out_start"], p["out_start"] + p["frames"] / fps
        if win and abs(win[-1][1] - a) < 0.05:
            win[-1][1] = b
        else:
            win.append([a, b])
    return [(a, b) for a, b in win]


def envelope_expr(windows, m: dict, total: float) -> str:
    terms = []
    for a, b in windows:
        r0 = max(0.0, a - m["lead"])
        fall = f"({b:.3f}-t)/{m['ramp_down']}" if b < total - 0.05 else "1"
        terms.append(f"clip(min((t-{r0:.3f})/{m['ramp_up']},{fall}),0,1)")
    if not terms:
        g = "0"
    else:
        g = terms[0]
        for t in terms[1:]:
            g = f"max({g},{t})"
    return f"pow(10,({m['duck_db']}*(1-({g})))/20)"


def peak_offset(path: Path) -> float:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-i", str(path), "-ac", "1",
                        "-ar", "8000", "-f", "s16le", "-"], stdout=subprocess.PIPE, check=True)
    a = array.array("h")
    a.frombytes(r.stdout[: len(r.stdout) // 2 * 2])
    if not a:
        return 0.0
    win, best, best_i = 80, -1, 0  # 10 ms windows
    for i in range(0, len(a), win):
        v = max((abs(x) for x in a[i:i + win]), default=0)
        if v > best:
            best, best_i = v, i
    return best_i / 8000


def build_bed(ws, vd, plan, cues, m, total) -> Path:
    ins, chains, labels = [], [], []
    xf = m["crossfade"]
    for k, c in enumerate(cues):
        src = resolve(ws, vd, c["file"])
        need = float(c["end"]) - float(c["start"]) + (xf if k < len(cues) - 1 else 0)
        have = probe_clip(src)["duration"]
        if have + 0.05 < need:
            say(f"  ! cue {k + 1} ({src.name}) dài {have:.1f}s, cần {need:.1f}s — xin bản edit dài hơn hoặc rút section")
        fin = xf if k > 0 else 0.5
        fout = xf if k < len(cues) - 1 else 2.0
        ins += ["-i", str(src)]
        d = int(round(float(c["start"]) * 1000))
        chains.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,"
                      f"loudnorm=I={m['full_lufs']}:TP=-2:LRA=11,aresample=48000,atrim=0:{need:.3f},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:st=0:d={fin},afade=t=out:st={max(0, need - fout):.3f}:d={fout},"
                      f"adelay={d}|{d}[c{k}]")
        labels.append(f"[c{k}]")
    env = envelope_expr(broll_windows(plan), m, total)
    fc = ";".join(chains) + f";{''.join(labels)}amix=inputs={len(cues)}:normalize=0:dropout_transition=0," \
         f"apad,atrim=0:{total:.3f},volume='{env}':eval=frame[out]"
    dst = next_version(vd / "music", "bed", ".wav")
    ffmpeg([*ins, "-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst)])
    return dst


def build_sfx(ws, vd, items, m, total) -> Path:
    ins, chains, labels = [], [], []
    for k, s in enumerate(items):
        src = resolve(ws, vd, s["file"])
        pk = peak_offset(src) if s.get("peak", "auto") == "auto" else float(s["peak"])
        start = float(s["at"]) - pk
        trim = max(0.0, -start)
        d = int(round(max(0.0, start) * 1000))
        gain = s.get("gain_db", m["sfx_db"])
        ins += ["-i", str(src)]
        chains.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I={m['full_lufs']}:TP=-2,"
                      f"aresample=48000,atrim=start={trim:.3f},asetpts=PTS-STARTPTS,volume={gain}dB,adelay={d}|{d}[s{k}]")
        labels.append(f"[s{k}]")
        say(f"  sfx {src.name}: đỉnh ở {pk:.2f}s trong file → đặt tại {fmt_tc(float(s['at']))}")
    fc = ";".join(chains) + f";{''.join(labels)}amix=inputs={len(items)}:normalize=0:dropout_transition=0," \
         f"apad,atrim=0:{total:.3f}[out]"
    dst = next_version(vd / "music", "sfx", ".wav")
    ffmpeg([*ins, "-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst)])
    return dst


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--bed-only", action="store_true")
    g.add_argument("--sfx-only", action="store_true")
    g.add_argument("--off", action="store_true")
    workspace_arg(ap)
    a = ap.parse_args()
    need_tools()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    cur = read_json(vd / "music" / "current.json", {}) or {}
    if a.off:
        write_json(vd / "music" / "current.json", {})
        say("đã tắt nhạc cho video này (file cũ vẫn giữ)")
        return
    plan = read_json(vd / "cuts.json") or die("chưa có cuts.json — chạy plan.py")
    spec = read_json(vd / "music" / "cues.json") or die("chưa có music/cues.json (xem --help)")
    m = cfg["music"]
    total = float(plan["duration"])
    cues = sorted(spec.get("cues", []), key=lambda c: float(c["start"]))
    if not a.sfx_only and cues:
        bed = build_bed(ws, vd, plan, cues, m, total)
        cur["bed"] = bed.name
        say(f"bed: music/{bed.name}")
        win = broll_windows(plan)
        if win:
            a0, b0 = win[0]
            lb = loudness(bed, a0 + 1.0, max(0.5, b0 - a0 - 1.0))
            say(f"  mức trên B-roll đầu ({fmt_tc(a0)}): {lb.get('lufs')} LUFS (mục tiêu ≈ {m['full_lufs']})")
        speech = next((p for p in plan["pieces"] if p["kind"] == "speech" and p["frames"] / float(plan["fps_float"]) > 4), None)
        if speech:
            ls = loudness(bed, speech["out_start"] + 1.5, 2.0)
            say(f"  mức dưới lời nói ({fmt_tc(speech['out_start'])}): {ls.get('lufs')} LUFS "
                f"(mục tiêu ≈ {m['full_lufs'] + m['duck_db']})")
        for k, c in enumerate(cues, 1):
            alts = " | ".join(c.get("alternates", [])) or "—"
            say(f"  cue {k}: {fmt_tc(float(c['start']))}–{fmt_tc(float(c['end']))} {c.get('title', '')}  (thay thế: {alts})")
    if not a.bed_only and spec.get("sfx"):
        sfx = build_sfx(ws, vd, spec["sfx"], m, total)
        cur["sfx"] = sfx.name
        say(f"sfx: music/{sfx.name}")
    write_json(vd / "music" / "current.json", cur)
    say("render.py sẽ trộn: " + ", ".join(f"{k}={v}" for k, v in cur.items() if k in ("bed", "sfx")))
    say("Mình không nghe được: đây là đánh giá từ số đo, người dùng nghe thử và nói nếu thấy chưa ổn.")


if __name__ == "__main__":
    main()
