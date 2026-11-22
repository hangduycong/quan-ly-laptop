---
name: b3-video-tiktok
description: 'Video TikTok / Reels / Shorts — video dọc ngắn cho TikTok, Reels, YouTube Shorts: móc câu 1–3 giây đầu, nhịp giữ chân người xem, phụ đề nhảy theo từ (karaoke), đếm ngược, lower third. Workflows from iart-ai/tiktok-video-skills (caption-animation, countdown-video, lower-thirds, short-form-video), each with a render-a-frame-and-check loop. Use for "video TikTok", "Reels", "Shorts", "video dọc", "phụ đề karaoke", "phụ đề nhảy chữ", "đếm ngược", "/b3-video-tiktok".'
---

# Video TikTok / Reels / Shorts

> Nguồn: [iart-ai/tiktok-video-skills](https://github.com/iart-ai/tiktok-video-skills) (MIT, xem `LICENSE`), commit `88e7152`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: video dọc ngắn cho TikTok, Reels, YouTube Shorts: móc câu 1–3 giây đầu, nhịp giữ chân người xem, phụ đề nhảy theo từ (karaoke), đếm ngược, lower third.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `caption-animation` | `goc/skills/caption-animation/SKILL.md` | phụ đề động theo từng từ (karaoke, tô sáng từ đang nói), đốt phụ đề vào video |
| `countdown-video` | `goc/skills/countdown-video/SKILL.md` | video đếm ngược (mm:ss, ngày:giờ:phút:giây) cho livestream, sự kiện, sale |
| `lower-thirds` | `goc/skills/lower-thirds/SKILL.md` | lower third: tên, chức danh người nói, tiêu đề kiểu truyền hình |
| `short-form-video` | `goc/skills/short-form-video/SKILL.md` | video dọc ngắn: hook, nhịp cắt giữ chân, pattern interrupt, vòng lặp, vùng an toàn 9:16 |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.

- Skill liên quan trong repo: `b4-bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `b5-video-youtube` (intro / outro / audiogram), `b3-tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `b4-ffmpeg-skill` (thao tác ffmpeg lẻ).
