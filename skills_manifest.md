# skills_manifest.md

Danh sách **31 skill** của dự án (thư mục `.claude/skills/`): tên, chức năng và câu lệnh thực thi. Sinh tự động từ frontmatter của từng `SKILL.md` và từ các script thật trong thư mục; mọi đường dẫn script bên dưới đã được kiểm tra là tồn tại.

## Cách chạy một skill

- **Trong Claude Code:** gõ `/<tên-skill>` (ví dụ `/bien-tap`) hoặc mô tả việc bằng lời (Claude tự chọn skill theo phần mô tả).
- **Chạy script của skill trực tiếp:** các lệnh bên dưới, chạy từ **gốc repo** (`/home/user/quan-ly-laptop`). `<…>` là tham số bạn điền; `[…]` là tùy chọn.
- Skill không có script (chỉ hướng dẫn) ghi rõ "không có script": Claude đọc `SKILL.md` rồi làm theo.
- Bản gốc của skill nhập từ ngoài nằm trong `goc/` (hoặc `goi/`); mỗi skill có `LICENSE` + `NOTICE.md`.

## Bảng tổng

| # | Skill | Nhóm | Gọi |
|---:|---|---|---|
| 1 | `chinh-sua-video` | Dựng / chỉnh video | `/chinh-sua-video` |
| 2 | `chinh-sua-video-dai` | Dựng / chỉnh video | `/chinh-sua-video-dai` |
| 3 | `bien-tap` | Dựng / chỉnh video | `/bien-tap` |
| 4 | `ffmpeg-skill` | Dựng / chỉnh video | `/ffmpeg-skill` |
| 5 | `ho-tro-tao-video` | Tạo video / đồ họa | `/ho-tro-tao-video` |
| 6 | `video-ra-mat-du-an` | Tạo video / đồ họa | `/video-ra-mat-du-an` |
| 7 | `cong-cu-san-xuat-video` | Tạo video / đồ họa | `/cong-cu-san-xuat-video` |
| 8 | `tao-do-hoa-chuyen-dong` | Tạo video / đồ họa | `/tao-do-hoa-chuyen-dong` |
| 9 | `video-tiktok` | Tạo video / đồ họa (gói iart-ai) | `/video-tiktok` |
| 10 | `video-tin-nhan` | Tạo video / đồ họa (gói iart-ai) | `/video-tin-nhan` |
| 11 | `chu-chuyen-dong` | Tạo video / đồ họa (gói iart-ai) | `/chu-chuyen-dong` |
| 12 | `video-ban-hang` | Tạo video / đồ họa (gói iart-ai) | `/video-ban-hang` |
| 13 | `video-quang-cao` | Tạo video / đồ họa (gói iart-ai) | `/video-quang-cao` |
| 14 | `bieu-do-dong` | Tạo video / đồ họa (gói iart-ai) | `/bieu-do-dong` |
| 15 | `video-giai-thich` | Tạo video / đồ họa (gói iart-ai) | `/video-giai-thich` |
| 16 | `ban-do-dong` | Tạo video / đồ họa (gói iart-ai) | `/ban-do-dong` |
| 17 | `animation-web` | Tạo video / đồ họa (gói iart-ai) | `/animation-web` |
| 18 | `video-toan-hoc-manim` | Tạo video / đồ họa (gói iart-ai) | `/video-toan-hoc-manim` |
| 19 | `minh-hoa-ai-chuyen-dong` | Tạo video / đồ họa (gói iart-ai) | `/minh-hoa-ai-chuyen-dong` |
| 20 | `animation-javascript` | Tạo video / đồ họa (gói iart-ai) | `/animation-javascript` |
| 21 | `lower-third` | Tạo video / đồ họa (gói iart-ai) | `/lower-third` |
| 22 | `b-roll-cho-video` | Tạo video / đồ họa (gói iart-ai) | `/b-roll-cho-video` |
| 23 | `video-nguoi-noi-ai` | Tạo video / đồ họa (gói iart-ai) | `/video-nguoi-noi-ai` |
| 24 | `video-youtube` | YouTube | `/video-youtube` |
| 25 | `cat-video-dai-thanh-shorts` | YouTube | `/cat-video-dai-thanh-shorts` |
| 26 | `tro-ly-kenh-youtube` | YouTube | `/tro-ly-kenh-youtube` |
| 27 | `chien-luoc-kenh-youtube` | YouTube | `/chien-luoc-kenh-youtube` |
| 28 | `ho-tro-danh-sach-canh-quay` | Đạo diễn / kịch bản | `/ho-tro-danh-sach-canh-quay` |
| 29 | `mo-phong-cong-viec-dao-dien` | Đạo diễn / kịch bản | `/mo-phong-cong-viec-dao-dien` |
| 30 | `tuan-thu-quy-trinh` | Quy trình / công cụ phát triển | `/tuan-thu-quy-trinh` |
| 31 | `tao-skill-rieng-theo-nhu-cau` | Quy trình / công cụ phát triển | `/tao-skill-rieng-theo-nhu-cau` |

