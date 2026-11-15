---
name: animation-web
description: 'Animation cho website — animation cho web: cuộn trang với GSAP ScrollTrigger, SVG vẽ nét / morph, Lottie, chuyển trang, micro-interaction, hiệu ứng kính mờ, ASCII, tối ưu 60fps và tôn trọng prefers-reduced-motion. Workflows from iart-ai/web-animation-skills (60fps-animation, accessible-animation, ascii-animation, glassmorphism, gsap-web, lottie-animation, micro-interaction, page-transition-animation, svg-animation), each with a render-a-frame-and-check loop. Use for "animation web", "hiệu ứng website", "GSAP", "ScrollTrigger", "SVG animation", "Lottie", "chuyển trang", "hover", "/animation-web".'
---

# Animation cho website

> Nguồn: [iart-ai/web-animation-skills](https://github.com/iart-ai/web-animation-skills) (MIT, xem `LICENSE`), commit `ed3a045`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: animation cho web: cuộn trang với GSAP ScrollTrigger, SVG vẽ nét / morph, Lottie, chuyển trang, micro-interaction, hiệu ứng kính mờ, ASCII, tối ưu 60fps và tôn trọng prefers-reduced-motion.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `60fps-animation` | `goc/skills/60fps-animation/SKILL.md` | sửa animation giật: chỉ animate transform/opacity, tránh layout thrashing |
| `accessible-animation` | `goc/skills/accessible-animation/SKILL.md` | tôn trọng prefers-reduced-motion, tránh gây chóng mặt |
| `ascii-animation` | `goc/skills/ascii-animation/SKILL.md` | ASCII: intro / loader terminal, ảnh/video thành ASCII, shader ASCII |
| `glassmorphism` | `goc/skills/glassmorphism/SKILL.md` | kính mờ / liquid glass: card, thanh menu, modal |
| `gsap-web` | `goc/skills/gsap-web/SKILL.md` | GSAP + ScrollTrigger: ghim section, scrub theo cuộn, hero timeline, cuộn ngang |
| `lottie-animation` | `goc/skills/lottie-animation/SKILL.md` | Lottie (.json / .lottie) trên web / mobile, điều khiển đoạn phát |
| `micro-interaction` | `goc/skills/micro-interaction/SKILL.md` | hover, nhấn, toggle, nút like, toast, drawer, modal, sắp xếp danh sách |
| `page-transition-animation` | `goc/skills/page-transition-animation/SKILL.md` | chuyển trang / route (View Transitions API, Next.js, AnimatePresence) |
| `svg-animation` | `goc/skills/svg-animation/SKILL.md` | SVG: nét tự vẽ, chữ ký, morph hình, chạy theo đường, icon / logo động |

## Điều kiện chạy

- **Trình duyệt / HTML**: cần Node.js 22+; skill có khung render bằng Playwright + ffmpeg khi cần xuất video (Chromium có sẵn trong container cloud).
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Đây là code cho website của người dùng: sửa trong codebase của họ, chạy thử trên trình duyệt (Playwright) và chụp ảnh để kiểm tra trước khi báo xong.
- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
