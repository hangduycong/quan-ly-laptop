"""Shared helpers for the bien-tap scripts (Python stdlib + ffmpeg/ffprobe only).

Workspace layout (created by init.py):
  <workspace>/raw video/            footage, READ-ONLY
  <workspace>/export edited video/  finished exports (new file name every time)
  <workspace>/brand/                BRAND.md, brand.json, logo, music/, sfx/
  <workspace>/system/config.json    defaults (deep-merged over DEFAULTS below)
  <workspace>/system/keys.env       API keys, never printed
  <workspace>/system/videos/<v>/    per-video work files
"""
from __future__ import annotations

import copy
import json
import math
import os
import re
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".mts", ".mxf", ".webm"}

DEFAULTS: dict = {
    "paths": {"raw": "raw video", "export": "export edited video", "videos": "system/videos"},
    "timeline": {"width": None, "height": None, "fps": None},
    "cut": {
        "pre_pad": 0.08, "post_pad": 0.12,
        "pauses_enabled": True, "max_pause": 1.0, "pause_keep": 0.6,
        "scene_lead_in": 0.5, "scene_tail": 0.6,
        "silence_db": -43, "silence_min": 0.25, "silence_cover": 0.85,
        "onset_window": 0.25, "offset_window": 0.3,
        "audio_fade": 0.03,
    },
    "zoom": {"enabled": True, "jump": 1.075, "punch": 1.15},
    "grade": {"lut": None, "clips": []},
    "audio": {
        "voice": {
            "target_lufs": -16.0, "true_peak": -2.0, "lra": 11.0,
            "channel": "auto", "eq": False, "denoise": False,
        },
        "silent_broll_db": -60.0,
    },
    "music": {"full_lufs": -16, "duck_db": -14, "ramp_up": 1.2, "ramp_down": 1.0,
              "lead": 0.9, "crossfade": 2.5, "sfx_db": -10},
    "captions": {
        "chars_per_line": 42, "stretch_to": 50, "pause_split": 0.6, "max_cue": 3.2,
        "min_cue": 0.9, "end_after_word": 0.25,
        "style": {"font": "DejaVu Sans", "size_at_1080": 48, "position_y_from_bottom": 0.11,
                  "outline": 2, "shadow": 1, "bold": False},
        "fillers": {
            "en": ["um", "uh", "uhm", "erm", "hmm", "mm"],
            "vi": ["ờ", "ơ", "ừm", "ưm", "hừm", "ờm"],
            "pt": ["hã", "hãã", "éé", "ããã"],
        },
        "standard_language": {"words": {}, "phrases": {}},
    },
    "render": {"crf": 18, "preset": "medium", "draft_height": 720, "draft_crf": 28, "jobs": 0},
    "export": {"audio_bitrate": "320k"},
    "transcribe": {"provider": "elevenlabs", "model": "scribe_v2", "language": "auto",
                   "diarize": True, "audio_events": True},
}


# ---------------------------------------------------------------- output ----
def say(msg: str = "") -> None:
    print(msg, flush=True)


