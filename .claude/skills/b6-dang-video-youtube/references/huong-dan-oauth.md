# Lấy khóa OAuth để đăng video (làm một lần)

Làm trên máy tính, đăng nhập đúng tài khoản Google sở hữu kênh YouTube.

1. Vào https://console.cloud.google.com/ → **Tạo project mới** (ví dụ `b6-dang-video-youtube`).
2. **APIs & Services → Library** → tìm **YouTube Data API v3** → **Enable**.
3. **APIs & Services → OAuth consent screen** (hoặc *Google Auth Platform*):
   - User type: **External**; điền tên ứng dụng, email của bạn.
   - Phần **Audience / Test users**: thêm chính email của bạn.
   - Scope: thêm `.../auth/youtube.upload`.
4. **Credentials → Create credentials → OAuth client ID** → loại **Desktop app** → tạo → **Download JSON**.
5. Lưu file thành `~/.config/b6-dang-video-youtube/client_secret.json` (hoặc đặt biến `YT_CLIENT_SECRET_FILE`). Không đưa file này lên git, không dán vào chat.
6. Chạy `youtube_upload.py login`, chọn kênh, bấm **Cho phép**. Thấy cảnh báo "Google hasn't verified this app": **Advanced → Go to … (unsafe)** (ứng dụng do chính bạn tạo).

## Hai điều bất ngờ hay gặp

- **Video lên rồi nhưng bị khóa riêng tư** (thông báo "video đã bị khóa ở chế độ riêng tư vì dịch vụ API chưa qua kiểm duyệt"): project của bạn chưa được **YouTube API Services Audit**. Gửi form audit của YouTube để được đăng công khai bằng API; trước đó hãy chuyển công khai thủ công trong YouTube Studio.
- **Mỗi 7 ngày phải đăng nhập lại:** app ở trạng thái *Testing* có refresh token sống 7 ngày. Chuyển consent screen sang **In production** để token không hết hạn (app chỉ mình bạn dùng thì không cần xác minh).

## Hạn mức

Mặc định 10.000 đơn vị/ngày; `videos.insert` ≈ 1.600, `thumbnails.set` ≈ 50 → khoảng 6 video/ngày. Xin tăng ở trang *Quotas* của project nếu cần.
