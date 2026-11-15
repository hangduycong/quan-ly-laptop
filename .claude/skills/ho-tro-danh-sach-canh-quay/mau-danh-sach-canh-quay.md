# Mẫu danh sách cảnh quay (tiếng Việt)

Bản tiếng Việt của `goc/assets/shot-plan-template.md`. Định nghĩa từng cột, ví dụ tốt/xấu, cách chấm rủi ro và cách tự kiểm tra độ phủ cảnh (coverage) vẫn theo file gốc; file này chỉ đặt tên cột, thuật ngữ và mẫu điền bằng tiếng Việt. Chỉ lập bảng **sau khi** đã có beat (beat sheet) và luật hình ảnh (director's book).

## Bảng đầy đủ

| # | Thời gian | Beat / nhiệm vụ | Bối cảnh | Nội dung khung hình | Diễn xuất: đầu → chuyển động → cuối | Cỡ cảnh / Góc máy | Ống kính | Chuyển động máy | Hướng sáng | Ánh sáng / không khí | Mốc liên tục | Rủi ro | Chuyển cảnh | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 0:00–0:04 (4s) | B1 · … | loc_… / … | … | bắt đầu … → … → kết thúc … | WS, ngang mắt | 35mm — vì … | đứng yên | key: …, cao, trái máy 45°, 5:1 | … | … | Xanh 5 (…) | cắt thẳng khi … | … |

| Cột | Phải có | Tốt | Kém |
|---|---|---|---|
| `#` | Số thứ tự theo truyện, 2 chữ số, giữ cố định; tách thì thành `04a`, `04b` | `04` | `Cảnh 4 (trước là 3)` |
| Thời gian | Vào – ra trong cảnh + độ dài | `0:12–0:18 (6s)` | `khoảng 6 giây` |
| Beat / nhiệm vụ | Mã beat + việc cảnh này làm cho beat đó | `B4 · trao đi không lấy lại được` | `khoảnh khắc cảm xúc` |
| Bối cảnh | Mã bối cảnh trong continuity bible + vị trí máy | `loc_chieu_nghi / phía cửa, thấp` | `hành lang` |
| Nội dung khung hình | Thứ người vẽ storyboard sẽ vẽ: vị trí chủ thể + 2–3 chi tiết bối cảnh / đạo cụ bắt buộc có | `đầu và vai gần ở trái khung, mặt cửa tối chiếm bên phải, mép phong bì ở góc dưới trái` | `anh ấy đứng ở cửa` |
| Diễn xuất | Ba trạng thái, trạng thái cuối nói rõ | `đứng thẳng trước cửa → tay phải giơ lên, khớp tay dừng cách gỗ 3cm → hạ tay xuống đùi, vẫn nhìn cửa` | `anh ấy ngập ngừng gõ cửa` |
| Cỡ cảnh / Góc máy | Một cỡ trên thang + góc (độ) hoặc độ cao máy (cm) | `MCU, ngang mắt` / `MS, thấp, máy cách sàn 40cm, ngửa 10°` | `trung trung, góc kịch tính` |
| Ống kính | Tiêu cự mm (quy đổi full-frame) + lý do khi không hiển nhiên | `85mm — nén khoảng cách, giấu hành lang phía sau` | `tele` |
| Chuyển động máy | Đúng **một** chuyển động có quãng và thời gian, hoặc `đứng yên` | `dolly-in chậm 25cm trong 6s` | `đẩy nhẹ, hơi trôi` |
| Hướng sáng | Hướng key so với máy này, độ cao, nguồn thực tế tạo ra nó, tỉ lệ sáng:tối, fill là gì | `key: bóng đèn cầu thang, cao, trái máy 45°, 5:1, fill chỉ là phản xạ tường` | `ánh sáng bên huyền bí` |
| Ánh sáng / không khí | Điều ánh sáng làm ở khung này mà khung trước chưa làm | `mặt cửa tối hơn 1,5 stop; bụi trong vệt nắng; thấy hơi thở` | `tối và lạnh` |
| Mốc liên tục | Những thứ phải khớp với cảnh kề: nhận dạng, trang phục, trạng thái đạo cụ, trạng thái ánh sáng | `sẹo xuyên lông mày trái, mũ đẩy ra sau, túi đeo vai trái, phong bì mặt trắng ra ngoài` | `cùng nhân vật và bối cảnh` |
| Rủi ro | Mức `Xanh` / `Vàng` / `Đỏ` theo thang khó trong `goc/references/production-workflow.md` + 6 điểm (Hành động / Người / Máy / Thời lượng / Tương tác / Liên tục) + chiều quyết định mức | `Đỏ 12 (3/1/1/2/3/2) — tương tác 3, có tiếp xúc` | `hơi khó` |
| Chuyển cảnh | Rời cảnh thế nào, ở khung nào | `cắt thẳng đúng khung đầu ngón tay chạm gỗ` | `cắt sang cảnh sau` |
| Ghi chú tạo AI | Điều model sẽ làm sai, câu lệnh ngăn nó, và phương án tách cảnh nếu vẫn sai | `ghi "khớp tay dừng trước cửa, không chạm"; negative: knocking, hand on door; vẫn gõ thì rút còn 3s` | `prompt tốt, chất lượng cao` |

## Bảng rút gọn (khi chat, trả lời ngắn, hoặc bản nháp đầu)

| # | Khung hình | Hành động → trạng thái cuối |
|---:|---|---|
| 01 | WS · 35mm · cao +15° · đứng yên · 4s | Anh leo lên chiếu nghỉ, đi ba bước — dừng thẳng trước cửa cách 60cm, phong bì ngang ngực, bất động. |

## Thuật ngữ (Việt — Anh — viết tắt)

**Cỡ cảnh** (thang 6 bậc, cắt nhảy ≥ 2 bậc nếu góc máy giữ nguyên):

| Bậc | Tiếng Việt | Tiếng Anh | Khung gồm |
|---:|---|---|---|
| 1 | Toàn cảnh rất rộng | Extreme wide shot — EWS | người ≤ 1/8 chiều cao khung |
| 2 | Toàn cảnh | Wide shot — WS | cả người + môi trường |
| 3 | Trung cảnh | Medium shot — MS | từ thắt lưng trở lên |
| 4 | Cận trung | Medium close-up — MCU | từ ngực trở lên |
| 5 | Cận cảnh | Close-up — CU | đầu và vai |
| 6 | Đặc tả | Extreme close-up — ECU | mắt, miệng, tay, đồ vật |

**Góc máy:** ngang mắt (eye level) · góc thấp / ngửa (low angle) · góc cao / chúc (high angle) · từ trên xuống (overhead / top-down) · nghiêng khung (Dutch) · qua vai (over-the-shoulder — OTS) · nghiêng mặt (profile) · góc nhìn nhân vật (POV).

**Chuyển động máy:** đứng yên (locked) · đẩy vào (push-in / dolly-in) · kéo ra (pull-back / dolly-out) · lia ngang (pan) · lia dọc (tilt) · đi theo (tracking / follow) · cầm tay (handheld) · vòng quanh (orbit / arc) · cẩu (crane / boom) · lia nhanh (whip pan) · dolly zoom.

**Chức năng cảnh** (9 loại, không tự đặt thêm): thiết lập bối cảnh (establishing) · quan hệ (relation) · cận cảnh (close-up) · chèn chi tiết (insert / detail) · phản ứng (reaction) · chuyển tiếp (transition) · dư âm (aftermath) · góc nhìn (point-of-view) · hé lộ (reveal).

**Khác:** trục hành động / luật 180° (axis of action) · luật 30° · hướng màn hình (screen direction) · khớp ánh nhìn (eyeline match) · độ dài cảnh trung bình (ASL) · ánh sáng chính / phụ / viền (key / fill / rim) · nguồn sáng thực trong cảnh (practical).

## Xuất file

Khi người dùng cần file để in hoặc gửi đoàn phim: CSV (UTF-8 có BOM để Excel đọc đúng dấu) với đúng các cột trên, hoặc dùng skill bảng tính (xlsx) nếu có. Prompt cho model tạo ảnh/video viết **tiếng Anh** (mặc định của skill gốc), bảng và giải thích viết **tiếng Việt**.
