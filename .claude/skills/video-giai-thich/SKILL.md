---
name: video-giai-thich
description: 'Video giải thích (explainer) — video giải thích: kịch bản + storyboard + thuyết minh + phụ đề, sơ đồ / flowchart hiện từng bước, isometric 2.5D, whiteboard vẽ tay, video tổng kết năm kiểu Spotify Wrapped. Workflows from iart-ai/explainer-video-skills (diagram-animation, explainer-video, isometric-animation, whiteboard-animation, wrapped-video), each with a render-a-frame-and-check loop. Use for "video giải thích", "explainer", "video hướng dẫn", "sơ đồ động", "whiteboard", "vẽ tay", "isometric", "tổng kết năm", "/video-giai-thich".'
---

# Video giải thích (explainer)

> Nguồn: [iart-ai/explainer-video-skills](https://github.com/iart-ai/explainer-video-skills) (MIT, xem `LICENSE`), commit `3c13a1b`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: video giải thích: kịch bản + storyboard + thuyết minh + phụ đề, sơ đồ / flowchart hiện từng bước, isometric 2.5D, whiteboard vẽ tay, video tổng kết năm kiểu Spotify Wrapped.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `diagram-animation` | `goc/skills/diagram-animation/SKILL.md` | sơ đồ / flowchart / kiến trúc hệ thống hiện ra từng bước |
| `explainer-video` | `goc/skills/explainer-video/SKILL.md` | video giải thích trọn gói: kịch bản, storyboard, thuyết minh, phụ đề đồng bộ |
| `isometric-animation` | `goc/skills/isometric-animation/SKILL.md` | cảnh isometric 2.5D, sơ đồ tách lớp, xếp tầng |
| `whiteboard-animation` | `goc/skills/whiteboard-animation/SKILL.md` | kiểu VideoScribe: nét vẽ tay hiện dần trên bảng trắng |
| `wrapped-video` | `goc/skills/wrapped-video/SKILL.md` | video tổng kết cá nhân hóa kiểu Spotify Wrapped / year in review |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.

- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