## Dựng / chỉnh video

### `chinh-sua-video`

**Chức năng:** Chỉnh sửa video qua hội thoại (video-use): chuyển giọng nói thành chữ có mốc từng từ (ElevenLabs Scribe), cắt, chỉnh màu, hoạt hình chèn, phụ đề. Cần `ELEVENLABS_API_KEY`.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Cài phụ thuộc | `pip install -e .claude/skills/chinh-sua-video` |
| Chuyển giọng nói thành chữ | `python3 .claude/skills/chinh-sua-video/helpers/transcribe.py <video>` |
| Chuyển hàng loạt | `python3 .claude/skills/chinh-sua-video/helpers/transcribe_batch.py <thư_mục_video>` |
| Gói transcript để đọc | `python3 .claude/skills/chinh-sua-video/helpers/pack_transcripts.py --edit-dir <edit_dir>` |
| Xem khung + sóng âm một đoạn | `python3 .claude/skills/chinh-sua-video/helpers/timeline_view.py <video> <bắt_đầu_s> <kết_thúc_s>` |
| Dựng từ EDL | `python3 .claude/skills/chinh-sua-video/helpers/render.py <edl.json> -o final.mp4 [--preview|--draft] [--build-subtitles]` |
| Chỉnh màu | `python3 .claude/skills/chinh-sua-video/helpers/grade.py <vào.mp4> -o <ra.mp4> [--preset warm_cinematic]` |

### `chinh-sua-video-dai`

**Chức năng:** Như `chinh-sua-video` kèm mục "Video dài": chia nguồn dài, bản đồ chương, dựng từng chương, ghép chương + chuẩn hóa âm lượng một lần, mốc chương YouTube. Cần `ELEVENLABS_API_KEY`.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Cài phụ thuộc | `pip install -e .claude/skills/chinh-sua-video-dai` |
| Chuyển giọng nói thành chữ | `python3 .claude/skills/chinh-sua-video-dai/helpers/transcribe_batch.py <thư_mục_video>` |
| Gói transcript | `python3 .claude/skills/chinh-sua-video-dai/helpers/pack_transcripts.py --edit-dir <edit_dir>` |
| Dựng một chương | `python3 .claude/skills/chinh-sua-video-dai/helpers/render.py edit/chapters/ch01/edl.json -o ch01.mp4 --draft --fps 30 --no-loudnorm` |
| Ghép chương | `ffmpeg -f concat -safe 0 -i edit/_chapters_concat.txt -c copy edit/joined.mp4` |

### `bien-tap`

