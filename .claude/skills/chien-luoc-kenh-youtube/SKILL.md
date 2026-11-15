---
name: chien-luoc-kenh-youtube
description: 'Chiến lược kênh YouTube — claude-youtube orchestrator with 14 sub-skills - channel audit, video SEO and keyword research, retention-engineered scripts, hooks, thumbnail briefs, channel strategy and positioning, content calendar, Shorts strategy, analytics interpretation, monetisation planning, competitor research, cross-platform repurposing, upload metadata packages, data-driven video ideas; channel-type templates (education, tutorial, review, vlog, commentary…); optional live data via YouTube Data / Analytics API and DataForSEO. Use for "chiến lược kênh YouTube", "phát triển kênh", "kiếm tiền YouTube", "phân tích đối thủ", "ý tưởng video", "lịch nội dung", "SEO YouTube", "phân tích số liệu kênh", "tái sử dụng video", "/chien-luoc-kenh-youtube".'
---

# Chiến lược kênh YouTube

> Nguồn: [AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube) (MIT, `LICENSE`, © 2025 Daniel Agrici), commit `84c3fa6`. Bản gốc trong `goc/` (nội dung của `skills/claude-youtube/` + README). File này là phần viết thêm.

Bộ điều phối 14 skill con về tăng trưởng, tối ưu và kiếm tiền cho kênh YouTube.

## Cách chạy

1. **Đọc `goc/SKILL.md`** — bảng định tuyến lệnh (`/youtube audit`, `seo`, `script`, `hook`, `thumbnail`, `strategy`, `calendar`, `shorts`, `analyze`, `repurpose`, `monetize`, `competitor`, `metadata`, `ideate`) → mở `goc/sub-skills/<tên>.md` tương ứng. Đường dẫn `references/`, `templates/`, `execution/` tính từ `goc/`.
2. Biết loại kênh thì đọc mẫu chiến lược hợp: `goc/templates/<loại>-channel.md` (education, tutorial, review, vlog, commentary, entertainment, personal-brand, niche-authority, shorts-first).
3. Không có dữ liệu thật thì làm từ thông tin người dùng đưa + WebSearch; nói rõ đâu là số liệu thật, đâu là ước đoán.

## Dữ liệu kênh thật (tùy chọn)

- Script `goc/execution/*.py` (lấy dữ liệu kênh, transcript, analytics, video đối thủ) cần thư viện Google API (`pip install google-api-python-client google-auth-oauthlib` — hỏi người dùng trước) và:
  - **`YOUTUBE_API_KEY`** (YouTube Data API v3, miễn phí trong hạn mức, tạo ở Google Cloud Console) — người dùng tự đặt làm biến môi trường hoặc trong `~/.claude/youtube-credentials.json`; **không dán key vào chat, không commit vào repo**.
  - Số liệu Analytics riêng của kênh: OAuth (người dùng tự đăng nhập Google trên máy họ).
  - `execution/utils/quota_tracker.py` theo dõi hạn mức API — tôn trọng nó, không gọi lặp.
- **DataForSEO MCP** (dịch vụ trả phí) chỉ dùng nếu người dùng đã cấu hình; thiếu thì quay về WebSearch + script, không chặn quy trình.

## Tiếng Việt và thị trường Việt Nam

- Mọi phân tích, kế hoạch, kịch bản, tiêu đề, mô tả: **tiếng Việt** khi kênh nói tiếng Việt; từ khóa SEO nghiên cứu theo cách người Việt gõ (có dấu và không dấu).
- Mốc doanh thu, CPM, thời gian xem trong tài liệu gốc chủ yếu theo thị trường Mỹ — với khán giả Việt Nam nói rõ số liệu khác (CPM thường thấp hơn), không chép nguyên con số.
- Điều kiện kiếm tiền và chính sách YouTube thay đổi: kiểm tra lại trên trang chính thức của YouTube trước khi khẳng định.

## Liên quan

`tro-ly-kenh-youtube` (công cụ nhỏ có script kiểm tra: tiêu đề, chapters, retention, hook), `cat-video-dai-thanh-shorts` (render Shorts), `video-youtube` (intro / outro / audiogram), `bien-tap` (dựng video).

## Trạng thái kiểm tra (15/11/2026)

Frontmatter và liên kết đã kiểm tra; đã đọc phần xác thực (`youtube_auth.py`: key từ biến môi trường hoặc file credentials). **Chưa chạy** script gọi YouTube API (cần key của người dùng).
