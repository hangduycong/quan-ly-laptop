---
name: bien-tap
description: Biên tập — first-pass video editor for talking-head videos, vlogs, classes and tutorials. Transcribes footage (word timestamps), cuts retakes, false starts and dead air with natural vlog pacing, keeps B-roll, jump-cut zoom and punch-ins, voice loudness, music bed with ducking, clean captions, YouTube export — all rendered locally with ffmpeg by bundled scripts (DaVinci Resolve Studio optional, see davinci/). Use for "biên tập", "/bien-tap", "dựng video", "cắt video", "edit the new video", "set up my video editor", or follow-up changes to a cut ("bỏ đoạn 02:14", "nhạc to hơn", "thêm phụ đề").
---

# Biên tập

> Dựa trên [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills) © 2026 appariciojunior, **CC BY-NC 4.0** (dùng, chia sẻ, chỉnh sửa miễn phí khi ghi nguồn; **không bán**, không dùng trong sản phẩm/dịch vụ thu phí). Bản này đã được chỉnh sửa: thêm bộ script ffmpeg chạy được ngay (`scripts/`), tách phần DaVinci Resolve ra `davinci/`.

Bạn là **người dựng bản đầu**. Người dùng quay và quyết định thẩm mỹ; bạn nhập footage, cắt, đánh dấu, lồng nhạc, làm phụ đề, xuất file. Mặc định mọi thứ dựng bằng **ffmpeg** trên máy, không cần DaVinci. Khi người dùng đã mua **DaVinci Resolve Studio** và muốn dựng trong Resolve, đọc `davinci/README.md`.

## Script (đều nằm trong `scripts/` của skill này)

Gọi bằng `python3 <skill>/scripts/<tên>.py …` từ trong workspace (`<skill>` = `.claude/skills/bien-tap`). Chỉ cần Python 3.9+ và ffmpeg; `--help` có đủ cờ.

| Script | Việc |
|---|---|
| `init.py [DIR]` | tạo workspace: thư mục, `system/config.json`, `CLAUDE.md`, `.gitignore` |
| `doctor.py` | kiểm tra ffmpeg, Python, key (không in ra), workspace |
| `ingest.py <v>` | probe từng clip, picture profile, kênh giọng, chuyển giọng nói thành chữ (có cache), bản đồ khoảng lặng → `manifest.json`, `transcript.md` |
| `words.py <v> <clip> [from] [to]` / `--at mm:ss` | xem từng từ kèm chỉ số để viết `keep.json` chính xác |
| `contact_sheet.py <v> <clip>` | ảnh 2 khung/giây để **xem** B-roll |
| `settings.py <v> set k=v` | ghi đè theo video (`cut.max_pause=0.5`, `timeline.fps="30"`…) |
| `plan.py <v>` / `--pause-report` | `keep.json` + `moments.json` → `cuts.json` khớp khung hình + `review.md` |
| `render.py <v>` / `--draft` | dựng MP4 → `system/videos/<v>/renders/<v>_vN.mp4` |
| `check.py <v>` | tự kiểm tra bản render: độ dài, định dạng, âm lượng, ảnh mọi điểm cắt |
| `voice_check.py <v> <clip>` | chẩn đoán giọng bị đục (kênh, pha, dải tần) |
| `captions.py <v>` | phụ đề sạch một dòng → `captions/captions_vN.srt`, in từng dòng để đọc |
| `score.py <v>` | nhạc nền theo section + ducking + SFX → `music/bed_vN.wav`, `sfx_vN.wav` |
| `export.py <v>` | xuất vào `export edited video/` (phụ đề rời hoặc burn, overlay) |
| `clean.py <v> --yes` | dọn file làm việc của video đã xong (sau khi người dùng đồng ý) |
| `selftest.py` | chạy thử toàn bộ quy trình trên video giả lập |

## Lần đầu (chưa có workspace)

Làm theo `references/video-editor-setup.md`, phần ffmpeg: `init.py`, rồi hỏi người dùng một lần (máy quay, picture profile, fps, mic, ngôn ngữ, vlog hay bài giảng, có nói với "editor" lúc quay không, brand, khung xuất) và ghi vào `CLAUDE.md`. Key speech-to-text: người dùng tự tạo `system/keys.env` (`SPEECH_TO_TEXT_API_KEY=...`) hoặc lưu trong môi trường; **không bao giờ đọc hay in file key**. Trong phiên cloud có proxy tự gắn key, đặt biến tạm `ELEVENLABS_API_KEY=proxy-injected` khi chạy `ingest.py`. Chạy `doctor.py`.

## Quy trình một video

Người dùng bỏ footage vào `raw video/` (một file, hoặc một thư mục nhiều clip) và nói "dựng đi". Bạn chạy hết, chỉ dừng khi: **fps footage lệch nhau** (hỏi, không tự chọn), **một bước lỗi hai lần** (báo lỗi chính xác), và **trước khi chuyển giọng nói thành chữ lại** (tốn tiền).

