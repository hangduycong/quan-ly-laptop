---
name: b3-tao-do-hoa-chuyen-dong
description: Tạo đồ họa chuyển động — 56 motion-graphics workflows (19 packs from iart-ai) - TikTok/Reels/Shorts, captions, countdowns, lower thirds, text-message stories, YouTube intros, e-commerce and product videos, ads and launch films, animated charts and infographics, explainers and whiteboard, Vox-style map animation, web animation (GSAP, SVG, Lottie, scroll), logo and brand motion, kinetic typography, Three.js/WebGL/shaders, Manim math, generative illustration, canvas animation, transparent overlays, b-roll for talking heads, AI talking-head films; rendered with Remotion, Manim, HTML or canvas and checked frame by frame. Use for "đồ họa chuyển động", "motion graphics", "animation", "video hoạt hình", "chữ chuyển động", "biểu đồ động", "/b3-tao-do-hoa-chuyen-dong".
---

# Tạo đồ họa chuyển động

> Nguồn: 19 gói skill của [iart-ai](https://github.com/iart-ai/motion-skills) (giấy phép MIT, xem `LICENSE`; gói `generative-illustration-skills` không có file LICENSE riêng, được tính theo tuyên bố "56 skill, MIT" của repo `motion-skills`). Lấy ngày 15/11/2026. Mỗi gói giữ nguyên trong `goi/<gói>/` (chỉ bỏ ảnh/video demo để nhẹ); file này và `MUC-LUC.md` là phần viết thêm.

## Cách dùng

1. Chọn skill theo bảng dưới (hoặc tra đủ 56 skill trong `MUC-LUC.md`).
2. **Đọc `goi/<gói>/skills/<skill>/SKILL.md` và làm theo đúng file đó.** Mọi đường dẫn trong file (`references/…`, `../<skill khác>/…`, `scripts/…`) tính từ thư mục của chính file đó; `scripts/` chung của gói nằm ở `goi/<gói>/scripts/` (probe MP4, chụp một khung, contact sheet).
3. Luôn làm theo vòng **làm → render một khung → xem ảnh → sửa** mà các skill mô tả, trước khi render cả video. Mở ảnh bằng Read và tự xem.

| Người dùng muốn | Gói → skill |
|---|---|
| Video dọc TikTok / Reels / Shorts, phụ đề nhảy theo từ, đếm ngược | `tiktok-video-skills` → `short-form-video`, `caption-animation`, `countdown-video`, `lower-thirds` |
| Video kể chuyện bằng tin nhắn | `text-message-video-skills` → `text-message-animation` |
| Intro / outro YouTube, podcast | `youtube-video-skills` → `youtube-intro-outro`, `audiogram` |
| Video sản phẩm, bán hàng | `ecommerce-video-skills` → `product-demo-video`, `promo-video`, `photo-slideshow` |
| Quảng cáo, video ra mắt, testimonial | `ad-video-skills` → `ad-creative-video`, `launch-video`, `testimonial-video` |
| Biểu đồ động từ CSV, infographic, slide thành video | `data-animation-skills` → `chart-animation`, `animated-infographic`, `presentation-video` |
| Video giải thích, bài giảng, whiteboard | `explainer-video-skills` → `explainer-video`, `whiteboard-animation`, `diagram-animation`, `isometric-animation`, `wrapped-video` |
| Bản đồ động kiểu Vox | `map-animation-skills` → `map-animation` |
| Animation cho website (GSAP, SVG, Lottie, scroll, micro-interaction) | `web-animation-skills` → `gsap-web`, `svg-animation`, `lottie-animation`, `page-transition-animation`, `micro-interaction`, `60fps-animation`, `accessible-animation`, `glassmorphism`, `ascii-animation` |
| Logo động, brand motion, hệ thống chuyển động | `motion-design-skills` → `logo-animation`, `remotion-video`, `animation-principles`, `motion-art-direction`, `color-motion`, `shot-composition`, `beat-sync-editing`, `motion-background`, `after-effects` |
| Chữ chuyển động (kinetic typography), title, lyric | `kinetic-typography-skills` → `kinetic-typography` |
| Làm cho khách hàng: brief, báo giá, sửa theo góp ý, brand guideline, thông số bàn giao | `freelance-motion-skills` → `creative-brief`, `motion-pricing`, `client-revisions`, `brand-motion-guidelines`, `video-delivery-specs` |
| 3D, Three.js, WebGL, shader | `webgl-animation-skills` → `threejs-animation`, `shader-glsl`, `particle-system` |
| Toán / vật lý / tin học bằng Manim | `manim-skills` → `manim` |
| Minh họa AI ghép và chuyển động | `generative-illustration-skills` → `generative-illustration` |
| Phim vẽ hoàn toàn bằng JavaScript (canvas) + nhạc tạo bằng code | `javascript-animation-skills` → `javascript-animation`, `soundtrack` |
| Lower third trong suốt cho OBS / Premiere / Resolve | `lower-thirds-skills` → `lower-thirds` |
| B-roll đồ họa chèn vào video nói trước camera | `b-roll-skills` → `talking-head-b-roll` |
| Tạo video người nói từ ảnh + giọng | `talking-head-skills` → `talking-head` |

## Điều kiện chạy

- Phần lớn render bằng **Remotion** hoặc HTML + Playwright/Chromium, nên cần **Node.js 22+** và **ffmpeg**; Manim cần Python + Manim CE (+ LaTeX cho công thức). Cài gói từ npm/pip: **hỏi người dùng trước**.
- Một số skill gọi dịch vụ AI tính phí: ElevenLabs (giọng đọc, chuyển giọng nói thành chữ), fal.ai (`FAL_KEY`, tạo ảnh/video), OpenRouter, Replicate, Gemini. **Không tự dùng dịch vụ trả phí khi người dùng chưa đồng ý**; nhiều skill có đường miễn phí (tự đưa ảnh/nhạc, không lồng tiếng). Key lưu trong môi trường hoặc file `.env` của người dùng, không bao giờ in ra hay dán vào chat. Key ElevenLabs đã lưu cho môi trường này dùng được với placeholder `ELEVENLABS_API_KEY=proxy-injected`.
- Các README có nhắc dịch vụ trả phí iart.ai / iArt MCP: chỉ là quảng cáo của tác giả, không cần cho skill chạy; chỉ nhắc tới nếu người dùng hỏi.

## Làm việc với người dùng

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: chọn font có đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Ý tưởng còn mơ hồ: đề xuất (storyboard ngắn, thời lượng, khung hình) trước khi dựng.
- Mỗi lần render ra file mới, không ghi đè.

## Kết hợp với các skill khác trong repo

- Cắt video nói trước camera trước (`b4-bien-tap`), rồi thêm b-roll / lower third / caption bằng skill ở đây; ghép overlay trong suốt bằng `b4-bien-tap` `export.py --overlays`.
- Dự án HTML → video kiểu HyperFrames: `b3-ho-tro-tao-video`. Thao tác ffmpeg lẻ: `b4-ffmpeg-skill`.
