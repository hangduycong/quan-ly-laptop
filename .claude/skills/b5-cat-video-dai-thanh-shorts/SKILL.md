---
name: b5-cat-video-dai-thanh-shorts
description: 'Cắt video dài thành Shorts — interactive long-form to short-form clip maker (claude-shorts): transcribes a long video with faster-whisper, Claude scores and presents the most viral-ready moments, the user picks and adjusts, boundaries snap to sentences, face-aware 9:16 reframing, Remotion renders animated captions (Bold / Bounce / Clean) and hook overlay, FFmpeg exports for YouTube Shorts, TikTok and Instagram Reels. Use for "cắt shorts", "cắt video dài thành clip ngắn", "làm Reels / TikTok từ video", "video dọc từ podcast", "shorts", "extract clips", "/b5-cat-video-dai-thanh-shorts".'
---

# Cắt video dài thành Shorts

> Nguồn: [AgriciDaniel/claude-shorts](https://github.com/AgriciDaniel/claude-shorts) (MIT, `LICENSE`, © 2026 Daniel Agrici), commit `a369fad`. Bản gốc trong `goc/` (bỏ `.github/`, plugin manifest, script cài vào `~/.claude`, ảnh header). File này là phần viết thêm.

Lấy một video dài (podcast, livestream, bài giảng, vlog) → tìm các đoạn đáng làm Shorts → người dùng chọn → render clip dọc 9:16 có phụ đề động → xuất đúng chuẩn từng nền tảng.

## Cách chạy

1. **Đọc `goc/SKILL.md`** và làm theo quy trình 10 bước của nó (pre-flight → chuyển giọng nói thành chữ → chấm điểm đoạn → người dùng chọn → snap ranh giới → reframe → render Remotion → export → validate).
2. **Đặt `SHORTS_ROOT` đúng thư mục `goc/` của skill này** thay cho vòng lặp dò thư mục trong bước Pre-Flight (skill không cài ở `~/.claude/skills/shorts`):
   ```bash
   SHORTS_ROOT="$(git rev-parse --show-toplevel)/.claude/skills/b5-cat-video-dai-thanh-shorts/goc"
   ```
3. **Cài phụ thuộc lần đầu — hỏi người dùng trước** (nặng: PyTorch, faster-whisper, mediapipe, OpenCV, Node packages của Remotion): `bash "$SHORTS_ROOT/setup.sh"`. Script tạo venv và cài vào đó; máy không có GPU thì faster-whisper chạy CPU (chậm hơn). Kiểm tra bằng `bash "$SHORTS_ROOT/scripts/preflight.sh" <video>`.
4. File tạm ở `$SHORTS_TMP` (mặc định `/tmp/claude-shorts`); clip xuất ra `./shorts/` trong thư mục làm việc của người dùng — không ghi vào thư mục skill.

## Tiếng Việt

- Chuyển giọng nói thành chữ: truyền ngôn ngữ `vi` cho `transcribe.py` (xem `--help`) thay vì để tự đoán, model whisper lớn hơn cho tiếng Việt chính xác hơn.
- Phụ đề: font Remotion kèm theo (Inter, Montserrat, Bangers trong `goc/remotion/public/fonts/`) — **Bangers không có dấu tiếng Việt**; với tiếng Việt dùng kiểu Clean / Bold với Inter hoặc Montserrat, và **render một khung xem dấu** trước khi render hết.
- Chấm điểm đoạn: trình bày lý do bằng tiếng Việt, giữ nguyên mốc thời gian.

## Ghi nhớ

- Người dùng chọn đoạn; không tự render hàng loạt khi chưa được duyệt danh sách.
- Chỉ cắt video người dùng có quyền dùng; ghi nguồn nếu là nội dung của người khác được phép.
- Liên quan: `b4-bien-tap` (dựng bản đầy đủ, phụ đề sạch), `b3-video-tiktok` (đồ họa / phụ đề TikTok), `b1-tro-ly-kenh-youtube` (`yt-shorts`: chọn đoạn từ transcript, không render).

## Trạng thái kiểm tra (15/11/2026)

Frontmatter và liên kết đã kiểm tra. **Chưa chạy thử** `setup.sh` hay quy trình render trong phiên tạo skill (cài đặt nặng, môi trường chặn chạy code vừa tải về) — lần đầu dùng chạy `preflight.sh` và thử một clip ngắn trước.