def die(msg: str, code: int = 1) -> None:
    print(f"LỖI: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


# ------------------------------------------------------------- workspace ----
def find_workspace(start: str | None = None) -> Path:
    """Walk up from `start` (or cwd) to the folder holding system/config.json."""
    p = Path(start or os.getcwd()).resolve()
    for cand in [p, *p.parents]:
        if (cand / "system" / "config.json").exists():
            return cand
    die("không tìm thấy workspace (thư mục có system/config.json). "
        "Chạy init.py trước, hoặc truyền --workspace.")
    raise SystemExit  # unreachable


def deep_merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if k in ("comment",):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(ws: Path, video: str | None = None) -> dict:
    cfg = deep_merge(DEFAULTS, read_json(ws / "system" / "config.json", {}))
    if video:
        cfg = deep_merge(cfg, read_json(video_dir(ws, video, cfg) / "settings.json", {}))
    return cfg


def video_dir(ws: Path, video: str, cfg: dict | None = None) -> Path:
    cfg = cfg or deep_merge(DEFAULTS, read_json(ws / "system" / "config.json", {}))
    return ws / cfg["paths"]["videos"] / video


def raw_dir(ws: Path, cfg: dict) -> Path:
    return ws / cfg["paths"]["raw"]


def export_dir(ws: Path, cfg: dict) -> Path:
    return ws / cfg["paths"]["export"]


def read_json(path: Path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return copy.deepcopy(default)
    except json.JSONDecodeError as e:
        die(f"{path} không phải JSON hợp lệ: {e}")


def write_json(path: Path, data) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def next_version(folder: Path, stem: str, ext: str) -> Path:
    """folder/stem_v1.ext, _v2 ... first that does not exist (never overwrite)."""
    folder.mkdir(parents=True, exist_ok=True)
    n = 1
    while (folder / f"{stem}_v{n}{ext}").exists():
        n += 1
    return folder / f"{stem}_v{n}{ext}"


def latest_version(folder: Path, stem: str, ext: str) -> Path | None:
    best, best_n = None, 0
    for p in folder.glob(f"{stem}_v*{ext}"):
        m = re.fullmatch(re.escape(stem) + r"_v(\d+)" + re.escape(ext), p.name)
        if m and int(m.group(1)) > best_n:
            best, best_n = p, int(m.group(1))
    return best


# ------------------------------------------------------------------ keys ----
def load_key(ws: Path) -> str | None:
    """SPEECH_TO_TEXT_API_KEY / ELEVENLABS_API_KEY from env or system/keys.env.
    The value is never printed. In a cloud session whose network proxy injects the key,
    any placeholder (e.g. ELEVENLABS_API_KEY=proxy-injected) works."""
    for name in ("SPEECH_TO_TEXT_API_KEY", "ELEVENLABS_API_KEY"):
        if os.environ.get(name):
            return os.environ[name]
    f = ws / "system" / "keys.env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() in ("SPEECH_TO_TEXT_API_KEY", "ELEVENLABS_API_KEY") and v.strip():
                    return v.strip().strip('"').strip("'")
    return None


# ---------------------------------------------------------------- ffmpeg ----
def need_tools() -> None:
    for t in ("ffmpeg", "ffprobe"):
        if not shutil.which(t):
            die(f"thiếu {t}. Cài ffmpeg (ví dụ: sudo apt install ffmpeg / brew install ffmpeg).")


def run(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.PIPE if capture else None, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        tail = (r.stderr or "").strip().splitlines()[-12:]
        die("lệnh thất bại: " + " ".join(cmd[:6]) + " …\n" + "\n".join(tail))
    return r


def ffmpeg(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return run(["ffmpeg", "-hide_banner", "-nostdin", "-y", "-loglevel", "error", *args], check=check)


def ffprobe_json(path: Path) -> dict:
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
             str(path)])
    return json.loads(r.stdout or "{}")


def parse_rate(s: str | None) -> Fraction | None:
    if not s or s in ("0/0", "0"):
        return None
    try:
        f = Fraction(s)
        return f if f > 0 else None
    except (ValueError, ZeroDivisionError):
        return None


def probe_clip(path: Path) -> dict:
    j = ffprobe_json(path)
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"
              and not s.get("disposition", {}).get("attached_pic")), None)
    a = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), None)
    dur = float(j.get("format", {}).get("duration") or 0)
    info: dict = {"duration": round(dur, 3), "has_video": bool(v), "has_audio": bool(a)}
    if v:
        w, h = int(v.get("width", 0)), int(v.get("height", 0))
        rot = 0
        for sd in v.get("side_data_list", []) or []:
            if "rotation" in sd:
                rot = int(float(sd["rotation"]))
        rot = rot or int(float(v.get("tags", {}).get("rotate", 0) or 0))
        if abs(rot) % 180 == 90:
            w, h = h, w
        fps = parse_rate(v.get("r_frame_rate")) or parse_rate(v.get("avg_frame_rate"))
        info.update({
            "width": w, "height": h, "rotation": rot,
            "fps": str(fps) if fps else None,
            "fps_float": round(float(fps), 3) if fps else None,
            "vcodec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"),
            "color_transfer": v.get("color_transfer"),
            "vertical": h > w,
        })
    if a:
        info.update({"channels": int(a.get("channels", 0)),
                     "sample_rate": int(a.get("sample_rate", 0) or 0),
                     "acodec": a.get("codec_name")})
    return info


