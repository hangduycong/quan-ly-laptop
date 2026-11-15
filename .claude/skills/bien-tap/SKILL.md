---
name: bien-tap
description: Biên tập — first-pass video editor for talking-head videos, vlogs and classes in DaVinci Resolve Studio. Transcribes footage, cuts retakes and dead air with natural vlog pacing, keeps B-roll, builds the timeline in Resolve, and helps with voice/audio, music and SFX, captions, Remotion motion graphics, Figma sync and YouTube export. Use for "biên tập", "/bien-tap", "edit the new video", "set up my video editor", or follow-up changes to a cut.
---

# Biên tập

> Nguồn: [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills), © 2026 appariciojunior, giấy phép **CC BY-NC 4.0** (được dùng, chia sẻ, chỉnh sửa miễn phí khi ghi nguồn; **không được bán** hay dùng trong sản phẩm/dịch vụ trả phí). Bộ 12 skill gốc được gộp thành skill này: `edit-video` là phần chính bên dưới, 11 skill còn lại nằm trong `references/`.
>
> Cần: **DaVinci Resolve Studio** (bản có external scripting) chạy trên máy của người dùng, ffmpeg, Python 3.9+, một API speech-to-text có word timestamps. Tùy chọn: Epidemic Sound MCP, Figma MCP, Node + Remotion.

## Bản đồ tham chiếu

Khi phần dưới (hoặc một file tham chiếu) nhắc tới một skill bằng tên, hãy đọc file tương ứng trong thư mục của skill này:

| Tên được nhắc | File | Dùng khi |
|---|---|---|
| `video-editor-setup` | `references/video-editor-setup.md` | lần đầu: thư mục, key, template Resolve, các script cần viết |
| `rough-cut` | `references/rough-cut.md` | chọn giữ/bỏ: retake, nói vấp, ghi chú cho editor |
| `vlog-pacing` | `references/vlog-pacing.md` | khoảng lặng, pad, nhịp, jump-cut zoom |
| `broll` | `references/broll.md` | tìm, xem và cắt B-roll |
| `resolve-scripting` | `references/resolve-scripting.md` | viết/sửa script điều khiển Resolve |
| `voice-and-audio` | `references/voice-and-audio.md` | chuẩn hóa âm lượng, giọng bị đục, EQ |
| `music-and-sound` | `references/music-and-sound.md` | nhạc nền, ducking, hiệu ứng âm thanh |
| `captions` | `references/captions.md` | phụ đề |
| `motion-overlays` | `references/motion-overlays.md` | đồ họa chuyển động Remotion |
| `figma-roundtrip` | `references/figma-roundtrip.md` | đồng bộ bộ đồ họa với Figma |
| `youtube-export` | `references/youtube-export.md` | thiết lập xuất video cho YouTube |

Giá trị khởi đầu: `templates/config.example.json`. Bài học từ các lần dựng thật: `LEARNINGS.md`.

Chưa có workspace (không có `raw video/`, script, `CLAUDE.md`)? Làm theo `references/video-editor-setup.md` trước.

# Edit video (the whole flow)

The creator drops footage in `raw video/`, opens their Resolve project and says "do it". You run the whole thing and stop only for:
- **a frame-rate mismatch** between footage and template timeline (ask; never choose for them),
- **a failure that happened twice** (report the script's exact error and what they must fix).

Prerequisite: `video-editor-setup` is done (folders, scripts, CLAUDE.md).

## 1. Check
Run your `doctor` script. No video named? Pick what's in `raw video/` without a finished build report; if several, ask which.

## 2. Ingest
Probe, read picture profiles, transcribe (verbatim, word timestamps), detect silences, write a manifest. Report anything odd:
- picture profile *guessed* (no camera sidecar) → say so; never put a log LUT on non-log footage;
- voice on one channel only (wireless receiver in stereo mode) → make sure the voice plays on both sides;
- mixed frame rates; **vertical clips** (they will crop hard in a horizontal or 4:3 frame).

## 3. Cut
Follow `rough-cut` for what to keep (by word index) and `vlog-pacing` for how much air to leave. Clips with no speech are B-roll: follow `broll`. A subagent ("story editor") is a good fit: give it the video name and the skills; it writes the keep-list and the markers and runs the planner.

## 4. Build
Follow `resolve-scripting`. Order inside the build:
1. footage into the footage bin;
2. copy the template timeline into the timelines bin as "<video> - Transcript cut" (v2, v3… never overwrite) and empty the copy (it keeps the track FX chain);
3. set a custom frame if asked (e.g. 4:3 2880x2160, footage *scaled to fill with crop*);
4. lay the cut on V1/A1, alternate jump-cut zoom, colour B-roll pieces green;
5. grade (log footage only);
6. markers for spoken notes (pink);
7. **audio treatment last**: Normalize Audio Level on A1 (see `voice-and-audio`).

## 5. Report and stop
Short: timeline name, raw → cut length, number of pieces, each retake removed (timestamp + a few words, translated if needed), each marker and what goes there, punch-ins, B-roll placed, anything guessed or unsure. Then stop. They watch it.

## Follow-ups (they speak in plain words)

| They say | You do |
|---|---|
| "put back X", "cut 02:14 to 02:20" | edit the keep-list, re-plan, rebuild as v2 |
| "too choppy / pops" | loosen pauses (see `vlog-pacing`), give scenes room, rebuild |
| "add music" | `music-and-sound` |
| "captions" | `captions` |
| "graphics / overlays" | `motion-overlays` |
| "my voice sounds bad" | `voice-and-audio` |
| "export settings?" | `youtube-export` |
| "always …" | change the global default, and add a dated line to CLAUDE.md |

They will often fix things by hand in the timeline you built (trims, deleted clips). **Always re-read the timeline from Resolve before the next step** (B-roll positions, what they deleted) and never put back what they removed.
