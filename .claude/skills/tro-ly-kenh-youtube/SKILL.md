---
name: tro-ly-kenh-youtube
description: 'Trợ lý kênh YouTube — 11 focused YouTube creator tools with small checking scripts: channel audit, script with scored hooks (21 formulas), title + thumbnail packaging lint, description / tags SEO, chapters validated against YouTube rules, Shorts picked from a transcript, edit decision list for dead air and retakes, retention CSV diagnosis, weekly / monthly upload plan, comment replies in the creator voice, niche viral research. Use for "kịch bản YouTube", "câu mở đầu", "tiêu đề video", "chữ trên thumbnail", "mô tả và tag", "chapters / mốc thời gian", "cắt shorts từ transcript", "vì sao người xem bỏ đi", "lịch đăng video", "trả lời bình luận", "audit kênh", "/tro-ly-kenh-youtube".'
---

# Trợ lý kênh YouTube

> Nguồn: [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) (MIT, `LICENSE`, © 2026 Jake Schincariol), commit `a2feb21`. Bản gốc trong `goc/skills/<tên>/` và `goc/templates/` (giữ nguyên cấu trúc để các script gọi nhau). File này là phần viết thêm.

Mỗi việc là một skill nhỏ: **đọc `goc/skills/<tên>/SKILL.md` và làm theo đúng file đó**. Script đi kèm chỉ dùng thư viện chuẩn Python, xử lý file cục bộ (transcript `.srt` / `.vtt` / whisper `.json`, CSV retention xuất từ YouTube Studio).

| Người dùng muốn | Skill | Script |
|---|---|---|
| Kịch bản từ ý tưởng, câu mở đầu (hook) | `yt-script` | `hookscore.py`, `hooks.json` |
| Tiêu đề + chữ trên thumbnail (cặp), CTR thấp | `yt-package` | `title.py` |
| Mô tả, tag, giúp video được tìm thấy | `yt-seo` | — |
| Chapters / mốc thời gian | `yt-chapters` | `chapters.py` (đúng luật YouTube: bắt đầu 00:00, ≥ 3 mốc, mỗi mốc ≥ 10 s) |
| Tìm đoạn làm Shorts từ video dài | `yt-shorts` | — |
| Bỏ khoảng lặng, câu lặp, quay lại (danh sách cắt có mốc giờ) | `yt-edit` | `deadair.py` |
| Người xem bỏ đi ở đâu (file retention) | `yt-retention` | `retention.py` |
| Kế hoạch đăng theo tuần / tháng | `yt-plan` | — |
| Trả lời bình luận theo giọng của người dùng | `yt-comment` | — |
| Audit cả kênh | `yt-audit` | — |
| Cái gì đang viral trong lĩnh vực | `yt-viral` | `swipe.py` |

Giọng văn của người dùng: điền `goc/templates/voice.md` một lần (cách xưng hô, từ hay dùng, điều không bao giờ nói) — các skill viết lời / trả lời bình luận dùng nó.

## Tiếng Việt

- Viết kịch bản, tiêu đề, mô tả, trả lời bình luận **bằng tiếng Việt** khi kênh nói tiếng Việt; giữ giới hạn độ dài của skill gốc (tiêu đề YouTube bị cắt theo số ký tự hiển thị — đo lại với tiếng Việt có dấu).
- Script tách từ khóa theo chữ Latin không dấu (`[a-z']`): với transcript tiếng Việt, kết quả chọn ranh giới chapter dựa nhiều vào khoảng lặng hơn từ vựng — luôn đọc lại và đặt lại tên mốc.
- Bình luận: chỉ soạn nháp; **không tự đăng** trả lời lên kênh.

## Liên quan

`chien-luoc-kenh-youtube` (chiến lược, kiếm tiền, đối thủ, dữ liệu kênh qua API), `cat-video-dai-thanh-shorts` (render Shorts thật), `bien-tap` (dựng theo danh sách cắt), `video-youtube` (intro / outro).

## Trạng thái kiểm tra (15/11/2026)

Frontmatter và liên kết đã kiểm tra; đã đọc script (thư viện chuẩn, chỉ đọc file cục bộ, không gọi mạng). **Chưa chạy thử** script trong phiên tạo skill (môi trường chặn chạy code vừa tải về).
