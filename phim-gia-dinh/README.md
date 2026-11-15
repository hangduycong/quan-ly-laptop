# Mùa Cuối Của Mẹ (tên tạm)

Phim dài tập tình cảm gia đình, 12 tập × khoảng 10 phút. Nhân vật chính: Minh, em trai út, đứng giữa hai nhà của mẹ và cha. Toàn bộ nhân vật và sự việc là hư cấu.

## Nội dung thư mục

| File | Nội dung |
|---|---|
| `bible/nhan-vat-va-gia-dinh.md` | Cây gia đình hai nhà, tính cách và tuyến truyện từng người, thế lực ông Sáu Lộc, bí mật lá thư, quy tắc giọng điệu, đồ vật xuyên suốt |
| `tap/dan-y-ca-mua.md` | Dàn ý 12 tập, hai tuyến truyện, hậu quả và cách làm lại của từng nhân vật |
| `tap/tap-01-…md` → `tap/tap-12-…md` | Kịch bản đầy đủ từng tập, có mốc thời gian theo cảnh và ghi chú sản xuất |
| `nhan-vat-3d/minh.spec.json` | Thông số 3D chi tiết của Minh |
| `nhan-vat-3d/dan-nhan-vat.json` | Thông số 3D cho tất cả nhân vật còn lại, trẻ em, thế lực xấu và Ông Tám (trong ảnh) |

## Thời lượng

Mỗi tập khoảng 750–1.450 chữ (thoại + hành động). Phim tâm lý có nhiều khoảng lặng, nên ước khoảng 9–11 phút mỗi tập. Tập 6, 7, 8 ngắn hơn; nếu quay nhịp nhanh có thể chỉ khoảng 8–9 phút, khi đó kéo dài các cảnh không lời (cảnh xe máy, hành lang bệnh viện) hoặc thêm một cảnh bếp.

## Quy trình sản xuất gợi ý (dùng các skill trong repo)

1. **Phân cảnh, danh sách cảnh quay:** `ho-tro-danh-sach-canh-quay` cho từng tập (bảng tiếng Việt có cỡ cảnh, góc máy, ánh sáng, mốc liên tục).
2. **Hình ảnh nhân vật và keyframe:** `mo-phong-cong-viec-dao-dien` (nhánh image) dựa trên `nhan-vat-3d/*.json`. Dựng 3D thật bằng Blender: `cong-cu-san-xuat-video` (cần máy có Blender và GPU).
3. **Clip chuyển động từ keyframe:** `mo-phong-cong-viec-dao-dien` (nhánh video) viết prompt cho Kling / Veo / Seedance, giữ khối nhận dạng nhân vật giống nhau ở mọi prompt.
4. **Lồng tiếng, nhạc, dựng:** `cong-cu-san-xuat-video` (thuyết minh AI) hoặc thu giọng thật, rồi `bien-tap` để cắt, làm phụ đề tiếng Việt, nhạc nền.
5. **Đăng YouTube:** `video-youtube` (intro / outro), `tro-ly-kenh-youtube` (tiêu đề, mô tả, chapters), `cat-video-dai-thanh-shorts` (cắt Shorts quảng bá).

## Nội dung nhạy cảm

Phim có đá gà, cờ bạc, lô đề, cho vay nặng lãi và cán bộ nhận hối lộ. Kịch bản thể hiện hậu quả, không hướng dẫn hay cổ vũ; bạo lực xảy ra ngoài khung hình; pháp luật cấp tỉnh giải quyết đường dây. Khi đăng lên nền tảng, nên chọn độ tuổi phù hợp và ghi chú "nhân vật, sự việc hư cấu".