**Chức năng:** Dựng bản đầu video nói trước camera / vlog / bài giảng bằng ffmpeg: nhập footage, chuyển giọng nói thành chữ, cắt retake + khoảng lặng theo từng từ, B-roll, zoom, chuẩn hóa giọng, phụ đề sạch, nhạc nền tự hạ khi có lời, xuất chuẩn YouTube. DaVinci Resolve tùy chọn (`davinci/`). Bản gốc CC BY-NC (không thương mại).

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Tạo workspace | `python3 .claude/skills/bien-tap/scripts/init.py [DIR]` |
| Kiểm tra môi trường | `python3 .claude/skills/bien-tap/scripts/doctor.py` |
| Nhập + transcript | `python3 .claude/skills/bien-tap/scripts/ingest.py <video> [--language vi]` |
| Xem từ / chỉ số | `python3 .claude/skills/bien-tap/scripts/words.py <video> <clip> [từ] [đến]` |
| Xem B-roll | `python3 .claude/skills/bien-tap/scripts/contact_sheet.py <video> <clip>` |
| Chỉnh theo video | `python3 .claude/skills/bien-tap/scripts/settings.py <video> set cut.max_pause=0.5` |
| Lập kế hoạch cắt | `python3 .claude/skills/bien-tap/scripts/plan.py <video> [--pause-report]` |
| Dựng | `python3 .claude/skills/bien-tap/scripts/render.py <video> [--draft] [--no-music]` |
| Tự kiểm tra | `python3 .claude/skills/bien-tap/scripts/check.py <video>` |
| Chẩn đoán giọng | `python3 .claude/skills/bien-tap/scripts/voice_check.py <video> <clip>` |
| Phụ đề | `python3 .claude/skills/bien-tap/scripts/captions.py <video> [--render FILE] [--resolve]` |
| Nhạc + SFX | `python3 .claude/skills/bien-tap/scripts/score.py <video> [--bed-only|--sfx-only|--off]` |
| Xuất | `python3 .claude/skills/bien-tap/scripts/export.py <video> [--captions latest] [--burn] [--overlays overlays.json]` |
| Dọn | `python3 .claude/skills/bien-tap/scripts/clean.py <video> --yes` |
| Thử toàn quy trình | `python3 .claude/skills/bien-tap/scripts/selftest.py` |

### `ffmpeg-skill`

**Chức năng:** 42 công cụ FFmpeg chạy cục bộ, chỉ dùng thư viện chuẩn Python: cắt, ghép, bỏ khoảng lặng, đổi khung, phụ đề / karaoke, overlay, màu / LUT, âm thanh, chuẩn hóa loudness, xuất theo nền tảng, kiểm tra thành phẩm. Cần FFmpeg 6.1+.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Kiểm tra môi trường | `python3 .claude/skills/ffmpeg-skill/scripts/_contract.py doctor` |
| Chạy một công cụ | `python3 .claude/skills/ffmpeg-skill/scripts/<tên>.py <vào> [-o ra] [--dry-run] [--json]` |
| Ví dụ: đọc thông số | `python3 .claude/skills/ffmpeg-skill/scripts/probe.py video.mp4 --json-brief` |
| Ví dụ: đổi sang video dọc | `python3 .claude/skills/ffmpeg-skill/scripts/fit.py in.mp4 --aspect 9:16 --fit crop -o v.mp4` |
| Ví dụ: kiểm tra chuẩn nền tảng | `python3 .claude/skills/ffmpeg-skill/scripts/check.py v.mp4` |
| Công cụ có sẵn | `audio, background, batch, broll, caption, check, color, crop, cropdetect, cut, deinterlace, denoise, export, fit, freeze, graphics, grid, insert, join, look, loop, loudness, metadata, multicam, overlay, pad, probe, proxy, redact, render, report, reverse, scenes, sequence, silence, speedramp, sphere, stabilize, straighten, sync, verify, waveform` |

## Tạo video / đồ họa

### `ho-tro-tao-video`

**Chức năng:** Tạo video từ HTML bằng HyperFrames (HTML + CSS + GSAP render từng khung ra MP4): phim giới thiệu, giải thích, biểu đồ, bản đồ, clip dọc, tiêu đề chữ động, slideshow; gồm 9 skill gốc trong `goc/`. Cần Node 22+, Chrome, ffmpeg.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Tạo project | `npx hyperframes init <thư_mục> --skip-skills --skill=hyperframes` |
| Tắt thu thập dữ liệu | `npx hyperframes telemetry disable` |
| Kiểm tra | `npx hyperframes check --json` |
| Xem trước | `npx hyperframes preview` |
| Render MP4 | `npx hyperframes render` |

### `video-ra-mat-du-an`

