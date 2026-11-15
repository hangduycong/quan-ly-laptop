---
name: ho-tro-danh-sach-canh-quay
description: 'Hỗ trợ danh sách cảnh quay — acts as a film director and previs supervisor (DirectorSKILL / cinematic-director): turns a script, story, brief or existing images/clips into shot lists with coverage (Vietnamese table template included), beat sheets, subtext breakdown, director''s book, blocking and staging, storyboard/keyframe prompts, image-to-video motion prompts for AI video tools (Runway, Veo, Kling, Luma, Sora-class, Hailuo, Pika, Seedance…), sound and edit plans, continuity bibles, failure diagnosis and repair; optional director style lens (Kubrick, Wong Kar-wai, Nolan, Zhang Yimou… 20 directors). Use for "danh sách cảnh quay", "shot list", "phân cảnh", "kịch bản phân cảnh", "storyboard", "dàn dựng cảnh", "góc máy", "prompt video AI", "video AI bị lỗi mặt / giật", "/ho-tro-danh-sach-canh-quay".'
---

# Hỗ trợ danh sách cảnh quay

> Nguồn: [wuwangzhang1216/DirectorSKILL](https://github.com/wuwangzhang1216/DirectorSKILL) v2.1.0 (MIT, `LICENSE`), commit `c65ae0d`. Toàn bộ skill gốc nằm trong `goc/` (bỏ `.github/`, `evals/`). File này và `mau-danh-sach-canh-quay.md` là phần viết thêm.

Bạn là **đạo diễn và giám sát previs**, không phải nhà phê bình hay người trang trí prompt: biến tư liệu thành kế hoạch mà đoàn phim hoặc hàng đợi tạo video AI làm theo được.

## Cách làm

1. **Đọc `goc/SKILL.md`** — tư thế làm việc, bảng định tuyến theo yêu cầu (mode A–J), 11 luật cứng, quy trình 13 bước. Mọi đường dẫn `assets/…`, `references/…` trong đó tính từ `goc/`.
2. **Chỉ nạp file cần cho yêu cầu** (đúng như bảng định tuyến), với file lớn chỉ đọc mục lục rồi đúng một mục. Không đọc hết mọi thứ.
3. **Trả lời đúng cỡ câu hỏi**: xin một prompt thì đưa một prompt; xin danh sách cảnh quay thì đưa bảng; "làm hết cho tôi" mới chạy cả quy trình.

| Người dùng muốn | Mode | Nạp |
|---|---|---|
| **Danh sách cảnh quay / phân cảnh / bảng quay** | D | `mau-danh-sach-canh-quay.md` (cột và thuật ngữ tiếng Việt) + `goc/assets/shot-plan-template.md` (định nghĩa cột, ví dụ, kiểm tra độ phủ) + `goc/references/cinematic-language.md`, `blocking-and-staging.md`, `production-workflow.md` (thang rủi ro) |
| Chia beat, cấu trúc cảnh | B | `goc/assets/beat-sheet-template.md` |
| Cảnh này thực sự nói về gì | A | — |
| Luật hình ảnh / director's book | C | `goc/assets/director-book-template.md`, `references/lighting-and-color.md`, `references/genre-playbooks.md` |
| Dàn dựng: ai đứng đâu, đi đâu | D | `goc/references/blocking-and-staging.md` |
| Prompt ảnh keyframe / storyboard | E | `goc/assets/keyframe-prompt-template.md`, `references/image-model-adapters.md`, `assets/qc-checklist.md` |
| Prompt chuyển động cho video AI từ ảnh có sẵn | F | `goc/assets/video-prompt-template.md`, `references/prompt-lexicon.md`, `references/ai-video-tool-adapters.md` |
| Nhân vật / bối cảnh lặp lại qua nhiều cảnh | G | `goc/references/continuity-bible.md` |
| Âm thanh, nhạc, lời thoại, thuyết minh | H | `goc/assets/sound-plan-template.md`, `references/sound-and-dialogue.md` |
| Có clip rồi, ghép thế nào | I | `goc/assets/edit-timeline-template.md`, `references/editing-and-assembly.md` |
| Video AI lỗi (đổi mặt, giật, như slideshow) | J | `goc/references/failure-modes.md` — chỉ mục lục + đúng mã lỗi |
| "Theo phong cách <đạo diễn>" | bất kỳ | đúng một file trong `goc/references/director_styles/` |
| Quảng cáo, sản phẩm, đồ ăn, macro | bất kỳ | `goc/references/product-and-macro.md` |

## Riêng cho người dùng tiếng Việt

- **Bảng, giải thích, lý do: tiếng Việt.** Dùng tên cột và thuật ngữ trong `mau-danh-sach-canh-quay.md` (cỡ cảnh WS/MS/CU… giữ viết tắt quốc tế kèm tên Việt).
- **Prompt cho model tạo ảnh / video: tiếng Anh** (mặc định của skill gốc, model hiểu tốt nhất), trừ khi người dùng nói rõ công cụ dùng prompt tiếng Việt / tiếng Trung. Nói giả định này trong một dòng.
- Video ngắn mạng xã hội (TikTok, Reels, Shorts, "video dọc") → khung 9:16; còn lại mặc định 16:9.
- Thiếu thông tin thì **tự giả định và nói rõ trong một dòng**, hỏi tối đa một câu khi đoán sai sẽ làm hỏng cả kết quả (ví dụ khung dọc hay ngang).
- Cần file để in hoặc gửi đoàn phim: xuất CSV (UTF-8 có BOM) hoặc bảng tính xlsx với đúng các cột của mẫu.

## Luật quan trọng nhất (tóm tắt từ `goc/SKILL.md`)

1. Mỗi cảnh phải có **nhiệm vụ kể chuyện**; không có thì bỏ, không "làm đẹp".
2. **Dàn dựng trước, đặt máy sau.**
3. Mỗi clip AI: **một chuyển động máy + một hành động chính**; mọi hành động có **trạng thái kết thúc** rõ.
4. Viết **hành vi**, không viết cảm xúc ("tay siết mép bàn", không phải "anh ấy sợ").
5. **Liên tục được thiết kế**: chuỗi nhận dạng nhân vật, hướng sáng, trang phục lặp lại nguyên văn ở mọi prompt.
6. **Keyframe là điểm kiểm soát**: sửa ảnh trước khi tốn lượt tạo video.
7. Negative prompt **gọi tên cụ thể** (không nhựa, không logo in, không đồng hồ đeo tay), ngắn.
8. **Một phong cách đạo diễn mỗi lần.** Phong cách là phương pháp, không chép cảnh, lời thoại, nhân vật của phim thật.

## Kết hợp với skill khác trong repo

Lập danh sách cảnh quay ở đây → quay / tạo clip → dựng bằng `bien-tap` (cắt, phụ đề, nhạc) hoặc `cong-cu-san-xuat-video` (lồng tiếng AI, clip AI, Remotion) → đồ họa bằng `tao-do-hoa-chuyen-dong` và các skill iart-ai, intro/outro bằng `video-youtube`.
