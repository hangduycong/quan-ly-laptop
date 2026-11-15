---
name: video-tin-nhan
description: 'Video kể chuyện bằng tin nhắn — video hội thoại tin nhắn kiểu iMessage / WhatsApp / Messenger: bong bóng chat, dấu đang gõ, âm báo, kể chuyện bằng tin nhắn. Workflows from iart-ai/text-message-video-skills (text-message-animation), each with a render-a-frame-and-check loop. Use for "video tin nhắn", "video chat", "câu chuyện tin nhắn", "iMessage", "Zalo / Messenger style", "/video-tin-nhan".'
---

# Video kể chuyện bằng tin nhắn

> Nguồn: [iart-ai/text-message-video-skills](https://github.com/iart-ai/text-message-video-skills) (MIT, xem `LICENSE`), commit `10ae6bb`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: video hội thoại tin nhắn kiểu iMessage / WhatsApp / Messenger: bong bóng chat, dấu đang gõ, âm báo, kể chuyện bằng tin nhắn.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `text-message-animation` | `goc/skills/text-message-animation/SKILL.md` | hoạt cảnh cuộc trò chuyện: bong bóng, dấu đang gõ, nhịp đọc, âm báo |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Nội dung là hư cấu do người dùng viết: không dựng tin nhắn giả mạo người thật hay tổ chức thật để lừa người xem; nếu cần, ghi rõ "truyện hư cấu".
- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