**Chức năng:** Đọc code dự án rồi làm video ra mắt ngắn bằng HyperFrames (chuyển động + nhạc + SFX + lời chia sẻ). Nhạc kèm theo CC BY 4.0: phải ghi công Sascha Ende.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-ra-mat-du-an   (hoặc /brag, /brag-slim)` |
| Kiểm tra bố cục | `npx hyperframes check   (trong <output-dir>/composition/)` |
| Render | `npx hyperframes render` |
| Phân tích nhịp nhạc | `python3 .claude/skills/video-ra-mat-du-an/goc/brag/scripts/analyze_music_cues.py <track>` |

### `cong-cu-san-xuat-video`

**Chức năng:** claude-code-video-toolkit: biến đề bài thành MP4 có QC (kịch bản, lồng tiếng AI, ảnh, clip AI, nhạc, phụ đề, Remotion, moviepy, Blender tùy chọn); sửa video có sẵn (lồng tiếng lại, cắt dọc, highlight). Dùng dịch vụ trả phí (GPU cloud): hỏi trước.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Tải + cài bộ công cụ | `bash .claude/skills/cong-cu-san-xuat-video/scripts/cai-dat.sh [thư_mục]` |
| Kiểm tra | `cd $VIDEO_TOOLKIT_ROOT && uv run tools/verify_setup.py` |
| Ước tính chi phí | `uv run tools/video_job.py estimate <spec.json>` |
| Gửi job / theo dõi / lấy kết quả | `uv run tools/video_job.py submit <spec.json> ; uv run tools/video_job.py status <job_id> ; uv run tools/video_job.py result <job_id>` |

### `tao-do-hoa-chuyen-dong`

**Chức năng:** Mục lục + cửa vào 56 workflow đồ họa chuyển động (19 gói iart-ai): chọn gói theo nhu cầu rồi mở `goi/<gói>/skills/<skill>/SKILL.md`; tra đủ danh sách ở `MUC-LUC.md`.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/tao-do-hoa-chuyen-dong` |
| Render Remotion | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 | `bash .claude/skills/tao-do-hoa-chuyen-dong/goi/tiktok-video-skills/scripts/probe-mp4.sh out.mp4 1080x1920 30` |

## Tạo video / đồ họa (gói iart-ai)

### `video-tiktok`

**Chức năng:** Video dọc TikTok / Reels / Shorts: hook, nhịp giữ chân, phụ đề karaoke, đếm ngược, lower third (4 skill con).

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-tiktok` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/video-tiktok/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/video-tiktok/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `video-tin-nhan`

**Chức năng:** Video kể chuyện bằng tin nhắn kiểu iMessage / WhatsApp: bong bóng chat, dấu đang gõ.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-tin-nhan` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/video-tin-nhan/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/video-tin-nhan/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `chu-chuyen-dong`

**Chức năng:** Chữ chuyển động (kinetic typography): tách chữ / từ / dòng, font biến thiên, lời bài hát, title.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/chu-chuyen-dong` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/chu-chuyen-dong/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/chu-chuyen-dong/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `video-ban-hang`

**Chức năng:** Video bán hàng: demo sản phẩm / app, khuyến mãi (giá cũ → giá mới), slideshow ảnh có Ken Burns.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-ban-hang` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/video-ban-hang/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/video-ban-hang/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `video-quang-cao`

**Chức năng:** Video quảng cáo: biến thể A/B, video ra mắt cắt theo beat, testimonial / review khách hàng.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-quang-cao` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/video-quang-cao/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/video-quang-cao/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `bieu-do-dong`

**Chức năng:** Biểu đồ động từ CSV, infographic động, slide / pitch deck thành video.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/bieu-do-dong` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/bieu-do-dong/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/bieu-do-dong/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `video-giai-thich`

**Chức năng:** Video giải thích: kịch bản + storyboard + thuyết minh, sơ đồ hiện từng bước, isometric, whiteboard, tổng kết năm.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-giai-thich` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/video-giai-thich/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/video-giai-thich/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `ban-do-dong`

**Chức năng:** Bản đồ động kiểu Vox: zoom, tuyến đường, vùng tô sáng, ghim.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/ban-do-dong` |
| Render (Remotion, trong project của bạn) | `npx remotion render <Composition> out/<tên>.mp4 --props=./props.json` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/ban-do-dong/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/ban-do-dong/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `animation-web`

