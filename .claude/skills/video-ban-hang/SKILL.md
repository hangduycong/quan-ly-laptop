---
name: video-ban-hang
description: 'Video bán hàng / thương mại điện tử — video bán hàng: demo sản phẩm / ứng dụng, video khuyến mãi (giảm giá, giá cũ → giá mới gạch ngang, flash sale), slideshow ảnh có nhạc và hiệu ứng Ken Burns. Workflows from iart-ai/ecommerce-video-skills (photo-slideshow, product-demo-video, promo-video), each with a render-a-frame-and-check loop. Use for "video bán hàng", "video sản phẩm", "video khuyến mãi", "flash sale", "demo app", "slideshow ảnh", "/video-ban-hang".'
---

# Video bán hàng / thương mại điện tử

> Nguồn: [iart-ai/ecommerce-video-skills](https://github.com/iart-ai/ecommerce-video-skills) (MIT, xem `LICENSE`), commit `a430fbb`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: video bán hàng: demo sản phẩm / ứng dụng, video khuyến mãi (giảm giá, giá cũ → giá mới gạch ngang, flash sale), slideshow ảnh có nhạc và hiệu ứng Ken Burns.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `photo-slideshow` | `goc/skills/photo-slideshow/SKILL.md` | slideshow ảnh thành video: Ken Burns, chuyển cảnh, nhạc nền, video kỷ niệm |
| `product-demo-video` | `goc/skills/product-demo-video/SKILL.md` | video demo sản phẩm / app / SaaS từ ảnh chụp màn hình, giới thiệu tính năng |
| `promo-video` | `goc/skills/promo-video/SKILL.md` | video khuyến mãi: % giảm, giá cũ → giá mới, đếm ngược flash sale, Black Friday |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.

- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
