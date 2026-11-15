# Biên tập — skill dựng video bản đầu cho Claude Code

Claude dựng bản đầu cho vlog, bài giảng, video nói trước camera: chuyển giọng nói thành chữ, bỏ đoạn quay lại / nói vấp / khoảng lặng thừa mà vẫn giữ nhịp tự nhiên, giữ B-roll, zoom jump-cut và punch-in, chuẩn hóa giọng, nhạc nền tự hạ khi có lời, phụ đề sạch, xuất cho YouTube. Mọi thứ dựng bằng **ffmpeg** qua các script trong `scripts/` (Python thư viện chuẩn). DaVinci Resolve Studio là **tùy chọn** (`davinci/`).

## Cần
- ffmpeg 6+ (có filter `subtitles`, `loudnorm`), Python 3.9+
- Một API speech-to-text có timestamp từng từ (mặc định ElevenLabs Scribe)
- Tùy chọn: Node + Remotion (đồ họa động), Epidemic Sound / thư viện nhạc có bản quyền, DaVinci Resolve Studio

## Dùng
1. "set up my video editor" / "tạo workspace biên tập" → `scripts/init.py`
2. Bỏ video vào `raw video/`, nói "dựng video mới"
3. Góp ý bằng lời thường: "giật quá", "bỏ 02:14–02:20", "thêm nhạc", "thêm phụ đề", "xuất cho YouTube"

Kiểm tra cài đặt: `python3 scripts/selftest.py` (video giả lập, không cần key).

## Nguồn và giấy phép
Dựa trên [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills) © 2026 appariciojunior, giấy phép [CC BY-NC 4.0](LICENSE). **Đã chỉnh sửa**: gộp 12 skill thành một, thêm bộ script ffmpeg chạy được, viết lại hướng dẫn chính bằng tiếng Việt, tách phần DaVinci Resolve ra `davinci/`. Không dùng cho mục đích thương mại (không bán, không dùng trong sản phẩm/dịch vụ thu phí) nếu chưa hỏi tác giả.
