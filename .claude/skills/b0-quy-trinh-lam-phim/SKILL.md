---
name: b0-quy-trinh-lam-phim
description: 'Quy trình làm phim / video từ ý tưởng đến đăng lên YouTube — skill điều phối (Agent Lead): chia việc thành 6 bước, chọn đúng skill cho từng bước (kịch bản, phân cảnh, sản xuất hình và tiếng, dựng, đóng gói, đăng), chọn đường đi theo loại sản phẩm (Shorts nhanh, video nói trước camera, phim AI nhiều tập), đặt các cổng cần người dùng đồng ý (tốn tiền, dùng giọng hoặc ảnh người thật, đăng công khai) và giao việc từng bước cho subagent. Dùng khi người dùng muốn "làm một video / phim từ đầu", "chạy quy trình Agent Lead", "quy trình sản xuất video", "nên dùng skill nào", "video-producer", "/b0-quy-trinh-lam-phim".'
---

# Quy trình làm phim / video (Agent Lead)

Tên skill trong repo đánh số theo bước: `b1-…` → `b6-…`. Skill này là **bản đồ và người điều phối**: không tự dựng gì, mà chọn skill đúng, giữ file đầu vào / đầu ra giữa các bước nối khớp nhau, và dừng ở các cổng cần người dùng quyết.

## 6 bước và skill của từng bước

| Bước | Việc | Skill | Đầu ra |
|---|---|---|---|
| **B1** Ý tưởng và kịch bản | định vị kênh, ý tưởng, lịch; viết kịch bản, chấm câu mở đầu (hook) | `b1-chien-luoc-kenh-youtube`, `b1-tro-ly-kenh-youtube` | `kich-ban.md` (thoại, thời lượng ước tính) |
| **B2** Phân cảnh và prompt | danh sách cảnh quay, góc máy, prompt ảnh / video AI | `b2-ho-tro-danh-sach-canh-quay`, `b2-mo-phong-cong-viec-dao-dien` | bảng cảnh quay, prompt từng cảnh |
| **B3** Sản xuất hình, tiếng, đồ họa | tạo ảnh / clip / đồ họa chuyển động / giọng đọc | chọn theo loại, bảng bên dưới | file hình, clip, âm thanh |
| **B4** Dựng | cắt ghép, phụ đề, nhạc, chỉnh màu, b-roll, lower third | `b4-bien-tap`, `b4-chinh-sua-video`, `b4-chinh-sua-video-dai`, `b4-ffmpeg-skill`, `b4-b-roll-cho-video`, `b4-lower-third` | bản dựng `.mp4` |
| **B5** Đóng gói | intro / outro, cắt Shorts từ video dài, tiêu đề / mô tả / mốc chương / thumbnail | `b5-video-youtube`, `b5-cat-video-dai-thanh-shorts`, `b1-tro-ly-kenh-youtube` (gọi lại để đóng gói) | bản cuối + `meta.json` |
| **B6** Đăng | upload lên YouTube | `b6-dang-video-youtube` | link video |

Công cụ nền (không thuộc bước nào): `tao-skill-rieng-theo-nhu-cau` (tạo / kiểm tra skill), `tuan-thu-quy-trinh` (quy trình phát triển phần mềm).

### Chọn skill ở B3 theo loại sản phẩm

| Cần làm | Skill |
|---|---|
| chưa biết chọn gì trong 56 workflow đồ họa | `b3-tao-do-hoa-chuyen-dong` (mục lục) |
| video từ HTML (HyperFrames): giới thiệu, giải thích, clip dọc | `b3-ho-tro-tao-video` |
| từ kịch bản đến MP4 có thuyết minh AI, nhiều dịch vụ AI (trả phí) | `b3-cong-cu-san-xuat-video` |
| TikTok / Reels / Shorts, phụ đề nhảy chữ | `b3-video-tiktok`, `b3-chu-chuyen-dong` |
| kể chuyện bằng tin nhắn | `b3-video-tin-nhan` |
| giải thích, sơ đồ, whiteboard, tổng kết năm | `b3-video-giai-thich` |
| biểu đồ, số liệu, slide thành video | `b3-bieu-do-dong` |
| bản đồ, tuyến đường | `b3-ban-do-dong` |
| toán / vật lý kiểu 3Blue1Brown | `b3-video-toan-hoc-manim` |
| bán hàng, quảng cáo, ra mắt sản phẩm | `b3-video-ban-hang`, `b3-video-quang-cao`, `b3-video-ra-mat-du-an` |
| người nói bằng AI (ảnh + giọng của chính người dùng) | `b3-video-nguoi-noi-ai` |
| tranh minh họa AI chuyển động, phim vẽ bằng code | `b3-minh-hoa-ai-chuyen-dong`, `b3-animation-javascript` |
| animation cho website | `b3-animation-web` |

## Chọn đường đi

