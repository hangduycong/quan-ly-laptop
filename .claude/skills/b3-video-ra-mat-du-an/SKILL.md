---
name: b3-video-ra-mat-du-an
description: 'Video ra mắt dự án — brag: turns the current project (reads the code directly, no live URL or screenshots needed) or a website URL into a short, polished, shareable launch video with motion, music, sound effects and share copy, built with HyperFrames; brag-slim builds everything with tools already on the machine. Use for "video ra mắt", "khoe dự án", "làm video giới thiệu sản phẩm từ code", "launch video", "/brag", "/brag-slim", "let''s brag about this", "/b3-video-ra-mat-du-an".'
---

# Video ra mắt dự án (brag)

> Nguồn: [latent-spaces/brag](https://github.com/latent-spaces/brag) (MIT, `LICENSE`, © 2026 Shunit Haviv Hakimi), commit `669ab92`. Bản gốc trong `goc/brag/` và `goc/brag-slim/` (bỏ `docs/`, `examples/` ~47 MB, plugin manifest). File này là phần viết thêm.

Đọc code của dự án (trang web, app) → lên kế hoạch → dựng video ra mắt ngắn bằng HyperFrames (chuyển động, nhạc, hiệu ứng âm thanh) → kèm lời chia sẻ để đăng.

## Cách chạy

1. Chọn bản:
   - **`goc/brag/SKILL.md`** — bản đầy đủ: có nhạc / SFX đi kèm, đồng bộ nhịp, tùy chọn lồng tiếng (`--voice`).
   - **`goc/brag-slim/SKILL.md`** — một file, không asset đi kèm, model tự dựng hết. Bản đầy đủ tự chuyển sang slim với một số model (dòng "Model check" đầu file gốc).
2. `<skill-dir>` trong file gốc = thư mục `goc/brag/` của skill này (asset ở `goc/brag/assets/`, script ở `goc/brag/scripts/`).
3. **Skill HyperFrames** mà brag yêu cầu đọc (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`) đã có trong repo: `.claude/skills/b3-ho-tro-tao-video/goc/<tên>/SKILL.md`. Cần Node.js 22+, Chrome/Chromium, ffmpeg; `npx hyperframes` tải CLI từ npm (hỏi người dùng lần đầu) và nên tắt telemetry: `npx hyperframes telemetry disable`.
4. Video và file làm việc ghi vào thư mục đầu ra của người dùng, không vào thư mục skill.

## Bản quyền âm thanh (bắt buộc)

- **Nhạc** (`goc/brag/assets/music/`): "Happy Beats / Business Moves" của **Sascha Ende** (ende.app), giấy phép **CC BY 4.0** — **video dùng nhạc này phải ghi công**: `Music: Sascha Ende, ende.app (CC BY 4.0)` (trong mô tả / lời chia sẻ). Nhắc người dùng khi giao video.
- **SFX**: Kenney.nl và bộ phím của unicae_games — CC0, không cần ghi công.
- Không dùng nhạc khác khi người dùng chưa xác nhận có quyền.

## Tiếng Việt

- Kế hoạch, lời chia sẻ, báo cáo: tiếng Việt (trừ khi người dùng muốn đăng bằng tiếng Anh).
- Chữ trên video: font có dấu tiếng Việt (Montserrat, Inter, Roboto…); xem snapshot để chắc dấu đúng.

## Liên quan

`b3-ho-tro-tao-video` (HyperFrames nói chung), `b3-video-quang-cao` (`launch-video`), `b5-video-youtube` (intro / outro).

## Trạng thái kiểm tra (15/11/2026)

Frontmatter và liên kết đã kiểm tra; HyperFrames CLI 0.9.52 đã render được trong repo này (skill `b3-ho-tro-tao-video`). **Chưa chạy thử** trọn quy trình brag.
