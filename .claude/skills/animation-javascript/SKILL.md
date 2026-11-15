---
name: animation-javascript
description: 'Phim hoạt hình vẽ bằng JavaScript — phim hoạt hình vẽ từng khung bằng JavaScript trên canvas, không cần ảnh có sẵn, kèm nhạc nền tổng hợp bằng code khớp với nhịp cắt. Workflows from iart-ai/javascript-animation-skills (javascript-animation, soundtrack), each with a render-a-frame-and-check loop. Use for "vẽ bằng code", "canvas animation", "phim hoạt hình JavaScript", "nhạc tạo bằng code", "/animation-javascript".'
---

# Phim hoạt hình vẽ bằng JavaScript

> Nguồn: [iart-ai/javascript-animation-skills](https://github.com/iart-ai/javascript-animation-skills) (MIT, xem `LICENSE`), commit `060f746`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: phim hoạt hình vẽ từng khung bằng JavaScript trên canvas, không cần ảnh có sẵn, kèm nhạc nền tổng hợp bằng code khớp với nhịp cắt.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `javascript-animation` | `goc/skills/javascript-animation/SKILL.md` | vẽ mọi khung hình bằng JavaScript (canvas), phong cách vẽ tay, xuất video |
| `soundtrack` | `goc/skills/soundtrack/SKILL.md` | soạn nhạc nền bằng code khớp nhịp cắt, kiểm tra âm lượng, ghép vào video |

## Điều kiện chạy

- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Dịch vụ / key mà một số bước dùng: `OPENROUTER_API_KEY`. Đều tính phí: hỏi người dùng trước, có đường thay thế miễn phí thì đề xuất. Key không bao giờ in ra hay dán vào chat; lưu trong môi trường hoặc qua form key an toàn.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.

- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
