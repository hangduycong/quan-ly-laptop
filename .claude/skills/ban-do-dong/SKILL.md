---
name: ban-do-dong
description: 'Bản đồ động — bản đồ động kiểu Vox: zoom vào khu vực, vẽ tuyến đường, tô sáng quốc gia / vùng, cắm ghim, lia bản đồ, Google Earth Studio. Workflows from iart-ai/map-animation-skills (map-animation), each with a render-a-frame-and-check loop. Use for "bản đồ động", "map animation", "vẽ đường đi trên bản đồ", "zoom bản đồ", "/ban-do-dong".'
---

# Bản đồ động

> Nguồn: [iart-ai/map-animation-skills](https://github.com/iart-ai/map-animation-skills) (MIT, xem `LICENSE`), commit `c8ef846`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: bản đồ động kiểu Vox: zoom vào khu vực, vẽ tuyến đường, tô sáng quốc gia / vùng, cắm ghim, lia bản đồ, Google Earth Studio.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `map-animation` | `goc/skills/map-animation/SKILL.md` | bản đồ động: zoom, tuyến đường, vùng tô sáng, ghim, lia |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Ranh giới và tên địa danh: dùng dữ liệu bản đồ người dùng chọn hoặc nguồn chính thống, hỏi khi có vùng tranh chấp; ghi nguồn dữ liệu bản đồ (OpenStreetMap, Natural Earth…) theo giấy phép của nguồn.
- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
