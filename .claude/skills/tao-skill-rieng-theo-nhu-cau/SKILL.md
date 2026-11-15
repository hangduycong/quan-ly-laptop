---
name: tao-skill-rieng-theo-nhu-cau
description: 'Tạo skill riêng theo nhu cầu — create new Claude skills from scratch, turn a workflow from the conversation into a reusable skill, edit and improve existing skills, import a skill from a GitHub repo (license check, packaging, Vietnamese entry point), run evals and benchmarks against a baseline, and optimize a skill description so it triggers at the right time. Built on Anthropic skill-creator (Apache 2.0) plus this repo''s conventions and a validator for every skill. Use for "tạo skill", "làm skill mới", "biến quy trình này thành skill", "sửa skill", "skill không được gọi", "nhập skill từ GitHub", "kiểm tra skill", "/tao-skill-rieng-theo-nhu-cau".'
---

# Tạo skill riêng theo nhu cầu

> Dựa trên **skill-creator** của Anthropic ([anthropics/skills](https://github.com/anthropics/skills), Apache 2.0 — `LICENSE.txt`), commit `1780c5e` (14/11/2026), giữ nguyên trong `goc/skill-creator/`. Phần viết thêm: file này, `nhap-skill-tu-github.md`, `mau/SKILL.mau.md`, `scripts/kiem_tra_skill.py`.

Skill là một thư mục `.claude/skills/<tên>/` có `SKILL.md` (frontmatter `name` + `description`, rồi hướng dẫn), kèm tài liệu tham chiếu / script / mẫu nếu cần. Claude đọc `description` để quyết định khi nào mở skill.

## Chọn việc

| Người dùng muốn | Làm |
|---|---|
| Tạo skill mới (từ ý tưởng, hoặc "biến việc vừa làm thành skill") | Quy trình của `goc/skill-creator/SKILL.md`: nắm ý định → phỏng vấn & tìm hiểu → viết `SKILL.md` → test case → chạy & đánh giá → cải tiến. Mẫu tiếng Việt: `mau/SKILL.mau.md` |
| Nhập / chuyển một skill từ repo GitHub | `nhap-skill-tu-github.md` (giấy phép, đóng gói `goc/`, cửa vào tiếng Việt, kiểm tra, NOTICE) |
| Sửa / cải thiện skill có sẵn | đọc skill hiện tại → mục "Improving the skill" trong `goc/skill-creator/SKILL.md` |
| Skill không được gọi đúng lúc | mục "Description Optimization" trong `goc/skill-creator/SKILL.md`; kiểm tra trước là frontmatter có hợp lệ không |
| Kiểm tra một hoặc mọi skill | `python3 <skill này>/scripts/kiem_tra_skill.py .claude/skills[/<tên>]` |
| Đo skill có giúp ích không (có skill vs không) | mục "Running and evaluating test cases" + `goc/skill-creator/agents/` (grader, comparator, analyzer) + `eval-viewer/` |

Đọc `goc/skill-creator/SKILL.md` trước khi làm sâu; mọi đường dẫn `scripts/…`, `agents/…`, `references/…` trong đó tính từ `goc/skill-creator/`.

## Quy ước của repo này

- **Nơi đặt:** `.claude/skills/<ten-khong-dau>/` trong repo (dùng chung cho mọi phiên mở repo). `name` = tên thư mục, chữ thường không dấu, nối bằng gạch ngang, ≤ 64 ký tự.
- **Description:** ≤ 1024 ký tự, không có `<` `>`; mở đầu bằng tên tiếng Việt, nói rõ việc + kết quả, kết bằng các cụm từ người dùng hay nói (Việt và Anh) và `/ten-skill`. **Đặt trong nháy đơn** để YAML không hỏng khi có `: `. Viết hơi "chủ động" để skill không bị bỏ qua, nhưng đừng nhận cả những việc không phải của nó.
- **Thân SKILL.md:** tiếng Việt, ngắn (< 500 dòng); chi tiết đưa sang `references/` và trỏ tới rõ "khi nào đọc file nào". Giải thích **lý do** của quy tắc thay vì chỉ viết HOA "PHẢI".
- **An toàn:** việc tốn tiền (API trả phí, GPU cloud), đăng lên mạng, xóa dữ liệu, cài hook / đổi cấu hình hệ thống → skill phải dặn hỏi người dùng trước. Key không bao giờ in ra hay ghi vào repo.
- **Skill nhập từ ngoài:** bản gốc trong `goc/`, `LICENSE` + `NOTICE.md` đầy đủ (xem `nhap-skill-tu-github.md`).
- **Trước khi giao:** chạy `kiem_tra_skill.py` (phải "đạt"); skill có code thì chạy thử thật và xem kết quả; chưa chạy được thì ghi rõ trong skill. Commit + push lên nhánh làm việc; PR / merge chỉ khi người dùng yêu cầu.

## Về phần eval tự động của skill-creator

`goc/skill-creator/scripts/run_eval.py`, `run_loop.py`, `improve_description.py` gọi `claude -p` (Claude Code CLI) trong subprocess để chạy thử và tối ưu mô tả — tốn lượt dùng model và cần CLI `claude` trên máy. Hỏi người dùng trước khi chạy vòng lặp dài; không có CLI hoặc môi trường chặn thì làm thủ công: tự chạy vài câu hỏi mẫu có / không có skill và so sánh kết quả.

## Liên quan

`tuan-thu-quy-trinh` có skill `writing-skills` (viết skill theo hướng TDD: viết test áp lực trước, rồi mới viết skill) — dùng kèm khi skill là một quy trình kỷ luật.
