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
| `nhan-vat-3d/chuoi-nhan-dang.json` | 19 chuỗi nhận dạng (30–50 từ) dán nguyên văn vào mọi prompt |
| `nhan-vat-3d/prompt-anh-nhan-vat.md` | 26 prompt GPT Image 2.5: chân dung khóa nhận dạng, bảng 3 góc, bảng biểu cảm, ảnh cũ trắng đen, mẫu chỉnh sửa |
| `tap/tap-01-danh-sach-canh-quay.md` | Danh sách 93 cảnh quay tập 1: luật hình ảnh, bối cảnh, mức rủi ro |
| `tap/tap-01-prompt-hinh-anh.md` | 8 prompt bối cảnh trống + keyframe (GPT Image 2.5) và chuyển động (Kling 3.0) cho 88 cảnh tạo AI |
| `cong-cu/` | Dữ liệu cảnh tập 1 (`tap01_du_lieu.py`), chuỗi nhận dạng, script sinh prompt và animatic |
| `nhan-vat-3d/blender/` | 7 nhân vật tập 1 dựng bằng Blender: `<tên>.glb` (mô hình) và `<tên>_bang.jpg` (trước / ba phần tư / sau / cận mặt), `tap01_dan-nhan-vat.jpg` (bảng tổng) |
| `tap/hinh-3d-tap01/` | 88 ảnh bố cục 3D (`01.jpg` … `93.jpg`, theo số cảnh quay) và 8 bảng xem nhanh `bang-canh-1..8.jpg` |
| `animatic/tap-01-animatic.mp4` | Animatic tập 1 (7:41, thẻ cảnh + phụ đề + âm nền). Không lưu trong git; tạo lại bằng lệnh dưới |

## Thời lượng

Mỗi tập khoảng 750–1.450 chữ (thoại + hành động). Phim tâm lý có nhiều khoảng lặng, nên ước khoảng 9–11 phút mỗi tập. Tập 6, 7, 8 ngắn hơn; nếu quay nhịp nhanh có thể chỉ khoảng 8–9 phút, khi đó kéo dài các cảnh không lời (cảnh xe máy, hành lang bệnh viện) hoặc thêm một cảnh bếp.

## Tạo lại prompt và animatic

```bash
python3 phim-gia-dinh/cong-cu/tao_prompt_tap01.py     # → tap/tap-01-prompt-hinh-anh.md
python3 phim-gia-dinh/cong-cu/tao_animatic_tap01.py   # → animatic/tap-01-animatic.mp4 (cần Pillow + ffmpeg)
```

Sửa cảnh trong `cong-cu/tap01_du_lieu.py` (giữ khớp số cảnh và thời lượng với `tap-01-danh-sach-canh-quay.md`), rồi chạy lại hai lệnh trên.

## Nhân vật 3D bằng Blender (tập 1)

```bash
uv venv --python 3.13 .venv-bpy && uv pip install --python .venv-bpy/bin/python bpy pillow   # Blender dạng thư viện Python, ~1 GB
.venv-bpy/bin/python phim-gia-dinh/cong-cu/dung_nhan_vat_blender.py --out /tmp/raw   # 7 nhân vật, ~4 phút trên 4 CPU, không cần GPU
python3 phim-gia-dinh/cong-cu/ghep_bang_nhan_vat.py /tmp/raw                          # ghép bảng có nhãn
```

Thông số mỗi nhân vật nằm trong `NHAN_VAT` ở đầu `dung_nhan_vat_blender.py` (khớp `nhan-vat-3d/*.json`). **Đây là mô hình dựng bằng hình khối, không phải mặt người "giống thật 90%"**: đúng chiều cao, tỉ lệ, dáng, màu da, tóc, trang phục và dấu nhận dạng, dùng làm tham chiếu tỉ lệ / tư thế / ánh sáng. Muốn khuôn mặt thật hơn: tạo chân dung bằng `nhan-vat-3d/prompt-anh-nhan-vat.md` rồi dùng dịch vụ ảnh → 3D, hoặc dựng mặt chi tiết trong Blender (sculpt / MB-Lab / MetaHuman).

## Cảnh 3D tập 1 (Blender)

```bash
.venv-bpy/bin/python phim-gia-dinh/cong-cu/dung_canh_3d_tap01.py [--scenes 2 5] [--shots 9 62] --samples 14   # ~11 s / ảnh trên 4 CPU
python3 phim-gia-dinh/cong-cu/ghep_bang_canh_3d.py       # bảng xem nhanh
python3 phim-gia-dinh/cong-cu/tao_animatic_tap01.py      # animatic dùng ảnh 3D
```

8 bộ cảnh dựng từ hình khối (hành lang, phòng bệnh, mái hiên mưa, trường gà, sân nhà, bữa cơm, phòng Mẹ, sân sau). Vị trí nhân vật: `SCENE_CFG` / `OVR` trong `dung_canh_3d_tap01.py`; camera tính từ cỡ cảnh, ống kính và góc máy trong `tap01_du_lieu.py`, hướng nhìn riêng: `AZ`. **Đây là ảnh bố cục** (vị trí, cỡ cảnh, trục máy, ánh sáng) với nhân vật hình khối, không phải ảnh phim cuối. 5 cảnh có chữ trong khung (02, 42, 72, 78, 79) không dựng. Cảnh 35 (tay giơ tiền) và 38 (tay trao giấy) chưa có chi tiết bàn tay.

## Quy trình sản xuất gợi ý (dùng các skill trong repo)

1. **Phân cảnh, danh sách cảnh quay:** `ho-tro-danh-sach-canh-quay` cho từng tập (bảng tiếng Việt có cỡ cảnh, góc máy, ánh sáng, mốc liên tục).
2. **Hình ảnh nhân vật và keyframe:** `mo-phong-cong-viec-dao-dien` (nhánh image) dựa trên `nhan-vat-3d/*.json`. Dựng 3D thật bằng Blender: `cong-cu-san-xuat-video` (cần máy có Blender và GPU).
3. **Clip chuyển động từ keyframe:** `mo-phong-cong-viec-dao-dien` (nhánh video) viết prompt cho Kling / Veo / Seedance, giữ khối nhận dạng nhân vật giống nhau ở mọi prompt.
4. **Lồng tiếng, nhạc, dựng:** `cong-cu-san-xuat-video` (thuyết minh AI) hoặc thu giọng thật, rồi `bien-tap` để cắt, làm phụ đề tiếng Việt, nhạc nền.
5. **Đăng YouTube:** `video-youtube` (intro / outro), `tro-ly-kenh-youtube` (tiêu đề, mô tả, chapters), `cat-video-dai-thanh-shorts` (cắt Shorts quảng bá).

## Nội dung nhạy cảm

Phim có đá gà, cờ bạc, lô đề, cho vay nặng lãi và cán bộ nhận hối lộ. Kịch bản thể hiện hậu quả, không hướng dẫn hay cổ vũ; bạo lực xảy ra ngoài khung hình; pháp luật cấp tỉnh giải quyết đường dây. Khi đăng lên nền tảng, nên chọn độ tuổi phù hợp và ghi chú "nhân vật, sự việc hư cấu".