1. **Shorts nhanh (≤ 60 giây, ý tưởng → video trong một buổi):** B1 (kịch bản ~70–80 từ cho 30 giây) → giọng đọc → hình (đồ họa chữ động bằng Pillow + ffmpeg, hoặc `b3-video-tiktok`) → kiểm tra khung hình → B6. Ví dụ đã chạy thật: `video-shorts/vo-chong/` (script `dung_video.py`).
2. **Video nói trước camera / vlog / bài giảng:** quay xong → B4 `b4-bien-tap` (nguồn dài nhiều giờ: `b4-chinh-sua-video-dai`) → B5 (intro / outro, mốc chương) → B6.
3. **Phim AI nhiều tập:** B1 (bible nhân vật, dàn ý, kịch bản từng tập) → B2 (danh sách cảnh quay, chuỗi nhận dạng nhân vật, prompt keyframe + chuyển động) → B3 (ảnh / clip, dựng 3D tham chiếu) → B4 → B5 → B6. Ví dụ: `phim-gia-dinh/`.
4. **Video dài → nhiều Shorts:** B4 (bản dài) → `b5-cat-video-dai-thanh-shorts` → B6 cho từng clip.

## Điều phối

1. **Lập brief một lần** trước khi bắt đầu, ghi vào đầu `kich-ban.md`: mục tiêu, nền tảng và khổ hình, thời lượng, giọng điệu, ngôn ngữ, ngân sách, bản quyền nhạc / hình / giọng. Thiếu thông tin nào quan trọng mới hỏi; còn lại tự quyết và nói rõ đã chọn gì.
2. **Mỗi bước là một nhiệm vụ độc lập** có file vào và file ra rõ ràng (cột "Đầu ra" ở trên). Có thể giao cho subagent (`video-producer` trong `.claude/agents/`) và kiểm tra đầu ra trước khi sang bước sau; không chuyển bước khi đầu ra chưa đạt.
3. **Kiểm tra bằng mắt và tai, không chỉ bằng mã thoát:** xuất vài khung hình tiêu biểu (đầu, giữa, cuối mỗi cảnh) để nhìn chữ tràn mép, sai dấu tiếng Việt, hình lệch; đo âm lượng (`ffmpeg -af volumedetect`, mục tiêu khoảng -14 LUFS cho YouTube).
4. **Báo trung thực:** việc nào chưa chạy thử, hạn chế nào của sản phẩm (ví dụ "nhân vật 3D là hình khối, chưa giống thật") nói thẳng.

## Cổng cần người dùng đồng ý (không tự làm)

- **Tốn tiền hoặc dịch vụ ngoài:** giọng ElevenLabs, fal.ai, GPU cloud, ảnh AI trả phí. Nói ước tính trước khi chạy.
- **Giọng, mặt, tên của người thật:** chỉ dùng của chính người dùng hoặc người đã đồng ý; nhân vật phim giữ hư cấu.
- **Cài đặt nặng** (Blender, whisper, ~1 GB): hỏi trước.
- **Đăng công khai:** `b6-dang-video-youtube` mặc định riêng tư; chỉ thêm `--yes` sau khi người dùng nói "công khai". Đăng thật cần người dùng xác nhận từng lần.
- **Khai báo AI:** video có giọng / hình do AI tạo dùng `--ai-generated` khi đăng.

## Kinh nghiệm đã kiểm chứng trong repo này

- **Giọng đọc ElevenLabs:** giọng "thư viện" (library voices) báo lỗi 402 trên gói miễn phí; dùng giọng có sẵn như Sarah (`EXAVITQu4vr4xnSDxMaL`) với model `eleven_multilingual_v2` đọc được tiếng Việt. Gọi `/v1/text-to-speech/<voice>/with-timestamps` để lấy mốc từng ký tự, dùng cho phụ đề bám giọng. **Kiểm tra độ rõ:** chép lại chính file giọng bằng ElevenLabs Scribe (`scribe_v2`, `language_code=vie`) rồi so với lời gốc; với giọng Sarah đọc tiếng Việt, bản chép lại sai nhiều chỗ ("Vợ chồng cãi nhau không đáng sợ" thành "Vở chồng cái in hậu không giang so"), tức phát âm chưa chuẩn bản xứ. Người dùng nên nghe lại trước khi đăng; muốn giọng Việt tốt hơn cần giọng được huấn luyện cho tiếng Việt hoặc thu giọng thật.
- **Font tiếng Việt đủ dấu:** `DejaVu Sans Bold` (có sẵn ở `/usr/share/fonts/truetype/dejavu/`); chữ to dễ tràn mép khung dọc 1080 px, kiểm tra bằng khung hình.
- **Âm lượng:** `loudnorm=I=-14:TP=-1.5` cho bản cuối đăng YouTube; nhạc nền hạ xuống ~0,16 so với giọng.
- **Shorts:** ≤ 3 phút, khung vuông hoặc dọc, thêm `#Shorts` vào mô tả.
- **Phim nhiều tập:** giữ một "chuỗi nhận dạng" nhân vật (30–50 từ) dán nguyên văn vào mọi prompt; mỗi clip chỉ một chuyển động máy.
