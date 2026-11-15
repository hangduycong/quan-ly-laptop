---
name: video-nguoi-noi-ai
description: 'Video người nói bằng AI — tạo video người nói bằng AI từ ảnh của chính người dùng + mẫu giọng (hoặc từ video họ tự quay), dùng giọng ElevenLabs được phép và kịch bản mới, rồi ghép với thuyết minh và đồ họa. Workflows from iart-ai/talking-head-skills (talking-head), each with a render-a-frame-and-check loop. Use for "video người nói AI", "avatar AI", "talking head AI", "nhân bản giọng", "/video-nguoi-noi-ai".'
---

# Video người nói bằng AI

> Nguồn: [iart-ai/talking-head-skills](https://github.com/iart-ai/talking-head-skills) (MIT, xem `LICENSE`), commit `eac1f6b`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: tạo video người nói bằng AI từ ảnh của chính người dùng + mẫu giọng (hoặc từ video họ tự quay), dùng giọng ElevenLabs được phép và kịch bản mới, rồi ghép với thuyết minh và đồ họa.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `talking-head` | `goc/skills/talking-head/SKILL.md` | ảnh + giọng → video người nói (ElevenLabs + fal.ai), ghép thuyết minh và đồ họa |

## Điều kiện chạy

- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Dịch vụ / key mà một số bước dùng: `ELEVENLABS_API_KEY`, `FAL_API_KEY`, `FAL_KEY`. Đều tính phí: hỏi người dùng trước, có đường thay thế miễn phí thì đề xuất. Key không bao giờ in ra hay dán vào chat; lưu trong môi trường hoặc qua form key an toàn.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- **Chỉ dùng khuôn mặt và giọng của chính người dùng, hoặc của người đã đồng ý rõ ràng.** Không tạo video giả người thật khác (người nổi tiếng, chính trị gia, đồng nghiệp…), không dùng để lừa đảo hay mạo danh.
- Dịch vụ tính phí: ElevenLabs (nhân bản giọng, đọc kịch bản) và fal.ai (`FAL_KEY`, tạo video). Hỏi trước; key ElevenLabs đã lưu dùng được với `ELEVENLABS_API_KEY=proxy-injected`; `FAL_KEY` cần người dùng lưu qua form key an toàn.
- Nên ghi chú "video tạo bằng AI" khi đăng.
- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
