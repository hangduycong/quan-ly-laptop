# Nhập skill từ một repo GitHub

Quy trình đã dùng để tạo các skill trong repo này (`bien-tap`, `ho-tro-tao-video`, `video-youtube`, các skill iart-ai, `tuan-thu-quy-trinh`…). Làm theo thứ tự; mỗi bước có lý do.

## 1. Tải về chỗ tạm và đọc trước

- `git clone --depth 1 <url>` vào thư mục tạm (scratchpad), **không** vào repo. Ghi lại commit (`git log -1 --format=%H`) để biết chính xác đã lấy bản nào.
- Đọc `README`, `LICENSE`, tìm mọi `SKILL.md` (`find . -name SKILL.md`). Repo có thể là: một skill; nhiều skill; **trang mục lục trỏ sang repo khác** (iart-ai/motion-skills); hay **cả một bộ công cụ** chạy từ thư mục gốc của nó (claude-code-video-toolkit) — mỗi loại đóng gói khác nhau (bước 3).
- Đọc code trước khi chạy (đặc biệt script tải về, gọi mạng, tốn tiền).

## 2. Giấy phép — quyết định có được chép không

| Giấy phép | Làm |
|---|---|
| MIT, Apache 2.0, BSD | Chép được; giữ `LICENSE` (Apache: giữ cả NOTICE nếu có) |
| CC BY 4.0 | Chép được, kể cả thương mại; **bắt buộc ghi công tác giả** ở đầu `SKILL.md` và trong `NOTICE.md`, ghi rõ đã đổi gì |
| CC BY-NC | Chép được nhưng **không dùng thương mại**; báo người dùng rõ |
| "Source-available", "All rights reserved", proprietary (vd. skill docx/pdf/pptx/xlsx trong anthropics/skills) | **Không chép**; báo người dùng |
| Không có file LICENSE | Mặc định là giữ mọi quyền: tìm tuyên bố giấy phép ở nơi khác của tác giả (README, repo mục lục) và ghi rõ căn cứ; không có thì hỏi người dùng |

## 3. Đóng gói

Cấu trúc chuẩn trong repo này:

```
.claude/skills/<ten-khong-dau>/
├── SKILL.md      cửa vào tiếng Việt (viết mới)
├── goc/          bản gốc, giữ nguyên cấu trúc thư mục
├── LICENSE       (hoặc LICENSE.txt) của bản gốc
└── NOTICE.md     nguồn, commit, giấy phép, đã bỏ gì, đã sửa gì, phần nào viết thêm
```

- **Giữ nguyên cấu trúc tương đối** trong `goc/` — các skill hay trỏ nhau bằng `../<skill khác>/…` hoặc `superpowers:<tên>`; đổi chỗ là gãy.
- Bỏ thứ không cần khi chạy: ảnh/GIF/video demo lớn, `.github/`, plugin manifest, tests, evals, website. Ghi lại trong `NOTICE.md`.
- Bộ công cụ quá lớn hoặc phải chạy từ gốc của nó: **không chép**; viết `scripts/cai-dat.sh` tải đúng commit đã ghi + cài phụ thuộc, và để hướng dẫn agent gốc trong `goc/`.
- Bộ nhiều skill: hoặc một skill cửa vào có bảng "tình huống → `goc/<tên>/SKILL.md`", hoặc mỗi gói thành một skill riêng (sinh bằng script cho đồng nhất).
- Hook / thay đổi cấu hình hệ thống mà bản gốc cài (SessionStart…): **không tự cài**; ghi hướng dẫn bật trong `SKILL.md`, chỉ làm khi người dùng yêu cầu.

## 4. Viết `SKILL.md` cửa vào

- `name` = tên thư mục, kebab-case không dấu (vd. "hỗ trợ tạo video" → `ho-tro-tao-video`).
- `description` ≤ 1024 ký tự, không chứa `<` `>`; mở đầu bằng tên tiếng Việt, nói việc cụ thể, cuối là `Use for "cụm từ tiếng Việt", "English", "/ten"`. **Đặt trong nháy đơn** `'...'` (nháy đơn bên trong viết `''`) — mô tả có `: ` mà không đặt trong nháy là YAML hỏng và skill không được nhận (đã gặp ở 12 skill, xem bài học).
- Thân: nguồn + giấy phép (1 dòng), dùng cho việc gì, bảng định tuyến tới file gốc, điều kiện chạy (công cụ, key trả phí → hỏi trước), quy ước tiếng Việt (giải thích tiếng Việt; prompt cho model AI thường tiếng Anh), ranh giới (người thật, bản quyền, chi tiền), liên kết skill liên quan trong repo.
- Mẫu: `mau/SKILL.mau.md`.

## 5. Kiểm tra

- `python3 <skill>/scripts/kiem_tra_skill.py .claude/skills/<ten>` — frontmatter theo đặc tả, `name` khớp thư mục, liên kết tương đối không gãy.
- Skill có code: chạy thử thật (cài vào thư mục tạm, render / chạy một ví dụ nhỏ, **xem kết quả** — mở ảnh bằng Read). Tải gói từ npm/pip hay chạy code vừa tải: hỏi người dùng; môi trường có thể chặn, khi đó ghi "chưa chạy thử" vào `SKILL.md`, không giả kết quả.
- Lỗi phát hiện khi chạy thử (vd. `probe-mp4.sh` hỏng với ffprobe 6.x): sửa trong `goc/`, ghi vào `NOTICE.md`.

## 6. Giao

- Commit trên nhánh làm việc, push; **tạo / merge pull request chỉ khi người dùng yêu cầu**.
- Báo người dùng: skill làm gì, cấu trúc, giấy phép (nhất là NC / bắt buộc ghi công), cần gì để chạy, đã kiểm tra gì và **chưa kiểm tra gì**.

## Bài học

- 12 skill từng có frontmatter hỏng vì mô tả chứa `: ` không đặt trong nháy → luôn kiểm tra bằng YAML parser, không chỉ nhìn bằng mắt.
- Script bản gốc có thể hỏng trên công cụ mới hơn (ffprobe 6.x in thêm dấu phẩy) → chạy thử mới thấy.
- Phụ đề / chữ tiếng Việt: luôn xem khung hình thật; font phải có bộ ký tự tiếng Việt.
