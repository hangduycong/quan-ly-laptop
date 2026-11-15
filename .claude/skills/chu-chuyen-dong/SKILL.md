---
name: chu-chuyen-dong
description: 'Chữ chuyển động (kinetic typography) — chữ chuyển động: tách chữ/từ/dòng xuất hiện so le, hiệu ứng lộ chữ, font biến thiên, chữ chạy theo đường, video lời bài hát, title card. Workflows from iart-ai/kinetic-typography-skills (kinetic-typography), each with a render-a-frame-and-check loop. Use for "chữ chuyển động", "kinetic typography", "hiệu ứng chữ", "video lời bài hát", "title động", "/chu-chuyen-dong".'
---

# Chữ chuyển động (kinetic typography)

> Nguồn: [iart-ai/kinetic-typography-skills](https://github.com/iart-ai/kinetic-typography-skills) (MIT, xem `LICENSE`), commit `2b79c81`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: chữ chuyển động: tách chữ/từ/dòng xuất hiện so le, hiệu ứng lộ chữ, font biến thiên, chữ chạy theo đường, video lời bài hát, title card.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `kinetic-typography` | `goc/skills/kinetic-typography/SKILL.md` | chữ chuyển động bằng CSS, GSAP SplitText, Framer Motion hoặc Remotion |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Tiếng Việt: tách theo **từ** hoặc **dòng**; nếu tách theo ký tự, dùng `Intl.Segmenter` (grapheme) để không tách rời dấu khỏi chữ cái. Font đủ dấu: Be Vietnam Pro, Montserrat, Inter, Roboto.
- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
