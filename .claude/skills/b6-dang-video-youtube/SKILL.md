---
name: b6-dang-video-youtube
description: 'Đăng video lên YouTube — upload video thật qua YouTube Data API v3 + OAuth 2.0 (chỉ dùng thư viện chuẩn Python): đăng nhập một lần, tải lên theo từng đoạn có tự nối lại, đặt tiêu đề / mô tả / thẻ / danh mục, ảnh thumbnail, hẹn giờ công khai, đánh dấu Shorts, khai báo nội dung do AI tạo và nội dung cho trẻ em; mặc định đăng ở chế độ riêng tư và chỉ công khai khi người dùng đồng ý. Dùng khi người dùng muốn "đăng video lên YouTube", "upload YouTube", "tải video lên kênh", "đăng Shorts", "hẹn giờ đăng", "đặt thumbnail", "/b6-dang-video-youtube".'
---

# Đăng video lên YouTube

Upload video thật lên kênh YouTube của người dùng bằng **YouTube Data API v3** (`videos.insert` dạng resumable + `thumbnails.set`), xác thực **OAuth 2.0** (PKCE, quyền tối thiểu `youtube.upload`). Một file Python, không cần cài thêm thư viện: `scripts/youtube_upload.py`.

Đây là việc **đăng công khai ra ngoài**: làm đúng các bước an toàn bên dưới, không đăng công khai khi người dùng chưa đồng ý rõ ràng.

## Quy trình

1. **Kiểm tra điều kiện.** `python3 .claude/skills/b6-dang-video-youtube/scripts/youtube_upload.py doctor` → báo thiếu file khóa OAuth, chưa đăng nhập, thiếu ffprobe. Chưa có khóa OAuth: đọc `references/huong-dan-oauth.md` (tạo project Google Cloud, bật API, tạo OAuth client "Desktop app") và hướng dẫn người dùng làm; **không** nhờ họ dán khóa vào khung chat, chỉ đặt file `client_secret.json` vào `~/.config/b6-dang-video-youtube/`.
2. **Đăng nhập một lần** (lưu refresh token, quyền 600):
   - máy có trình duyệt: `... youtube_upload.py login`
   - phiên đám mây / không có trình duyệt: `... login-url` → người dùng mở link trên máy mình, bấm cho phép, trang báo lỗi "không kết nối được 127.0.0.1" là bình thường → họ copy **toàn bộ địa chỉ** trên thanh địa chỉ gửi lại → `... login-finish "<địa chỉ đó>"`.
3. **Soạn metadata** vào `meta.json` (xem mẫu `mau-meta.json`). Tiêu đề / mô tả / thẻ tốt hơn: dùng skill `b1-tro-ly-kenh-youtube` (`/b1-tro-ly-kenh-youtube`, mục `yt-package`) và `b1-chien-luoc-kenh-youtube`.
4. **Chạy thử không gửi gì:** `... upload VIDEO --meta meta.json --dry-run` (kiểm tra độ dài tiêu đề, ký tự cấm, tổng độ dài thẻ, Shorts ≤ 3 phút và dọc…, in ra đúng nội dung sẽ gửi).
5. **Xác nhận với người dùng** trước khi gửi: nói rõ tên file, tiêu đề, chế độ (riêng tư / không công khai / công khai / hẹn giờ), có khai báo AI, có thumbnail.
6. **Đăng:** `... upload VIDEO --meta meta.json [--thumbnail thumb.jpg] [--privacy private|unlisted|public --yes] [--publish-at 2026-12-01T19:00:00+07:00] [--shorts] [--ai-generated]`. In ra `https://youtu.be/<id>`.
7. Báo lại cho người dùng link, chế độ hiện tại, và (nếu để riêng tư) cách chuyển công khai trong YouTube Studio.

## Quy tắc an toàn

- **Mặc định `--privacy private`.** `public` bắt buộc có `--yes`, và chỉ thêm `--yes` sau khi người dùng nói đồng ý công khai (nội dung này có thể bị lập chỉ mục / chia sẻ, không thu hồi hết được).
- Hẹn giờ (`--publish-at`) tự đặt video ở chế độ riêng tư cho đến giờ đó.
- Video có giọng đọc / hình ảnh do AI tạo (như các Shorts làm trong repo này): dùng `--ai-generated` để khai báo nội dung tổng hợp, đúng quy định của YouTube.
- `--made-for-kids yes` nếu video dành cho trẻ em; mặc định `no`. Đây là khai báo pháp lý của người đăng, hỏi nếu chưa rõ.
- Không in, không ghi log refresh token / client secret. Token nằm ở `~/.config/b6-dang-video-youtube/token.json` (chmod 600); không commit file đó. Thu hồi quyền: `... logout` rồi vào https://myaccount.google.com/permissions.
- Không đăng nội dung vi phạm điều khoản YouTube hoặc nội dung của người khác khi chưa có phép.

## Giới hạn cần nói với người dùng

- **Project Google Cloud chưa qua kiểm duyệt (audit): mọi video upload qua API bị khóa ở chế độ riêng tư** (từ 28/07/2020). Muốn đăng công khai bằng API phải gửi form "YouTube API Services – Audit"; trong lúc chưa có, đăng riêng tư rồi chuyển công khai bằng tay trong YouTube Studio. Script nhận ra lỗi này và báo rõ.
- **Hạn mức:** mặc định 10.000 đơn vị / ngày, mỗi lần upload tốn khoảng 1.600 → khoảng 6 video / ngày. Hết hạn mức báo `quotaExceeded`, thử lại sau 0 giờ giờ Thái Bình Dương.
- Màn hình đồng ý OAuth ở trạng thái "Testing" (loại External): **refresh token hết hạn sau 7 ngày**, phải `login` lại; chuyển sang "In production" để dùng lâu dài (tự dùng cho tài khoản của mình thì không cần xác minh app, chỉ hiện cảnh báo "ứng dụng chưa được xác minh").
- Chưa hỗ trợ: phụ đề (cần thêm quyền `youtube.force-ssl`), thêm vào playlist, sửa video đã đăng.

## Lệnh

| Lệnh | Việc |
|---|---|
| `doctor` | kiểm tra file khóa, token, ffprobe |
| `login` / `login-url` + `login-finish "<url>"` | đăng nhập OAuth (có trình duyệt / không có) |
| `logout` | xóa token trên máy và thu hồi trên Google |
| `check VIDEO --meta meta.json` | kiểm tra, không gửi |
| `upload VIDEO --meta meta.json …` | đăng (cờ ở trên; `--dry-run` chỉ in) |
| `selftest` | thử toàn bộ luồng với server giả lập cục bộ, không gọi Google |

Cờ chung: `--client-secret FILE`, biến môi trường `YT_CLIENT_SECRET_FILE`, `YT_CONFIG_DIR` (đổi thư mục lưu token).

## Ví dụ với video có sẵn trong repo

```bash
python3 .claude/skills/b6-dang-video-youtube/scripts/youtube_upload.py upload \
  video-shorts/vo-chong/shorts-vo-chong-30s.mp4 \
  --meta .claude/skills/b6-dang-video-youtube/mau-meta.json --shorts --ai-generated --dry-run
```
