---
name: cong-cu-san-xuat-video
description: 'Công cụ sản xuất video — claude-code-video-toolkit (Digital Samba) turns a brief into a finished, QC-checked MP4 - script, AI voiceover, images, AI video clips, music, captions, talking heads, Remotion templates (product demo, release notes, sprint review, data charts), moviepy ad spots, optional Blender 3D; plus tools to redub, add music, cut down to vertical, make highlights, burn subtitles. One-prompt "job" route (estimate, submit, poll, result) or a working-session route. Use for "công cụ sản xuất video", "sản xuất video", "làm video từ kịch bản", "video explainer có thuyết minh AI", "video demo sản phẩm", "lồng tiếng lại", "cắt video dọc", "/cong-cu-san-xuat-video".'
---

# Công cụ sản xuất video (claude-code-video-toolkit)

> Nguồn: [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (MIT, `LICENSE`), commit `01e85f4` (14/11/2026). Bộ công cụ nặng ~61 MB và chạy từ thư mục gốc của chính nó, nên không chép vào đây: `scripts/cai-dat.sh` tải đúng commit đó. `goc/video-toolkit/SKILL.md` là hướng dẫn agent gốc (đọc kỹ trước khi làm). File này là phần viết thêm.

Bộ công cụ biến một đề bài thành MP4 hoàn chỉnh: viết kịch bản, lồng tiếng AI, tạo ảnh / clip video AI, nhạc, phụ đề, dựng bằng Remotion hoặc moviepy, rồi tự kiểm tra chất lượng (QC). Dùng các model mã nguồn mở chạy trên GPU cloud của người dùng (thuyết minh ~0,01 USD, clip video AI ~0,23 USD).

## Cài đặt (một lần, hỏi người dùng trước)

1. `bash <skill>/scripts/cai-dat.sh [thư mục]` — mặc định `$VIDEO_TOOLKIT_ROOT` hoặc `~/claude-code-video-toolkit`; tải đúng commit đã ghi, chạy `uv sync` (Python deps vào `.venv` của bộ công cụ). Cần git, `uv`, Node.js 22+, ffmpeg.
2. `export VIDEO_TOOLKIT_ROOT=<thư mục>`; **mọi lệnh chạy từ thư mục gốc đó**, không chạy trong thư mục dự án con.
3. `uv run tools/verify_setup.py` — xem còn thiếu gì ([x] là sẵn sàng).
4. Thiết lập GPU cloud, lưu trữ, giọng: làm theo `$VIDEO_TOOLKIT_ROOT/.claude/commands/setup.md` (lệnh `/setup` của bộ công cụ). Gợi ý của tác giả: **Modal** (gói Starter có 30 USD/tháng miễn phí) hoặc RunPod; lưu file trên **Cloudflare R2** (10 GB miễn phí).
5. Không có key nào cũng thử được: `cd examples/hello-world && npm install && npm run render` (render MP4 mẫu, không gọi dịch vụ ngoài).

## Chọn đường làm

Đọc bảng "pick a route" trong `goc/video-toolkit/SKILL.md`; tóm tắt:

| Người dùng muốn | Đường | Kiểu |
|---|---|---|
| Video giải thích ngắn (Shorts, Reels, 16:9) từ một đề bài | `tools/video_job.py` (estimate → submit → status → result) | **job**: một lệnh, tự lồng tiếng, minh họa, phụ đề, dựng, QC |
| Bài đăng / video cho doanh nghiệp nhỏ có "kit" ảnh và màu thương hiệu | `video_job.py` với `"kit"` (`kits/README.md`) | job |
| Video demo / release notes của app có mã nguồn | template `ds-release-notes` + skill `synthetic-ui-demo` | session |
| Demo app không có mã nguồn | quay bằng Playwright → `product-demo` | session |
| Video ra mắt / marketing, sprint review | `templates/product-demo`, `templates/sprint-review` | session |
| Câu chuyện số liệu (biểu đồ hiện theo lời) | `lib/components/DataChart.tsx` (Remotion) hoặc Matplotlib + moviepy | session |
| Quảng cáo < 30 s, brand stinger | moviepy (`.claude/skills/moviepy/`) | session |
| Người dẫn nói trước camera (AI) | `soulx.py` + `NarratorPiP` | tool |
| Sửa video có sẵn: lồng tiếng lại, thêm nhạc, cắt dọc, highlight, phụ đề, bỏ watermark | `redub.py`, `addmusic.py`, `cutdown.py`, `highlights.py`, `captions.py --srt`, `dewatermark.py` | tool |
| Nhân vật / sản phẩm 3D | Blender (`tools/blender_render.py doctor` trước; chỉ đề xuất nếu máy có Blender) | session |

"session" = sao chép template / example vào `projects/<tên>/`, sửa code theo skill tương ứng, render bằng Node, xem, sửa. Các skill con nằm ở `$VIDEO_TOOLKIT_ROOT/.claude/skills/<tên>/SKILL.md` (remotion, moviepy, ffmpeg, elevenlabs, playwright-recording, synthetic-ui-demo, video-design, parody-short, blender, ltx2, ideogram4, qwen-edit, acestep, runpod, youtube-stats); các lệnh `/video`, `/brand`, `/design`, `/redub`, `/thumbnail`… nằm ở `.claude/commands/<tên>.md` — đọc file và làm theo. "Bộ công cụ làm được gì": trả lời từ `uv run tools/video_job.py catalog`, không đoán.

## Tiền và key (bắt buộc)

- Mỗi job có ước tính chi phí: **chạy `estimate` và báo người dùng số tiền trước khi `submit`**, đặt giới hạn chi (cap) như hướng dẫn gốc; không tự tăng cap.
- Dịch vụ có thể dùng: GPU cloud (Modal / RunPod: `RUNPOD_API_KEY`), lưu trữ R2 (`*_ACCESS_KEY_ID`, `*_SECRET_ACCESS_KEY`), ElevenLabs (`ELEVENLABS_API_KEY`), tạo ảnh (Ideogram, FLUX…), YouTube API. Key nằm trong `$VIDEO_TOOLKIT_ROOT/.env` (người dùng tự điền từ `.env.example`) hoặc môi trường; **không bao giờ in, `cat`, hay dán key vào chat**. Key ElevenLabs đã lưu trong môi trường cloud này dùng được với `ELEVENLABS_API_KEY=proxy-injected`.
- Nhân bản giọng (`/voice-clone`), người dẫn AI, nhân vật 3D của người thật: chỉ với giọng / khuôn mặt của người dùng hoặc người đã đồng ý; không mạo danh người khác.

## Làm việc với người dùng

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Thuyết minh tiếng Việt: chọn giọng / provider hỗ trợ tiếng Việt (ElevenLabs đa ngôn ngữ hoặc giọng nhân bản của người dùng), nghe thử một cảnh trước khi làm cả video; ngân sách ~2,4 từ/giây (tiếng Việt nói nhanh hơn — đo lại sau cảnh đầu). Font chữ trên hình phải đủ dấu.
- Gửi lại các điểm duyệt mà skill gốc nêu (kịch bản, contact sheet, bản render) trước khi tiêu thêm tiền.
- Mỗi lần render ra file mới, không ghi đè.

## Kết hợp với các skill khác trong repo

`bien-tap` (cắt video nói trước camera, phụ đề sạch, nhạc nền), `video-youtube` (intro / outro / audiogram), `ho-tro-tao-video` (HyperFrames), `tao-do-hoa-chuyen-dong` và các skill iart-ai (đồ họa chuyển động), `ffmpeg-skill` (thao tác ffmpeg lẻ).

## Trạng thái kiểm tra (15/11/2026)

`scripts/cai-dat.sh` đã chạy thử: tải đúng commit `01e85f4`, `uv sync` thành công. Chưa chạy `verify_setup.py`, ví dụ `hello-world` hay một job thật trong phiên tạo skill (môi trường chặn chạy code vừa tải về) — lần đầu dùng, chạy `verify_setup.py` và `hello-world` để xác nhận trước khi làm video thật.
