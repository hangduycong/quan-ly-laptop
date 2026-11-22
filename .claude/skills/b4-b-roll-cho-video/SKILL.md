---
name: b4-b-roll-cho-video
description: 'B-roll đồ họa cho video nói trước camera — thêm b-roll đồ họa vào video nói trước camera: chuyển giọng nói thành chữ có mốc từng từ, quyết định từng câu khi nào thấy người nói, khi nào phủ đồ họa, khi nào đồ họa toàn khung, vẽ đồ họa theo đúng lời nói rồi ghép lại. Workflows from iart-ai/b-roll-skills (talking-head-b-roll), each with a render-a-frame-and-check loop. Use for "b-roll", "thêm đồ họa vào video", "video nói chuyện thêm hình minh họa", "/b4-b-roll-cho-video".'
---

# B-roll đồ họa cho video nói trước camera

> Nguồn: [iart-ai/b-roll-skills](https://github.com/iart-ai/b-roll-skills) (MIT, xem `LICENSE`), commit `bcd5674`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: thêm b-roll đồ họa vào video nói trước camera: chuyển giọng nói thành chữ có mốc từng từ, quyết định từng câu khi nào thấy người nói, khi nào phủ đồ họa, khi nào đồ họa toàn khung, vẽ đồ họa theo đúng lời nói rồi ghép lại.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `talking-head-b-roll` | `goc/skills/talking-head-b-roll/SKILL.md` | chuyển giọng nói thành chữ (ElevenLabs), lên kế hoạch từng câu, vẽ đồ họa, ghép vào video |

## Điều kiện chạy

- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Dịch vụ / key mà một số bước dùng: `ELEVENLABS_API_KEY`. Đều tính phí: hỏi người dùng trước, có đường thay thế miễn phí thì đề xuất. Key không bao giờ in ra hay dán vào chat; lưu trong môi trường hoặc qua form key an toàn.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Dùng key ElevenLabs đã lưu trong môi trường: đặt `ELEVENLABS_API_KEY=proxy-injected` khi chạy (proxy tự gắn key thật). Cắt video trước bằng `b4-bien-tap` nếu cần bỏ đoạn hỏng.
- Skill liên quan trong repo: `b4-bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `b5-video-youtube` (intro / outro / audiogram), `b3-tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `b4-ffmpeg-skill` (thao tác ffmpeg lẻ).
