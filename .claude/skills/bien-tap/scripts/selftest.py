#!/usr/bin/env python3
"""End-to-end self test on synthetic footage (no API key, no DaVinci): init -> ingest (cached fake
transcript) -> plan -> render -> check -> captions -> score -> render with music -> export.

Usage: python3 selftest.py [DIR]     (default: a temp folder, deleted afterwards unless --keep)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sh(*args, cwd=None):
    r = subprocess.run([sys.executable, *args], cwd=cwd, text=True, capture_output=True)
    print(r.stdout, end="")
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        raise SystemExit(f"FAIL: {' '.join(str(a) for a in args[:2])}")
    return r.stdout


def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def make_talk(path: Path, words: list[tuple[float, float]], dur: float, color: str):
    gate = "+".join(f"between(t,{s},{e})" for s, e in words)
    ff("-f", "lavfi", "-i", f"testsrc2=size=1280x720:rate=30,drawbox=c={color}@0.4:t=fill",
       "-f", "lavfi", "-i", "sine=f=220:sample_rate=48000",
       "-filter_complex", f"[1:a]volume='if({gate},0.5,0)':eval=frame,pan=stereo|c0=c0|c1=c0[a]",
       "-map", "0:v", "-map", "[a]", "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
       str(path))


def tokens(texts, times):
    return [{"i": i, "text": t, "start": s, "end": e, "type": "word", "speaker": "speaker_0"}
            for i, (t, (s, e)) in enumerate(zip(texts, times))]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dir", nargs="?")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    td = tempfile.TemporaryDirectory() if not a.dir else None
    ws = Path(a.dir or td.name).resolve()
    ws.mkdir(parents=True, exist_ok=True)
    sh(str(HERE / "init.py"), str(ws))
    raw = ws / "raw video" / "demo"
    raw.mkdir(parents=True, exist_ok=True)
    # clip A: a retake (words 0-3 abandoned), then the good take with a long pause in it
    ta = [(1.0, 1.4), (1.5, 1.9), (2.0, 2.3), (2.4, 2.8),
          (4.0, 4.4), (4.5, 4.9), (5.0, 5.5), (5.6, 6.0), (8.5, 8.9), (9.0, 9.5), (9.6, 10.2)]
    wa = ["Hello", "uh", "every-", "let", "Hello", "pro-product", "fans,", "today", "we", "test", "everything."]
    make_talk(raw / "A001.mp4", ta, 11.5, "blue")
    tb = [(0.8, 1.2), (1.3, 1.7), (1.8, 2.4), (2.5, 3.1), (3.2, 3.6), (3.7, 4.4)]
    wb = ["This", "is", "the", "punchline", "right", "here."]
    make_talk(raw / "A002.mp4", tb, 5.5, "green")
    ff("-f", "lavfi", "-i", "testsrc=size=1280x720:rate=30", "-f", "lavfi", "-i", "anoisesrc=a=0.01:r=48000",
       "-t", "4", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(raw / "B001.mp4"))
    vd = ws / "system" / "videos" / "demo"
    (vd / "words").mkdir(parents=True, exist_ok=True)
    (vd / "words" / "A001.json").write_text(json.dumps(tokens(wa, ta)))
    (vd / "words" / "A002.json").write_text(json.dumps(tokens(wb, tb)))
    (vd / "words" / "B001.json").write_text("[]")
    sh(str(HERE / "ingest.py"), "demo", "--no-transcribe", cwd=ws)
    (vd / "keep.json").write_text(json.dumps({
        "segments": [{"clip": "A001", "from": 4, "to": 10, "why": "second take"},
                     {"clip": "B001", "broll": True, "in": 0.5, "out": 3.5, "why": "cutaway"},
                     {"clip": "A002", "from": 0, "to": 5, "why": "punchline"}],
        "flags": [{"clip": "A001", "at": 5, "note": "stutter kept"}], "summary": "test"}))
    (vd / "moments.json").write_text(json.dumps({"moments": [
        {"type": "punch", "clip": "A002", "from": 2, "to": 3, "label": "the punchline"},
        {"type": "note", "clip": "A001", "from": 0, "to": 3, "label": "VIDEO: demo", "note": "roll demo"}]}))
    sh(str(HERE / "plan.py"), "demo", "--pause-report", cwd=ws)
    sh(str(HERE / "plan.py"), "demo", cwd=ws)
    cuts = json.loads((vd / "cuts.json").read_text())
    assert cuts["stats"]["pause_cuts"] == 1, "expected the 2.5 s pause to be shortened"
    assert any(p.get("punch") for p in cuts["pieces"]), "expected a punch-in piece"
    assert cuts["markers"], "expected a note marker"
    sh(str(HERE / "render.py"), "demo", "--draft", cwd=ws)
    sh(str(HERE / "check.py"), "demo", cwd=ws)
    sh(str(HERE / "captions.py"), "demo", "--language", "en", cwd=ws)
    srt = (vd / "captions" / "captions_v1.srt").read_text()
    assert "pro-product" not in srt and "every-" not in srt and " uh " not in srt, "caption cleaning failed"
    (vd / "music" / "src").mkdir(parents=True, exist_ok=True)
    ff("-f", "lavfi", "-i", "sine=f=330:sample_rate=48000", "-t", "30", str(vd / "music" / "src" / "bed.wav"))
    ff("-f", "lavfi", "-i", "anoisesrc=a=0.3:r=48000", "-af", "afade=t=in:d=1.5,afade=t=out:st=1.5:d=0.5",
       "-t", "2", str(vd / "music" / "src" / "riser.wav"))
    broll = next(p for p in cuts["pieces"] if p["kind"] == "broll")
    (vd / "music" / "cues.json").write_text(json.dumps({
        "cues": [{"file": "music/src/bed.wav", "start": 0, "end": cuts["duration"], "title": "test tone"}],
        "sfx": [{"file": "music/src/riser.wav", "at": broll["out_start"], "gain_db": -10}]}))
    sh(str(HERE / "score.py"), "demo", cwd=ws)
    sh(str(HERE / "render.py"), "demo", cwd=ws)
    sh(str(HERE / "check.py"), "demo", cwd=ws)
    sh(str(HERE / "export.py"), "demo", "--captions", "latest", "--burn", cwd=ws)
    sh(str(HERE / "export.py"), "demo", "--captions", "latest", cwd=ws)
    print("SELFTEST OK:", ws)
    if td and not a.keep:
        td.cleanup()


if __name__ == "__main__":
    main()
