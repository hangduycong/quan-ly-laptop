---
name: b3-bieu-do-dong
description: 'Biểu đồ và dữ liệu động — biểu đồ động từ dữ liệu: bar chart race, CSV thành video, số đếm tăng dần, infographic động, chuyển slide / pitch deck thành video có thuyết minh. Workflows from iart-ai/data-animation-skills (animated-infographic, chart-animation, presentation-video), each with a render-a-frame-and-check loop. Use for "biểu đồ động", "bar chart race", "CSV thành video", "infographic động", "slide thành video", "/b3-bieu-do-dong".'
---

# Biểu đồ và dữ liệu động

> Nguồn: [iart-ai/data-animation-skills](https://github.com/iart-ai/data-animation-skills) (MIT, xem `LICENSE`), commit `6570c0c`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: biểu đồ động từ dữ liệu: bar chart race, CSV thành video, số đếm tăng dần, infographic động, chuyển slide / pitch deck thành video có thuyết minh.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `animated-infographic` | `goc/skills/animated-infographic/SKILL.md` | infographic động: icon và số liệu xuất hiện theo trình tự |
| `chart-animation` | `goc/skills/chart-animation/SKILL.md` | biểu đồ động từ CSV / số liệu: bar chart race, đường, cột, số đếm |
| `presentation-video` | `goc/skills/presentation-video/SKILL.md` | pitch deck / slide thành video, có thể kèm thuyết minh |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Số liệu lấy đúng từ file người dùng; không làm tròn hay bịa số. Ghi nguồn dữ liệu trên khung hình nếu người dùng có.
- Skill liên quan trong repo: `b4-bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `b5-video-youtube` (intro / outro / audiogram), `b3-tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `b4-ffmpeg-skill` (thao tác ffmpeg lẻ).