**Chức năng:** Animation cho website (GSAP, SVG, Lottie, chuyển trang, micro-interaction, 60fps, reduced-motion); 9 skill con.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/animation-web` |
| Chạy thử trên trình duyệt | `mở trang / chạy dev server của website rồi chụp ảnh kiểm tra (Playwright)` |
| Kiểm tra MP4 (độ phân giải, fps, thời lượng) | `bash .claude/skills/animation-web/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |
| Ảnh tổng hợp khung hình | `bash .claude/skills/animation-web/goc/scripts/contact-sheet.sh sheet.png f1.png f2.png f3.png` |

### `video-toan-hoc-manim`

**Chức năng:** Video toán / vật lý / tin học kiểu 3Blue1Brown bằng Manim CE: phương trình LaTeX, đồ thị, ValueTracker, 3D.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-toan-hoc-manim` |
| Cài | `pip install manim` |
| Render | `manim -qm scene.py <TênScene>` |
| Kiểm tra MP4 | `bash .claude/skills/video-toan-hoc-manim/goc/scripts/probe-mp4.sh out.mp4 1920x1080 30` |

### `minh-hoa-ai-chuyen-dong`

**Chức năng:** Minh họa AI chuyển động: tạo nhiều mảnh nhỏ, tách nền, ghép sprite, animate bằng code, render khung chính xác. Có thể gọi dịch vụ ảnh AI tính phí.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/minh-hoa-ai-chuyen-dong` |
| Render | `xem khung render trong goc/skills/generative-illustration/ (Node + Playwright + ffmpeg)` |

### `animation-javascript`

**Chức năng:** Phim hoạt hình vẽ từng khung bằng JavaScript (canvas), không cần ảnh có sẵn; kèm nhạc nền tổng hợp bằng code khớp nhịp cắt.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/animation-javascript` |
| Render MP4 | `node .claude/skills/animation-javascript/goc/skills/javascript-animation/scripts/render.mjs piece.html piece.mp4` |
| Ảnh tổng hợp / khung cụ thể | `node .claude/skills/animation-javascript/goc/skills/javascript-animation/scripts/render.mjs piece.html sheet.jpg --sheet 1` |
| Kiểm tra không dùng asset | `node .claude/skills/animation-javascript/goc/skills/javascript-animation/scripts/asset-audit.mjs piece.html` |
| Kiểm tra nhịp nhạc | `node .claude/skills/animation-javascript/goc/skills/soundtrack/scripts/sync-check.mjs piece.mp4 --cues-file piece.cues.json` |

### `lower-third`

**Chức năng:** Lower third và overlay truyền hình dạng video nền trong suốt (WebM alpha, ProRes 4444) cho OBS / Premiere / DaVinci.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/lower-third` |
| Kiểm tra | `node .claude/skills/lower-third/goc/skills/lower-thirds/scripts/render.mjs page.html --check` |
| Ảnh tĩnh trên nền ô vuông / tối / sáng | `node .claude/skills/lower-third/goc/skills/lower-thirds/scripts/render.mjs page.html shot --stills 3s` |
| Render WebM alpha | `node .claude/skills/lower-third/goc/skills/lower-thirds/scripts/render.mjs page.html out.webm` |

### `b-roll-cho-video`

