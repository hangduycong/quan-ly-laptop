---
name: ho-tro-tao-video
description: Hỗ trợ tạo video — make, edit, animate or render videos from HTML with HyperFrames (HTML/CSS/GSAP rendered frame by frame to deterministic MP4) - launch and promo films, explainers, tutorials, music videos, charts and data, maps, vertical/social clips, title cards, kinetic type, captions, overlays, 3D, slideshows; remaking a video, porting Remotion/Lottie/Three.js, bringing in Figma; getting music, SFX, voiceover, images. Use for "tạo video", "làm video", "hỗ trợ tạo video", "/ho-tro-tao-video", "make a video", "motion graphics", "animated explainer", or any HyperFrames project.
---

# Hỗ trợ tạo video (HyperFrames)

> Nguồn: [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) (Apache License 2.0, xem `LICENSE`), commit `04ee926` (14/11/2026). 9 skill đã phát hành được giữ nguyên trong `goc/`; file này là cửa vào tiếng Việt. Cập nhật bản gốc: chép lại thư mục `skills/` của repo vào `goc/`.

HyperFrames biến HTML, CSS, media và animation có thể tua (GSAP, Lottie, Three.js, canvas…) thành video MP4 giống hệt nhau mỗi lần render. Công cụ chạy bằng CLI `npx hyperframes <lệnh>`.

## Bắt buộc trước khi làm

1. **Đọc `goc/hyperframes/SKILL.md`** — render contract, vòng làm việc, bảng "What to read" theo loại video. Mọi đường dẫn `references/...` trong file đó tính từ `goc/hyperframes/`.
2. Khi một file nhắc skill khác bằng `/tên`, đọc `goc/<tên>/SKILL.md`:

| Được nhắc | Đọc | Dùng khi |
|---|---|---|
| `/hyperframes` | `goc/hyperframes/SKILL.md` | luôn đọc đầu tiên |
| `/hyperframes-cli` | `goc/hyperframes-cli/SKILL.md` | init, check, timeline, preview, render, history, xử lý lỗi CLI |
| `/hyperframes-registry` | `goc/hyperframes-registry/SKILL.md` | ~450 block dựng sẵn (transition, title, caption, chart, map, 3D…) — tìm ở đây trước khi tự viết hiệu ứng |
| `/media-use` | `goc/media-use/SKILL.md` | nhạc, SFX, ảnh, icon, logo, giọng đọc, avatar, transcript, tách nền, chỉnh màu |
| `/reverse-any-video` | `goc/reverse-any-video/SKILL.md` | dựng lại một video có sẵn thành project chỉnh được |
| `/style-sampling` | `goc/style-sampling/SKILL.md` | làm một tập mới theo phong cách đã có |
| `/slideshow` | `goc/slideshow/SKILL.md` | bài trình chiếu (deck) thay vì video |
| `/remotion-to-hyperframes` | `goc/remotion-to-hyperframes/SKILL.md` | chuyển code Remotion / Motion Canvas / Lottie / Three.js… sang |
| `/figma` | `goc/figma/SKILL.md` | dùng thiết kế Figma (cần Figma MCP) |

## Điều kiện chạy

- **Node.js 22+** và `npx`. Lần đầu, `npx hyperframes` tải CLI từ npm: **hỏi người dùng trước khi cài**.
- Trình duyệt Chrome/Chromium (CLI dùng để chụp từng khung hình) và ffmpeg.
- Tài khoản HeyGen **không bắt buộc**: `/media-use` nói rõ cái gì miễn phí, cái gì cần HeyGen (gói Pro có trả phí). Không tự đăng ký hay dùng dịch vụ trả phí khi người dùng chưa đồng ý.
- Dòng "Usage beacon" (`npx hyperframes events …`) trong `goc/hyperframes/SKILL.md` gửi dữ liệu sử dụng (telemetry) cho HeyGen: **bỏ qua** trừ khi người dùng đồng ý. CLI cũng tự thu thập dữ liệu sử dụng: lần đầu chạy trên máy, tắt bằng `npx hyperframes telemetry disable`.
- Đã thử (CLI 0.9.52, Node 22): `init` → `check --json` (0 lỗi) → `render` ra MP4 1920×1080 5 giây trong ~7 giây. Không có `chrome-headless-shell` thì CLI dùng Chrome hệ thống ở chế độ chụp màn hình (chậm hơn, vẫn đúng).

## Cách làm việc với người dùng

- Người dùng nói tiếng Việt: trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ trên video theo ngôn ngữ người dùng muốn; font tiếng Việt: dùng tên font có sẵn (Montserrat, Inter, Roboto, Open Sans, Lato, Poppins…), trình biên dịch tự tải bộ ký tự tiếng Việt từ Google Fonts nên dấu hiển thị đúng; font khác cần `@font-face` tới file trong `assets/fonts/`. Luôn xem snapshot để chắc dấu không bị lỗi.
- Làm đúng thứ được yêu cầu (không tự thêm giọng đọc, phụ đề, đổi khung hình). Ý tưởng còn mơ hồ: đề xuất trước, chưa sửa.
- Phim > ~15 giây có kể chuyện: đưa 3 hướng câu chuyện bằng lời (`references/story.md`) để người dùng chọn, rồi mới viết `SPEC.md`.
- Trước khi giao: `npx hyperframes check --json`, sửa hết lỗi; phim thì `snapshot --review` và xem ảnh. Chỉ render bản cuối khi người dùng duyệt preview, hoặc xin file, hoặc bảo "làm hết đừng hỏi".
- Mỗi lần render ra file mới, không ghi đè bản trước.

## Kết hợp với các skill khác trong repo này

- Video nói trước camera / vlog cần cắt bỏ đoạn hỏng, khoảng lặng: dùng `bien-tap` (hoặc `chinh-sua-video`) để dựng phần cắt; dùng skill này cho đồ họa, title, chart, intro/outro.
- Overlay có nền trong suốt render bằng HyperFrames có thể ghép vào bản dựng của `bien-tap` bằng `export.py --overlays`.
- Thao tác ffmpeg đơn lẻ (cắt nhanh, đổi khung, chuẩn hóa âm lượng, kiểm tra chuẩn nền tảng): `ffmpeg-skill`.
