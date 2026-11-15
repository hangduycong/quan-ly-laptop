---
name: tuan-thu-quy-trinh
description: 'Tuân thủ quy trình — Superpowers (Jesse Vincent, MIT) disciplined development workflow, 15 process skills - brainstorming a design before building, writing plans, executing plans inline or with subagents, test-driven development (red-green-refactor), systematic debugging (root cause before fixes), verification before claiming done, requesting and receiving code review, git worktrees, finishing a branch, parallel agents, writing skills, diagnosing a session that went wrong. Use when starting a feature or any new build ("làm tính năng", "xây dựng", "thêm chức năng", "lên kế hoạch"), fixing a bug or failing test ("sửa lỗi", "debug", "test fail"), before saying work is done, around code review and merging, or when asked to "tuân thủ quy trình", "làm đúng quy trình", "TDD", "/tuan-thu-quy-trinh".'
---

# Tuân thủ quy trình (Superpowers)

> Nguồn: [obra/superpowers](https://github.com/obra/superpowers) (MIT, `LICENSE`, © 2025 Jesse Vincent), commit `22f0b46` (03/11/2026). 15 skill quy trình giữ nguyên trong `goc/<tên>/`; file này là cửa vào tiếng Việt. Hook SessionStart của bản gốc **không** được cài (xem cuối file).

Mục tiêu: làm việc **có kỷ luật** — nghĩ trước khi xây, viết test trước khi viết code, tìm nguyên nhân gốc trước khi sửa, có bằng chứng trước khi nói "xong".

## Quy tắc gọi skill

- Khi một file nhắc `superpowers:<tên>` (vd. `superpowers:test-driven-development`), **đọc `goc/<tên>/SKILL.md` và làm theo đúng**. Đường dẫn tương đối trong đó tính từ thư mục của chính file.
- **Trước khi hành động**, xem bảng dưới; có skill khớp thì đọc nó trước (kể cả trước khi hỏi lại hay đọc code). Báo một dòng: "Dùng <skill> để <mục đích>". Skill có checklist thì tạo todo cho từng mục.
- Skill quy trình đi trước skill chuyên môn: "làm X" → brainstorming trước; "sửa lỗi" → systematic-debugging trước.
- Hướng dẫn của người dùng (và CLAUDE.md của repo) **luôn đứng trên** skill. Câu hỏi đơn giản, tra cứu nhanh không cần cả quy trình — nhưng đừng tự bào chữa để bỏ qua khi việc thật sự khớp.
- Ghi chú riêng cho Claude Code: `goc/using-superpowers/references/claude-code-tools.md`. Toàn văn luật gốc: `goc/using-superpowers/SKILL.md`.

## Bản đồ quy trình

| Tình huống | Skill (`goc/<tên>/SKILL.md`) |
|---|---|
| Sắp xây bất cứ thứ gì mới: tính năng, thành phần, thay đổi hành vi, kế hoạch (cả ngoài phần mềm) | `brainstorming` — hỏi để ra thiết kế, người dùng duyệt từng phần trước khi làm |
| Đã có yêu cầu / thiết kế cho việc nhiều bước, chưa đụng code | `writing-plans` — kế hoạch từng bước nhỏ, mỗi bước có test và lệnh kiểm |
| Cần không gian làm việc tách biệt trước khi làm | `using-git-worktrees` |
| Thực thi kế hoạch, tự mình làm trong phiên | `executing-plans` |
| Thực thi kế hoạch, giao từng việc cho subagent + review hai lớp | `subagent-driven-development` |
| 2+ việc độc lập, không chung trạng thái | `dispatching-parallel-agents` |
| Viết bất kỳ code tính năng / sửa lỗi nào | `test-driven-development` — RED (test hỏng) → GREEN (code tối thiểu) → REFACTOR |
| Gặp lỗi, test hỏng, hành vi lạ | `systematic-debugging` — tìm nguyên nhân gốc trước, không đoán mò sửa |
| Sắp nói "xong / đã sửa / test pass", trước commit hay PR | `verification-before-completion` — chạy lệnh kiểm, đọc kết quả, rồi mới khẳng định |
| Xong việc lớn, trước merge | `requesting-code-review` |
| Nhận góp ý review | `receiving-code-review` — kiểm chứng kỹ thuật, không đồng ý cho có |
| Xong việc, test pass, quyết định merge / PR / giữ / bỏ nhánh | `finishing-a-development-branch` |
| Tạo / sửa / kiểm thử skill | `writing-skills` |
| Phiên làm việc trục trặc (lặp việc, bỏ kế hoạch, tốn kém) muốn biết vì sao | `diagnosing-superpowers` |

Luồng điển hình: **brainstorming → writing-plans → (worktree) → subagent-driven-development hoặc executing-plans [mỗi việc: TDD; gặp lỗi: systematic-debugging] → verification-before-completion → requesting-code-review → finishing-a-development-branch.**

## Điều chỉnh cho repo và người dùng này

- Trao đổi, câu hỏi brainstorm, kế hoạch, báo cáo: **tiếng Việt**; tên file, lệnh, code, commit message theo quy ước sẵn có của repo.
- **Subagent**: `subagent-driven-development` và `dispatching-parallel-agents` tạo nhiều agent, tốn tài nguyên hơn. Khi người dùng chưa chọn, hỏi một câu (làm trực tiếp với `executing-plans`, hay giao subagent) thay vì tự quyết.
- **Git**: chỉ commit, push, tạo hay merge PR khi người dùng yêu cầu hoặc quy trình được người dùng duyệt; không viết lại lịch sử nhánh của người khác; `finishing-a-development-branch` đưa lựa chọn cho người dùng chọn.
- `diagnosing-superpowers` đọc transcript phiên làm việc và có thể soạn issue GitHub: làm theo chính sách che dữ liệu (`references/redaction-policy.md`) và **không đăng issue khi người dùng chưa đồng ý**.
- `brainstorming` có "visual companion" chạy server cục bộ để xem bản phác: chỉ bật khi người dùng muốn.

## Hook tự động (tùy chọn, chưa cài)

Bản gốc dùng hook SessionStart để chèn `using-superpowers` vào đầu mọi phiên, buộc kiểm tra skill trước mọi phản hồi. Hook đó không có trong skill này. Nếu người dùng muốn hành vi "luôn bật", thêm hook SessionStart trong `.claude/settings.json` của repo (qua skill `update-config`) đọc `goc/using-superpowers/SKILL.md` — chỉ làm khi người dùng yêu cầu.