def channel_levels(path: Path, start: float = 0.0, dur: float | None = None) -> list[float]:
    """RMS dB per audio channel (astats)."""
    args = ["-ss", f"{start:.3f}"] if start else []
    if dur:
        args += ["-t", f"{dur:.3f}"]
    r = run(["ffmpeg", "-hide_banner", "-nostdin", *args, "-i", str(path), "-map", "0:a:0",
             "-af", "astats=measure_overall=none", "-f", "null", "-"], check=False)
    levels = []
    for m in re.finditer(r"RMS level dB:\s*(-?[\d.]+|-inf)", r.stderr or ""):
        val = m.group(1)
        levels.append(-120.0 if val == "-inf" else float(val))
    return levels


def silence_map(path: Path, db: float, min_s: float) -> list[list[float]]:
    r = run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(path), "-map", "0:a:0", "-af",
             f"silencedetect=noise={db}dB:d={min_s}", "-f", "null", "-"], check=False)
    out, start = [], None
    for line in (r.stderr or "").splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and start is not None:
            out.append([round(start, 3), round(float(m.group(1)), 3)])
            start = None
    if start is not None:
        out.append([round(start, 3), None])  # runs to end of file
    return out


def loudness(path: Path, start: float | None = None, dur: float | None = None) -> dict:
    """Integrated loudness (LUFS) and true peak (dBTP) via ebur128."""
    args = []
    if start is not None:
        args += ["-ss", f"{start:.3f}"]
    if dur is not None:
        args += ["-t", f"{dur:.3f}"]
    r = run(["ffmpeg", "-hide_banner", "-nostdin", *args, "-i", str(path), "-map", "0:a:0",
             "-af", "ebur128=peak=true", "-f", "null", "-"], check=False)
    txt = (r.stderr or "").split("Summary:")[-1]
    res = {}
    m = re.search(r"I:\s*(-?[\d.]+|-inf) LUFS", txt)
    if m:
        res["lufs"] = None if m.group(1) == "-inf" else float(m.group(1))
    m = re.search(r"Peak:\s*(-?[\d.]+|-inf) dBFS", txt)
    if m:
        res["true_peak"] = None if m.group(1) == "-inf" else float(m.group(1))
    return res


def video_encode_args(cfg: dict, draft: bool, height: int) -> list[str]:
    r = cfg["render"]
    if draft:
        return ["-c:v", "libx264", "-preset", "ultrafast", "-crf", str(r["draft_crf"]),
                "-pix_fmt", "yuv420p"]
    cap = "50M" if height >= 2000 else "30M" if height >= 1400 else "16M" if height >= 1000 else "8M"
    return ["-c:v", "libx264", "-preset", r["preset"], "-crf", str(r["crf"]), "-profile:v", "high",
            "-maxrate", cap, "-bufsize", cap, "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]


def fmt_tc(t: float) -> str:
    t = max(0.0, t)
    m, s = divmod(t, 60)
    h, m = divmod(int(m), 60)
    return f"{h:d}:{m:02d}:{s:05.2f}" if h else f"{m:02d}:{s:05.2f}"


def srt_tc(t: float) -> str:
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def frame_floor(t: float, fps: Fraction) -> int:
    return int(math.floor(t * fps + 1e-6))


def frame_ceil(t: float, fps: Fraction) -> int:
    return int(math.ceil(t * fps - 1e-6))


def find_video_sources(ws: Path, cfg: dict, video: str) -> list[Path]:
    """`video` is a file stem in raw video/ (one clip) or a folder (several clips)."""
    rd = raw_dir(ws, cfg)
    folder = rd / video
    if folder.is_dir():
        clips = sorted(p for p in folder.rglob("*") if p.suffix.lower() in VIDEO_EXTS)
        if not clips:
            die(f"thư mục {folder} không có file video.")
        return clips
    hits = sorted(p for p in rd.glob(f"{video}.*") if p.suffix.lower() in VIDEO_EXTS)
    if not hits:
        die(f"không thấy '{video}' trong {rd} (file {video}.mp4/.mov… hoặc thư mục {video}/).")
    return hits[:1]


def workspace_arg(ap) -> None:
    ap.add_argument("--workspace", help="thư mục workspace (mặc định: tìm từ thư mục hiện tại)")