**Chức năng:** Thêm b-roll đồ họa vào video nói trước camera, bám theo từng câu nói (chuyển chữ ElevenLabs, quyết định từng câu, vẽ đồ họa, ghép).

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/b-roll-cho-video` |
| Kiểm tra | `node .claude/skills/b-roll-cho-video/goc/skills/talking-head-b-roll/scripts/render.mjs page.html --check` |
| Render phim | `node .claude/skills/b-roll-cho-video/goc/skills/talking-head-b-roll/scripts/render.mjs page.html film.mp4` |
| Render b-roll nền trong suốt | `node .claude/skills/b-roll-cho-video/goc/skills/talking-head-b-roll/scripts/render.mjs page.html b-roll.webm` |

### `video-nguoi-noi-ai`

**Chức năng:** Tạo video người nói bằng AI từ ảnh + giọng của CHÍNH người dùng (hoặc người đã đồng ý), ElevenLabs + fal.ai; dịch vụ trả phí, cần `FAL_KEY`.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/video-nguoi-noi-ai` |
| Trợ giúp | `node .claude/skills/video-nguoi-noi-ai/goc/skills/talking-head/scripts/talking-head.mjs --help` |
| Chuẩn bị người | `node .claude/skills/video-nguoi-noi-ai/goc/skills/talking-head/scripts/talking-head.mjs prepare-person --video inputs/me.mov --out inputs/person` |
| Chạy thử (không tốn phí) | `node .claude/skills/video-nguoi-noi-ai/goc/skills/talking-head/scripts/talking-head.mjs generate --plan plan.json --out runs/intro --dry-run` |
| Tạo | `node .claude/skills/video-nguoi-noi-ai/goc/skills/talking-head/scripts/talking-head.mjs generate --plan plan.json --out runs/intro` |
| Dựng phim | `node .claude/skills/video-nguoi-noi-ai/goc/skills/talking-head/scripts/talking-head.mjs render --manifest runs/intro/film.json` |

## YouTube

### `video-youtube`

**Chức năng:** Intro kênh (logo bật đúng tiếng hit), outro / end screen chừa vùng cho YouTube, audiogram podcast (16:9, 1:1, 9:16). Kèm project Remotion + font tiếng Việt.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Cài project | `cp -r .claude/skills/video-youtube/template <thư_mục>; cd <thư_mục>; npm install` |
| Tạo sting giả | `bash .claude/skills/video-youtube/scripts/make_sting.sh public/sting.wav 0.8` |
| Tìm khung có tiếng hit | `python3 .claude/skills/video-youtube/scripts/find_impact.py public/sting.wav --props brand.json` |
| SRT → audiogram | `python3 .claude/skills/video-youtube/scripts/srt_to_json.py captions.srt --into audiogram.json` |
| Render intro / outro | `npx remotion render Intro out/intro.mp4 --props=./brand.json ; npx remotion render Outro out/outro.mp4 --props=./brand.json` |
| Render audiogram dọc | `npx remotion render AudiogramVertical out/audiogram-9x16.mp4 --props=./audiogram.json` |
| Nhiều kênh | `bash .claude/skills/video-youtube/scripts/render_all.sh` |
| Kiểm tra MP4 | `bash .claude/skills/video-youtube/goc/scripts/probe-mp4.sh out/intro.mp4 1920x1080 30` |

### `cat-video-dai-thanh-shorts`

**Chức năng:** Cắt video dài thành Shorts / Reels / TikTok: whisper chuyển chữ, Claude chấm đoạn, reframe 9:16 theo khuôn mặt, phụ đề động Remotion, xuất đúng chuẩn nền tảng.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Cài (nặng, hỏi trước) | `bash .claude/skills/cat-video-dai-thanh-shorts/goc/setup.sh` |
| Kiểm tra | `bash .claude/skills/cat-video-dai-thanh-shorts/goc/scripts/preflight.sh <video> [OUTPUT_DIR]` |
| Chuyển chữ | `python3 .claude/skills/cat-video-dai-thanh-shorts/goc/scripts/transcribe.py <video> --language vi` |
| Chọn đoạn / snap / reframe | `python3 .claude/skills/cat-video-dai-thanh-shorts/goc/scripts/detect_content.py <video> ; python3 .../snap_boundaries.py ; python3 .../compute_reframe.py` |
| Render phụ đề | `node .claude/skills/cat-video-dai-thanh-shorts/goc/remotion/render.mjs ...` |
| Xuất + kiểm tra | `bash .claude/skills/cat-video-dai-thanh-shorts/goc/scripts/export.sh ... ; bash .claude/skills/cat-video-dai-thanh-shorts/goc/scripts/validate.sh --output-dir ./shorts/` |

### `tro-ly-kenh-youtube`

