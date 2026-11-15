---
name: minh-hoa-ai-chuyen-dong
description: 'Minh họa AI chuyển động — minh họa chuyển động: tạo nhiều mảnh minh họa nhỏ bằng AI, tách nền, ghép thành sprite rồi animate từng mảnh bằng code — tác phẩm thơ, giàu ý niệm. Workflows from iart-ai/generative-illustration-skills (generative-illustration), each with a render-a-frame-and-check loop. Use for "minh họa động", "tranh động", "animate minh họa AI", "generative motion", "/minh-hoa-ai-chuyen-dong".'
---

# Minh họa AI chuyển động

> Nguồn: [iart-ai/generative-illustration-skills](https://github.com/iart-ai/generative-illustration-skills) (MIT (repo không có file LICENSE riêng; repo mục lục `iart-ai/motion-skills` ghi toàn bộ skill là MIT — `LICENSE` ở đây lấy từ đó)), commit `e7d6243`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: minh họa chuyển động: tạo nhiều mảnh minh họa nhỏ bằng AI, tách nền, ghép thành sprite rồi animate từng mảnh bằng code — tác phẩm thơ, giàu ý niệm.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `generative-illustration` | `goc/skills/generative-illustration/SKILL.md` | tạo asset minh họa bằng AI, tách nền, ghép sprite, render khung chính xác |

## Điều kiện chạy

- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Dịch vụ / key mà một số bước dùng: `GEMINI_KEY`, `OPENROUTER_API_KEY`, `REPLICATE_API_KEY`. Đều tính phí: hỏi người dùng trước, có đường thay thế miễn phí thì đề xuất. Key không bao giờ in ra hay dán vào chat; lưu trong môi trường hoặc qua form key an toàn.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Tạo ảnh bằng AI tốn phí (OpenRouter, Replicate, Gemini): hỏi trước; có thể dùng ảnh người dùng tự đưa. Không tạo ảnh bắt chước phong cách hay nhân vật có bản quyền của người khác.
- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
