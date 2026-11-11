# Quản lý laptop của con từ điện thoại

Miễn phí, không cần thuê server:

```
 Điện thoại ──▶ Trang web trên GitHub Pages ──▶ Firebase (Google, miễn phí) ◀── Laptop Windows của con
 Điện thoại ──▶ Telegram ◀───────────────────────────────────────────────────── (báo động + nút bấm nhanh)
```

| Thư mục / file | Là gì |
|---|---|
| `index.html`, `config.js` | Trang web quản lý (GitHub Pages phục vụ). Chỉ cần sửa `config.js`. |
| `database.rules.json` | Quy tắc bảo mật dán vào Firebase (thay 2 email). |
| `agent/` | Phần mềm cài lên laptop của con (`install.ps1`). |

**Tính năng:** tắt/khởi động lại/ngủ/khoá máy, hẹn giờ tắt · chụp và xem màn hình trực tiếp · xem/đóng/mở ứng dụng · thời gian dùng máy theo giờ, theo app, lịch sử video YouTube · YouTube Restricted Mode / chặn hẳn / từ khoá cấm · chặn trang web · giới hạn phút/ngày · giờ đi ngủ · nhắn tin lên màn hình · báo động qua Telegram.

**Hướng dẫn cài đặt từng bước cho người mới:** xem tài liệu hướng dẫn đi kèm.

### Lưu ý
- Repo phải để **Public** thì GitHub Pages mới miễn phí. Không có bí mật nào trong repo: `config.js` chứa thông tin công khai của Firebase, bảo mật nằm ở Rules. **Không** đưa file `agent/data/config.json` (trên laptop) lên GitHub.
- Laptop đã tắt hẳn thì không bật lại từ xa được.
- Tài khoản Windows của con phải là **Standard user**.
