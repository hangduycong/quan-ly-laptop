#!/usr/bin/env python3
"""Render cuts.json to an MP4 with ffmpeg (no DaVinci needed).

Pipeline (each rule exists because the alternative failed):
  1. per piece: exact frame count at the timeline fps, scale-to-fill + crop, zoom, optional LUT
     (log clips only) -> H.264 segment, all with identical settings
  2. lossless concat (-c copy) of the video segments
  3. per piece: PCM audio of exactly the same duration, voice channel fixed, gain, 30 ms fades
     only at real cuts (never inside a punch-in split) -> sample-exact PCM concat
  4. voice: optional EQ/denoise, two-pass loudnorm (-16 LUFS, -2 dBTP)
  5. music bed / SFX from music/current.json (score.py) mixed under, limiter
  6. mux: AAC 320k 48 kHz, +faststart

Usage:
  python3 render.py <video>               -> system/videos/<v>/renders/<v>_vN.mp4
  python3 render.py <video> --draft       720p ultrafast, to check cut points quickly
  python3 render.py <video> --no-music    ignore music/current.json
  python3 render.py <video> --jobs 4      parallel segment encodes (default: half the CPUs)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

from common import (die, ffmpeg, find_workspace, fmt_tc, load_config, loudness, need_tools,
                    next_version, probe_clip, read_json, run, say, video_dir, video_encode_args,
                    workspace_arg, write_json)


def voice_filters(cfg: dict) -> list[str]:
    v = cfg["audio"]["voice"]
    f = []
    if v.get("denoise"):
        f.append("afftdn=nr=12:nf=-50")
    if v.get("eq"):  # recipe from references/voice-and-audio.md
        f += ["highpass=f=80", "equalizer=f=250:t=q:w=1.2:g=-3", "equalizer=f=3500:t=q:w=1:g=3",
              "highshelf=f=10000:g=2"]
    return f


def loudnorm_two_pass(src: Path, dst: Path, cfg: dict, extra: list[str]) -> None:
    v = cfg["audio"]["voice"]
    base = f"loudnorm=I={v['target_lufs']}:TP={v['true_peak']}:LRA={v['lra']}"
    pre = ",".join(extra + [base + ":print_format=json"])
    r = run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(src), "-af", pre, "-f", "null", "-"], check=False)
    txt = r.stderr or ""
    try:
        j = json.loads(txt[txt.rindex("{"):txt.rindex("}") + 1])
        if j.get("input_i") in ("-inf", None) or float(j["input_i"]) < -70:
            raise ValueError("silent")
        second = (f"{base}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                  f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
        af = ",".join(extra + [second])
    except (ValueError, KeyError):
        af = ",".join(extra) if extra else "anull"  # silent or unmeasurable: leave level alone
    ffmpeg(["-i", str(src), "-af", af + ",aresample=48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst)])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--jobs", type=int)
    ap.add_argument("--keep-temp", action="store_true")
    workspace_arg(ap)
    a = ap.parse_args()
    need_tools()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    plan = read_json(vd / "cuts.json") or die("chưa có cuts.json — chạy plan.py")
    man = read_json(vd / "manifest.json") or die("chưa có manifest.json")
    clips = {c["id"]: c for c in man["clips"]}
    fps = Fraction(plan["fps"])
    W, H = plan["width"], plan["height"]
    if a.draft:
        dh = cfg["render"]["draft_height"]
        if H > dh:
            W, H = int(round(W * dh / H / 2)) * 2, dh
    out = next_version(vd / "renders", f"{a.video}_draft" if a.draft else a.video, ".mp4")
    tmp = vd / "renders" / f".tmp_{out.stem}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    pieces = plan["pieces"]
    grade = cfg["grade"]
    lut = (ws / grade["lut"]) if grade.get("lut") else None
    if lut and not lut.exists():
        die(f"LUT {lut} không tồn tại")
    enc = video_encode_args(cfg, a.draft, H)
    fade = cfg["cut"]["audio_fade"]
    say(f"render {out.name}: {len(pieces)} đoạn, {W}x{H} @{float(fps):.3f}, {fmt_tc(plan['duration'])}")

    def src_of(p):
        s = p["src"]
        return Path(s) if s.startswith("/") else ws / s

    def do_video(k: int):
        p = pieces[k]
        cid = p["clip"]
        f = []
        if lut and (cid in grade.get("clips", []) or (not grade.get("clips") and clips[cid]["picture_profile"].get("log"))):
            f.append(f"lut3d=file='{lut}'")
        z = float(p["zoom"])
        zw, zh = int(round(W * z / 2)) * 2, int(round(H * z / 2)) * 2
        f += [f"fps={fps}", f"scale={zw}:{zh}:force_original_aspect_ratio=increase:flags=lanczos",
              f"crop={W}:{H}", "setsar=1", "tpad=stop_mode=clone:stop_duration=2", "format=yuv420p"]
        dst = tmp / f"v{k:04d}.mp4"
        ffmpeg(["-ss", f"{p['start']:.6f}", "-i", str(src_of(p)), "-map", "0:v:0", "-an", "-vf", ",".join(f),
                "-frames:v", str(p["frames"]), *enc, "-r", str(fps), "-g", str(int(round(float(fps) * 2))),
                "-video_track_timescale", str(fps.numerator if fps.denominator != 1 else fps.numerator * 1000),
                str(dst)])
        return dst

    def do_audio(k: int):
        p = pieces[k]
        dur = p["frames"] / fps
        cl = clips[p["clip"]]
        dst = tmp / f"a{k:04d}.wav"
        nxt = pieces[k + 1] if k + 1 < len(pieces) else None
        fin = p["cut_before"]
        fout = nxt is None or nxt["cut_before"]
        f = []
        want = str(cfg["audio"]["voice"].get("channel", "auto")).lower()
        vc = {"left": 0, "right": 1, "mix": None}.get(want, cl.get("voice_channel"))
        if vc is not None and cl["probe"].get("channels", 0) >= 2:
            f.append(f"pan=stereo|c0=c{vc}|c1=c{vc}")
        f += ["aresample=48000", "aformat=sample_fmts=s16:channel_layouts=stereo",
              "apad", f"atrim=0:{float(dur):.6f}"]
        if p.get("gain_db"):
            f.append(f"volume={p['gain_db']}dB")
        if fin:
            f.append(f"afade=t=in:st=0:d={fade}")
        if fout:
            f.append(f"afade=t=out:st={max(0.0, float(dur) - fade):.6f}:d={fade}")
        if cl["probe"].get("has_audio"):
            ffmpeg(["-ss", f"{p['start']:.6f}", "-t", f"{float(dur) + 0.5:.6f}", "-i", str(src_of(p)),
                    "-map", "0:a:0", "-af", ",".join(f), "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst)])
        else:
            ffmpeg(["-f", "lavfi", "-t", f"{float(dur):.6f}", "-i", "anullsrc=r=48000:cl=stereo",
                    "-c:a", "pcm_s16le", str(dst)])
        return dst

    jobs = a.jobs or cfg["render"].get("jobs") or max(1, (os.cpu_count() or 2) // 2)
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        vids = list(ex.map(do_video, range(len(pieces))))
        auds = list(ex.map(do_audio, range(len(pieces))))
    say("  đoạn hình + tiếng: xong")
    (tmp / "v.txt").write_text("".join(f"file '{p.name}'\n" for p in vids))
    (tmp / "a.txt").write_text("".join(f"file '{p.name}'\n" for p in auds))
    ffmpeg(["-f", "concat", "-safe", "0", "-i", str(tmp / "v.txt"), "-c", "copy", str(tmp / "video.mp4")])
    ffmpeg(["-f", "concat", "-safe", "0", "-i", str(tmp / "a.txt"), "-c", "copy", str(tmp / "voice_raw.wav")])
    loudnorm_two_pass(tmp / "voice_raw.wav", tmp / "voice.wav", cfg, voice_filters(cfg))
    say("  giọng: đã chuẩn hóa âm lượng")
    audio = tmp / "voice.wav"
    music_used = []
    cur = read_json(vd / "music" / "current.json", {}) if not a.no_music else {}
    extra = [vd / "music" / cur[k] for k in ("bed", "sfx") if cur.get(k)]
    for e in extra:
        if not e.exists():
            die(f"music/current.json trỏ tới {e.name} nhưng file không tồn tại — chạy lại score.py")
    if extra:
        ins = ["-i", str(audio)]
        for e in extra:
            ins += ["-i", str(e)]
        n = 1 + len(extra)
        ffmpeg([*ins, "-filter_complex",
                f"amix=inputs={n}:normalize=0:duration=first:dropout_transition=0,alimiter=limit=0.89:level=false",
                "-ar", "48000", "-c:a", "pcm_s16le", str(tmp / "mix.wav")])
        audio = tmp / "mix.wav"
        music_used = [e.name for e in extra]
        say(f"  nhạc: trộn {', '.join(music_used)}")
    total = plan["frames"] / fps
    ffmpeg(["-i", str(tmp / "video.mp4"), "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
            "-c:a", "aac", "-b:a", cfg["export"]["audio_bitrate"], "-ar", "48000", "-t", f"{float(total):.6f}",
            "-movflags", "+faststart", str(out)])
    meta = dict(plan, render={"file": out.name, "draft": a.draft, "width": W, "height": H, "music": music_used})
    write_json(out.with_suffix(".cuts.json"), meta)
    if not a.keep_temp:
        shutil.rmtree(tmp, ignore_errors=True)
    got = probe_clip(out)
    ld = loudness(out)
    say(f"xong: {out.relative_to(ws)}  {got['duration']:.2f}s (kế hoạch {float(total):.2f}s)  "
        f"{got.get('width')}x{got.get('height')} @{got.get('fps_float')}  "
        f"{ld.get('lufs')} LUFS, true peak {ld.get('true_peak')} dBTP")
    if abs(got["duration"] - float(total)) > 0.1:
        say("  ! độ dài lệch kế hoạch > 0.1s — chạy check.py")


if __name__ == "__main__":
    main()
