---
name: b3-video-toan-hoc-manim
description: 'Video toán học bằng Manim — video toán / vật lý / tin học kiểu 3Blue1Brown bằng Manim: biến đổi phương trình LaTeX, đồ thị hàm số, ValueTracker, 3D và camera chuyển động. Workflows from iart-ai/manim-skills (manim), each with a render-a-frame-and-check loop. Use for "video toán", "Manim", "3Blue1Brown", "animate phương trình", "đồ thị động", "/b3-video-toan-hoc-manim".'
---

# Video toán học bằng Manim

> Nguồn: [iart-ai/manim-skills](https://github.com/iart-ai/manim-skills) (MIT, xem `LICENSE`), commit `3e989cb`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: video toán / vật lý / tin học kiểu 3Blue1Brown bằng Manim: biến đổi phương trình LaTeX, đồ thị hàm số, ValueTracker, 3D và camera chuyển động.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `manim` | `goc/skills/manim/SKILL.md` | Manim CE: Scene, Mobject, MathTex, đồ thị, updater, 3D, render MP4/GIF |

## Điều kiện chạy

- **Manim Community** (Python): `pip install manim` + ffmpeg; công thức LaTeX cần TeX (`texlive`); trên Linux có thể cần `libcairo2-dev libpango1.0-dev`.
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Chữ tiếng Việt trong Manim: dùng `Text(..., font="Be Vietnam Pro")` (hoặc font hệ thống đủ dấu) thay vì `Tex`; công thức vẫn dùng `MathTex`.
- Skill liên quan trong repo: `b4-bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `b5-video-youtube` (intro / outro / audiogram), `b3-tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `b4-ffmpeg-skill` (thao tác ffmpeg lẻ).