**Chức năng:** 11 công cụ nhỏ cho kênh YouTube: kịch bản + hook, tiêu đề + thumbnail, SEO, chapters, chọn Shorts, danh sách cắt, retention, lịch đăng, trả lời bình luận, audit, tìm video viral.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Chấm hook | `python3 .claude/skills/tro-ly-kenh-youtube/goc/skills/yt-script/hookscore.py --hook "<câu mở đầu>"` |
| Kiểm tra tiêu đề + thumbnail | `python3 .claude/skills/tro-ly-kenh-youtube/goc/skills/yt-package/title.py --title "<tiêu đề>" --thumb "<chữ thumbnail>"` |
| Chapters từ transcript | `python3 .claude/skills/tro-ly-kenh-youtube/goc/skills/yt-chapters/chapters.py transcript.srt [--target 7]` |
| Danh sách cắt (khoảng lặng, nói lại) | `python3 .claude/skills/tro-ly-kenh-youtube/goc/skills/yt-edit/deadair.py transcript.srt` |
| Phân tích retention | `python3 .claude/skills/tro-ly-kenh-youtube/goc/skills/yt-retention/retention.py retention.csv [--transcript transcript.srt]` |
| Xếp hạng video viral | `python3 .claude/skills/tro-ly-kenh-youtube/goc/skills/yt-viral/swipe.py collected.json` |

### `chien-luoc-kenh-youtube`

**Chức năng:** Bộ điều phối 14 skill con: audit kênh, SEO, kịch bản, thumbnail, chiến lược, lịch nội dung, Shorts, phân tích số liệu, kiếm tiền, đối thủ, tái sử dụng video. Dữ liệu thật qua YouTube API (tùy chọn, cần `YOUTUBE_API_KEY`).

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Lấy dữ liệu kênh | `python3 .claude/skills/chien-luoc-kenh-youtube/goc/execution/fetch_channel_data.py @<handle> [--videos 20]` |
| Lấy transcript video | `python3 .claude/skills/chien-luoc-kenh-youtube/goc/execution/fetch_transcript.py <VIDEO_ID> [--format text]` |
| Tìm video đối thủ | `python3 .claude/skills/chien-luoc-kenh-youtube/goc/execution/search_competitor_videos.py "<từ khóa>" [--order viewCount]` |
| Analytics video | `python3 .claude/skills/chien-luoc-kenh-youtube/goc/execution/fetch_video_analytics.py <VIDEO_ID> [--days 90]` |

## Đạo diễn / kịch bản

### `ho-tro-danh-sach-canh-quay`

**Chức năng:** Đóng vai đạo diễn + giám sát previs (DirectorSKILL): beat sheet, bảng danh sách cảnh quay tiếng Việt, dàn dựng, keyframe, prompt video AI, kế hoạch âm thanh / dựng, chẩn đoán lỗi video AI; 20 phong cách đạo diễn.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/ho-tro-danh-sach-canh-quay` |
| Mẫu bảng | `.claude/skills/ho-tro-danh-sach-canh-quay/mau-danh-sach-canh-quay.md  (không có script)` |

### `mo-phong-cong-viec-dao-dien`

**Chức năng:** Viết prompt theo kỷ luật kịch tính cho video AI (Seedance, Kling, Veo…) và ảnh AI (Nano Banana, GPT Image): storyboard, treatment, keyframe, sửa prompt. CC BY 4.0: ghi công Serge Shima.

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/mo-phong-cong-viec-dao-dien` |
| Ghi chú | `chỉ viết prompt, không có script / không tự tạo ảnh` |

## Quy trình / công cụ phát triển

### `tuan-thu-quy-trinh`

