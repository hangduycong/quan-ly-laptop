---
name: b4-lower-third
description: 'Lower third và overlay trong suốt — lower third và overlay truyền hình (thanh tên, logo góc, nhắc đăng ký, tiêu đề bài hát / Kinh Thánh) dạng video nền trong suốt (WebM alpha, ProRes 4444) cho OBS, Premiere, DaVinci Resolve. Workflows from iart-ai/lower-thirds-skills (lower-thirds), each with a render-a-frame-and-check loop. Use for "lower third", "thanh tên", "overlay trong suốt", "nhắc đăng ký", "OBS overlay", "/b4-lower-third".'
---

# Lower third và overlay trong suốt

> Nguồn: [iart-ai/lower-thirds-skills](https://github.com/iart-ai/lower-thirds-skills) (MIT, xem `LICENSE`), commit `58d3623`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: lower third và overlay truyền hình (thanh tên, logo góc, nhắc đăng ký, tiêu đề bài hát / Kinh Thánh) dạng video nền trong suốt (WebM alpha, ProRes 4444) cho OBS, Premiere, DaVinci Resolve.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `lower-thirds` | `goc/skills/lower-thirds/SKILL.md` | vẽ từng khung trên canvas, render WebM có kênh alpha / ProRes 4444 |

## Điều kiện chạy

- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Đã chạy thử (15/11/2026)

Trong thư mục làm việc: copy `goc/skills/lower-thirds/templates/b4-lower-third.html` thành `page.html`, sửa `CARDS`, `npm i playwright-core`, rồi `node <skill>/goc/skills/lower-thirds/scripts/render.mjs page.html --check` → ✓ (trong suốt, đầu/cuối trống, trong vùng title-safe); `… shot --stills 3s` → ảnh trên nền ô vuông / tối / sáng; `… an.webm` → WebM VP9 có alpha 237 khung, 1920×1080 @30. Tên tiếng Việt ("Nguyễn Văn An", "Chuyên gia sửa laptop") hiển thị đủ dấu.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Ghép overlay trong suốt vào bản dựng của skill `b4-bien-tap`: `export.py --overlays` (ProRes 4444 / WebM alpha).
- Skill liên quan trong repo: `b4-bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `b5-video-youtube` (intro / outro / audiogram), `b3-tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `b4-ffmpeg-skill` (thao tác ffmpeg lẻ).
