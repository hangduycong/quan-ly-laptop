#!/usr/bin/env python3
"""Ingest a video: probe every clip, read picture profile, check voice channels, transcribe
(verbatim, word timestamps, cached), map silences, write manifest.json + transcript.md.

Usage:
  python3 ingest.py <video>                 <video> = file stem or folder name in raw video/
  python3 ingest.py <video> --num-speakers 2 --language vi
  python3 ingest.py <video> --retranscribe C0003   (costs money: ask the creator first)
  python3 ingest.py <video> --no-transcribe        (probe + silences only)

Outputs in system/videos/<video>/:
  manifest.json, transcripts/<clip>.json (raw API), words/<clip>.json (tokens {i,text,start,end,type,speaker}),
  silences/<clip>.json, transcript.md (phrase lines with word-index ranges, the reading view)
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from common import (channel_levels, die, ffmpeg, find_video_sources, find_workspace, fmt_tc,
                    load_config, load_key, need_tools, probe_clip, read_json, say, silence_map,
                    video_dir, workspace_arg, write_json)

SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"


def picture_profile(clip: Path, info: dict) -> dict:
    for xml in sorted(clip.parent.glob(clip.stem + "*")):
        if xml.suffix.lower() == ".xml":
            txt = xml.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'CaptureGammaEquation"?\s+value="([^"]+)"', txt) or \
                re.search(r'Gamma[^>]*value="([^"]+)"', txt)
            if m:
                val = m.group(1)
                return {"value": val, "log": "log" in val.lower(), "source": f"sidecar {xml.name}"}
    tr = (info.get("color_transfer") or "").lower()
    if tr in ("arib-std-b67", "smpte2084"):
        return {"value": f"HDR ({tr})", "log": False, "hdr": True, "source": "ffprobe"}
    return {"value": "baked (Rec.709?)", "log": False, "source": "đoán (không có sidecar)"}


def multipart(fields: dict, file_field: str, file_path: Path) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; '
                  f'filename="{file_path.name}"\r\nContent-Type: audio/flac\r\n\r\n').encode())
    parts.append(file_path.read_bytes())
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def transcribe(clip: Path, info: dict, voice_channel: int | None, key: str, cfg: dict,
               language: str | None, speakers: int | None) -> dict:
    t = cfg["transcribe"]
    with tempfile.TemporaryDirectory() as td:
        audio = Path(td) / (clip.stem + ".flac")
        af = f"pan=mono|c0=c{voice_channel}" if voice_channel is not None else "aformat=channel_layouts=mono"
        ffmpeg(["-i", str(clip), "-map", "0:a:0", "-af", af, "-ar", "16000", "-c:a", "flac", str(audio)])
        fields = {"model_id": t["model"], "timestamps_granularity": "word",
                  "tag_audio_events": "true" if t["audio_events"] else "false",
                  "diarize": "true" if t["diarize"] else "false"}
        lang = language or (None if t["language"] in (None, "", "auto") else t["language"])
        if lang:
            fields["language_code"] = lang
        if speakers:
            fields["num_speakers"] = str(speakers)
        body, ctype = multipart(fields, "file", audio)
        size_mb = len(body) / 1e6
        say(f"  upload {clip.name} ({size_mb:.1f} MB)")
        for attempt in range(3):
            req = urllib.request.Request(SCRIBE_URL, data=body, method="POST",
                                         headers={"xi-api-key": key, "Content-Type": ctype})
            try:
                with urllib.request.urlopen(req, timeout=1800) as r:
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                msg = e.read().decode("utf-8", "replace")[:300]
                if e.code in (401, 403):
                    die(f"speech-to-text từ chối key ({e.code}): {msg}. Kiểm tra key, quyền Speech to Text.")
                if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
                die(f"speech-to-text lỗi {e.code}: {msg}")
            except urllib.error.URLError as e:
                if attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
                die(f"không kết nối được speech-to-text: {e}")
    raise SystemExit


def tokens_from(resp: dict) -> list[dict]:
    out = []
    for w in resp.get("words", []):
        typ = w.get("type", "word")
        if typ == "spacing":
            continue
        text = (w.get("text") or "").strip()
        if not text:
            continue
        out.append({"i": len(out), "text": text, "start": round(float(w.get("start", 0)), 3),
                    "end": round(float(w.get("end", 0)), 3),
                    "type": "audio_event" if typ == "audio_event" else "word",
                    "speaker": w.get("speaker_id")})
    return out


def phrase_lines(tokens: list[dict]) -> list[str]:
    lines, cur = [], []

    def flush():
        if cur:
            spk = cur[0].get("speaker") or ""
            lines.append(f"[{cur[0]['i']}-{cur[-1]['i']}] {fmt_tc(cur[0]['start'])}  "
                         f"{(spk + '  ') if spk else ''}" + " ".join(t["text"] for t in cur))
            cur.clear()

    for t in tokens:
        if cur:
            gap = t["start"] - cur[-1]["end"]
            if gap >= 0.5 or t.get("speaker") != cur[-1].get("speaker") or \
                    (len(cur) >= 25 and re.search(r"[.!?…]$", cur[-1]["text"])):
                flush()
        cur.append(t)
    flush()
    return lines


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--language", help="mã ngôn ngữ (vi, en, pt…); mặc định theo config (auto)")
    ap.add_argument("--num-speakers", type=int)
    ap.add_argument("--retranscribe", nargs="*", default=[], metavar="CLIP",
                    help="chuyển lại giọng nói thành chữ cho các clip này (tốn tiền, hỏi trước)")
    ap.add_argument("--no-transcribe", action="store_true")
    workspace_arg(ap)
    a = ap.parse_args()
    need_tools()
    ws = find_workspace(a.workspace)
    cfg = load_config(ws, a.video)
    vd = video_dir(ws, a.video, cfg)
    clips = find_video_sources(ws, cfg, a.video)
    key = None if a.no_transcribe else load_key(ws)
    manifest = {"video": a.video, "clips": [], "warnings": []}
    md = [f"# Transcript: {a.video}", "",
          "Mỗi dòng: [chỉ số từ đầu-cuối] thời điểm trong clip  người nói  câu. "
          "Dùng words.py để xem từng từ kèm chỉ số.", ""]
    ids_seen = set()
    for clip in clips:
        cid = clip.stem if clip.stem not in ids_seen else f"{clip.parent.name}_{clip.stem}"
        ids_seen.add(cid)
        info = probe_clip(clip)
        say(f"{cid}: {info.get('duration')}s {info.get('width')}x{info.get('height')} "
            f"@{info.get('fps_float')} audio={info.get('channels', 0)}ch")
        entry = {"id": cid, "path": str(clip.relative_to(ws)) if clip.is_relative_to(ws) else str(clip),
                 "probe": info}
        if not info.get("has_video"):
            manifest["warnings"].append(f"{cid}: không có hình (file âm thanh?)")
        pp = picture_profile(clip, info)
        entry["picture_profile"] = pp
        if pp["source"].startswith("đoán"):
            manifest["warnings"].append(f"{cid}: picture profile đoán là baked (không có sidecar) — "
                                        "đừng áp LUT log nếu chưa chắc")
        if pp.get("hdr"):
            manifest["warnings"].append(f"{cid}: HDR — cần tone-map sang SDR trước khi dựng")
        if info.get("vertical"):
            manifest["warnings"].append(f"{cid}: clip dọc — sẽ bị crop mạnh trong khung ngang")
        voice_ch = None
        if info.get("has_audio") and info.get("channels", 0) >= 2:
            lv = channel_levels(clip, 0, min(120.0, info["duration"] or 120.0))
            entry["channel_rms_db"] = lv
            if len(lv) >= 2 and abs(lv[0] - lv[1]) > 15:
                voice_ch = 0 if lv[0] > lv[1] else 1
                manifest["warnings"].append(
                    f"{cid}: giọng chỉ nằm ở kênh {'trái' if voice_ch == 0 else 'phải'} "
                    f"({lv[0]:.0f} / {lv[1]:.0f} dB) — khi dựng sẽ dùng kênh đó cho cả hai bên")
        entry["voice_channel"] = voice_ch
        tokens: list[dict] = []
        if info.get("has_audio"):
            sil = silence_map(clip, cfg["cut"]["silence_db"], cfg["cut"]["silence_min"])
            for s in sil:
                if s[1] is None:
                    s[1] = info["duration"]
            write_json(vd / "silences" / f"{cid}.json", sil)
            raw_path = vd / "transcripts" / f"{cid}.json"
            words_path = vd / "words" / f"{cid}.json"
            if words_path.exists() and cid not in a.retranscribe:
                tokens = read_json(words_path, [])
                say(f"  transcript: cache ({len(tokens)} token)")
            elif not a.no_transcribe:
                if not key:
                    die("chưa có key speech-to-text (system/keys.env hoặc biến môi trường). "
                        "Dùng --no-transcribe để chỉ probe.")
                resp = transcribe(clip, info, voice_ch, key, cfg, a.language, a.num_speakers)
                write_json(raw_path, resp)
                tokens = tokens_from(resp)
                write_json(words_path, tokens)
                say(f"  transcript: {len(tokens)} token, ngôn ngữ {resp.get('language_code')}")
        n_words = sum(1 for t in tokens if t["type"] == "word")
        entry["words"] = n_words
        entry["broll"] = n_words == 0
        manifest["clips"].append(entry)
        head = f"## {cid}  ({fmt_tc(info.get('duration') or 0)}, {n_words} từ)"
        if entry["broll"]:
            head += "  — B-ROLL (không có lời): xem bằng contact_sheet.py"
        md += [head, *phrase_lines(tokens), ""]
    fps_set = {c["probe"].get("fps") for c in manifest["clips"] if c["probe"].get("fps")}
    if len(fps_set) > 1:
        manifest["warnings"].append(f"frame rate khác nhau giữa các clip: {sorted(fps_set)} — "
                                    "hỏi người dùng chọn fps timeline (settings.py <v> set timeline.fps=\"30\")")
    first = next((c for c in manifest["clips"] if not c["broll"] and c["probe"].get("has_video")),
                 next((c for c in manifest["clips"] if c["probe"].get("has_video")), None))
    if first:
        manifest["timeline_guess"] = {k: first["probe"].get(k) for k in ("width", "height", "fps")}
    write_json(vd / "manifest.json", manifest)
    (vd / "transcript.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    say(f"xong: {len(clips)} clip, {sum(c['broll'] for c in manifest['clips'])} B-roll → {vd.relative_to(ws)}")
    for w in manifest["warnings"]:
        say(f"  ! {w}")


if __name__ == "__main__":
    main()