**Chức năng:** Superpowers: 15 skill quy trình phát triển có kỷ luật (brainstorming, kế hoạch, TDD, debug có hệ thống, xác minh trước khi báo xong, review code, worktree, kết thúc nhánh).

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/tuan-thu-quy-trinh   (đọc goc/<tên>/SKILL.md theo bảng trong SKILL.md)` |
| Bản phác trực quan khi brainstorm | `bash .claude/skills/tuan-thu-quy-trinh/goc/brainstorming/scripts/start-server.sh ; bash .claude/skills/tuan-thu-quy-trinh/goc/brainstorming/scripts/stop-server.sh` |
| Tìm test gây nhiễu | `bash .claude/skills/tuan-thu-quy-trinh/goc/systematic-debugging/find-polluter.sh <...>` |

### `tao-skill-rieng-theo-nhu-cau`

**Chức năng:** Tạo / sửa / kiểm thử skill (Anthropic skill-creator + quy ước repo + hướng dẫn nhập skill từ GitHub).

**Câu lệnh thực thi:**

| Việc | Lệnh |
|---|---|
| Gọi | `/tao-skill-rieng-theo-nhu-cau` |
| Kiểm tra mọi skill | `python3 .claude/skills/tao-skill-rieng-theo-nhu-cau/scripts/kiem_tra_skill.py .claude/skills` |
| Kiểm tra một skill | `python3 .claude/skills/tao-skill-rieng-theo-nhu-cau/scripts/kiem_tra_skill.py .claude/skills/<tên>` |
| Kiểm tra frontmatter (bản gốc) | `python3 .claude/skills/tao-skill-rieng-theo-nhu-cau/goc/skill-creator/scripts/quick_validate.py .claude/skills/<tên>` |

## Công cụ của dự án phim "Mùa Cuối Của Mẹ" (không phải skill)

Nằm ở `phim-gia-dinh/cong-cu/`; dùng các skill ở trên. Chi tiết: `phim-gia-dinh/README.md`.

| Việc | Lệnh |
|---|---|
| Sinh prompt bối cảnh + keyframe + chuyển động tập 1 | `python3 phim-gia-dinh/cong-cu/tao_prompt_tap01.py` |
| Dựng animatic tập 1 (ảnh 3D nếu có) | `python3 phim-gia-dinh/cong-cu/tao_animatic_tap01.py` |
| Dựng 7 nhân vật 3D bằng Blender (cần `bpy`) | `.venv-bpy/bin/python phim-gia-dinh/cong-cu/dung_nhan_vat_blender.py` |
| Ghép bảng nhân vật | `python3 phim-gia-dinh/cong-cu/ghep_bang_nhan_vat.py <thư_mục_raw>` |
| Dựng 8 bộ cảnh 3D + 88 ảnh bố cục | `.venv-bpy/bin/python phim-gia-dinh/cong-cu/dung_canh_3d_tap01.py [--scenes N] [--shots N]` |
| Ghép bảng cảnh 3D | `python3 phim-gia-dinh/cong-cu/ghep_bang_canh_3d.py` |

## Yêu cầu chung và lưu ý

- **Công cụ:** `ffmpeg`, Python 3.9+; Node 22+ cho Remotion / HyperFrames / Playwright; `uv` cho `cong-cu-san-xuat-video`; Blender qua gói `bpy` cho cảnh 3D.
- **Dịch vụ trả phí / key:** `ELEVENLABS_API_KEY` (chuyển giọng nói thành chữ, lồng tiếng), `FAL_KEY` (video người nói AI), `YOUTUBE_API_KEY` (dữ liệu kênh), GPU cloud (Modal / RunPod). Hỏi người dùng trước khi dùng; không in key, không ghi vào repo.
- **Giấy phép:** `bien-tap` là CC BY-NC (không thương mại); `mo-phong-cong-viec-dao-dien` CC BY 4.0 (ghi công Serge Shima); `video-ra-mat-du-an` có nhạc CC BY 4.0 (ghi công Sascha Ende); còn lại MIT / Apache 2.0.
- **Chưa chạy thử:** các skill iart-ai (trừ `lower-third`, `video-youtube`), `cat-video-dai-thanh-shorts`, `tro-ly-kenh-youtube`, `chien-luoc-kenh-youtube`, `video-ra-mat-du-an`, `video-nguoi-noi-ai`, `cong-cu-san-xuat-video` (phần render / API); mỗi skill ghi trạng thái kiểm tra trong `SKILL.md`.
- **Kiểm tra cấu trúc mọi skill:** `python3 .claude/skills/tao-skill-rieng-theo-nhu-cau/scripts/kiem_tra_skill.py .claude/skills`