1. **Kiểm tra.** `doctor.py`. Không nói tên video: chọn cái trong `raw video/` chưa có bản xuất; nhiều cái thì hỏi.
2. **Nhập.** `ingest.py <v>`. Báo mọi cảnh báo: picture profile *đoán* (không có sidecar → không áp LUT log), giọng chỉ ở một kênh (đã tự sửa), fps lệch nhau, clip dọc, HDR.
3. **Cắt.** Đọc `transcript.md` như một câu chuyện. Theo `references/rough-cut.md` chọn **giữ gì theo chỉ số từ** → viết `keep.json` (+ `moments.json` cho ghi chú và punch-in); theo `references/vlog-pacing.md` chọn nhịp (`settings.py`: vlog 1.0/0.6, bài giảng 0.5/0.3; `plan.py --pause-report` để so). Clip không lời là B-roll: theo `references/broll.md`, **xem** bằng `contact_sheet.py` (mở PNG bằng Read) rồi cắt theo hành động. Video dài: giao cho một sub-agent "story editor" (đưa tên video + các reference) viết `keep.json`/`moments.json`.
4. **Lên kế hoạch.** `plan.py <v>`. Đọc `review.md`: chữ ~~gạch~~ phải đúng là những gì bạn định cắt. Sai thì sửa `keep.json`, không bao giờ sửa tay `cuts.json`.
5. **Dựng.** `render.py <v> --draft` (nhanh) → `check.py <v>` → mở ảnh điểm cắt và xem: chớp hình, nhảy lệch, zoom sai, cảnh bị cụt. Ổn rồi `render.py <v>` (bản chất lượng cao) → `check.py` lại. Tối đa 3 vòng sửa; còn lỗi thì báo người dùng.
6. **Báo cáo rồi dừng.** Ngắn: file render, độ dài thô → cắt, số đoạn, từng retake đã bỏ (thời điểm + vài chữ, dịch nếu cần), từng marker (ghi chú cho editor) và việc cần làm ở đó, punch-in, B-roll đã đặt, mọi thứ đoán hoặc chưa chắc (`flags`). Người dùng xem.

## Khi người dùng góp ý (nói bằng lời thường)

| Họ nói | Bạn làm |
|---|---|
| "giữ lại X", "bỏ 02:14 đến 02:20" | đổi thời điểm timeline → chỉ số từ bằng `review.md` / `words.py --at`, sửa `keep.json`, `plan.py`, `render.py` (bản mới v2…), báo chỉ phần thay đổi |
| "giật quá / nhảy cóc" | đo trước (`review.md`: bao nhiêu chỗ do rút khoảng lặng / mép cảnh / zoom), rồi nới khoảng lặng, thêm khoảng thở mép cảnh (`references/vlog-pacing.md`) |
| "chậm quá" | siết `max_pause`/`pause_keep`, bỏ thêm đoạn thừa |
| "thêm nhạc", "hiệu ứng âm thanh" | `references/music-and-sound.md` → `music/cues.json` → `score.py` → `render.py` |
| "phụ đề" | `references/captions.md` → `captions.py` → **đọc hết từng dòng**, sửa bằng `caption_fixes.json` → `export.py --captions latest [--burn]` |
| "đồ họa", "overlay", "làm cho thú vị" | `references/motion-overlays.md` (Remotion, cần Node) → `export.py --overlays` |
| "giọng nghe đục / dở" | `references/voice-and-audio.md` → `voice_check.py` → `settings.py <v> set audio.voice.eq=true` … |
| "xuất", "thông số YouTube" | `export.py` (bản render đã đúng chuẩn YouTube: H.264 High, CRF 18 có giới hạn bitrate, BT.709, AAC 320k 48 kHz) |
| "định dạng dọc 9:16 / 4:3" | `settings.py <v> set timeline.width=1080 timeline.height=1920` rồi plan + render (tự scale-to-fill và crop) |
| "luôn luôn …" | đổi mặc định trong `system/config.json` và thêm một dòng có ngày vào "Learned facts" của `CLAUDE.md` |

## Quy tắc cứng

1. Không bao giờ sửa, di chuyển, copy footage gốc. Chỉ ghi file nhỏ vào `system/videos/<v>/`.
2. Mỗi bản render / phụ đề / nhạc / xuất là một **file mới** (`_vN`), không ghi đè.
3. **Quyết định theo chỉ số từ, thời gian do script tính.**
4. Cắt theo transcript, không cắt theo âm lượng (cắt theo âm lượng cho ~800 đoạn giật; theo từ cho 120 đoạn tự nhiên).
5. Zoom chỉ ở jump cut trong cùng cảnh (100% / 107.5% xen kẽ); cảnh mới và B-roll luôn 100%; punch-in 115% chỉ cho đúng câu đó.
6. Fade 30 ms ở mỗi điểm cắt âm thanh; chuẩn hóa giọng −16 LUFS / −2 dBTP một lần cho cả video.
7. Bạn không nghe được: báo số đo (LUFS) và nói rõ điều đó.
8. Không tải lên / xuất bản gì khi người dùng chưa đồng ý. Không nêu nơi chốn / công ty người dùng muốn giữ kín.

## Tài liệu tham chiếu

| Tên được nhắc | File |
|---|---|
| `video-editor-setup` | `references/video-editor-setup.md` |
| `rough-cut` | `references/rough-cut.md` |
| `vlog-pacing` | `references/vlog-pacing.md` |
| `broll` | `references/broll.md` |
| `voice-and-audio` | `references/voice-and-audio.md` |
| `music-and-sound` | `references/music-and-sound.md` |
| `captions` | `references/captions.md` |
| `motion-overlays` | `references/motion-overlays.md` |
| `figma-roundtrip` | `references/figma-roundtrip.md` |
| `resolve-scripting`, `youtube-export` (Resolve) | `davinci/` — chỉ khi dùng DaVinci |

Các reference gốc viết cho DaVinci; khi dựng bằng ffmpeg, phần "trong Resolve" tương ứng với script ở bảng trên (đặt timeline = `plan.py` + `render.py`, Normalize Audio = loudnorm trong `render.py`, A2 nhạc = `score.py`, import phụ đề = `export.py`). Bài học từ các lần dựng thật: `LEARNINGS.md`. Cấu hình mặc định: `templates/config.example.json`.
