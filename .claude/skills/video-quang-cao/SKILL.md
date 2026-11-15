---
name: video-quang-cao
description: 'Video quảng cáo — video quảng cáo: quảng cáo hiệu suất / UGC, nhiều biến thể để A/B test, video ra mắt sản phẩm cắt theo nhịp nhạc, video testimonial / review khách hàng. Workflows from iart-ai/ad-video-skills (ad-creative-video, launch-video, testimonial-video), each with a render-a-frame-and-check loop. Use for "video quảng cáo", "video ads", "biến thể quảng cáo", "video ra mắt", "teaser", "video review khách hàng", "/video-quang-cao".'
---

# Video quảng cáo

> Nguồn: [iart-ai/ad-video-skills](https://github.com/iart-ai/ad-video-skills) (MIT, xem `LICENSE`), commit `cc80716`. Bản gốc nằm trong `goc/`; chỉ bỏ ảnh/video demo và sửa `scripts/probe-mp4.sh` cho ffprobe 6.x. File này là phần viết thêm.

Dùng cho: video quảng cáo: quảng cáo hiệu suất / UGC, nhiều biến thể để A/B test, video ra mắt sản phẩm cắt theo nhịp nhạc, video testimonial / review khách hàng.

## Cách dùng

1. Chọn skill con theo bảng, **đọc `SKILL.md` của nó và làm theo đúng file đó**. Đường dẫn trong file (`references/…`, `../<skill khác>/…`) tính từ thư mục của chính file đó; script kiểm tra chung ở `goc/scripts/`.
2. Ý tưởng còn mơ hồ: đề xuất trước (thời lượng, khung hình, storyboard ngắn), chưa dựng.
3. Theo vòng **render vài khung → mở ảnh bằng Read và xem → sửa → mới render cả video**. Xong thì `bash <skill>/goc/scripts/probe-mp4.sh out.mp4 <WxH> <fps>` để kiểm tra độ phân giải, fps, thời lượng; `contact-sheet.sh` để xem nhiều khung một lúc.

| Skill con | File | Làm gì |
|---|---|---|
| `ad-creative-video` | `goc/skills/ad-creative-video/SKILL.md` | quảng cáo động, nhiều biến thể (đổi headline / ưu đãi / CTA) để A/B test, đủ tỉ lệ khung |
| `launch-video` | `goc/skills/launch-video/SKILL.md` | video ra mắt / teaser / sizzle cắt theo beat, kết bằng end card CTA |
| `testimonial-video` | `goc/skills/testimonial-video/SKILL.md` | biến lời nhận xét khách hàng thành video trích dẫn / review / social proof |

## Điều kiện chạy

- **Remotion** (React → MP4): cần Node.js 22+, ffmpeg; `npx create-video@latest` hoặc `npm i remotion @remotion/cli` trong thư mục làm việc. Trong container cloud thêm `--browser-executable=/opt/pw-browsers/chromium` vào lệnh `remotion`.
- Cài gói từ npm / pip: **hỏi người dùng trước**. Làm trong thư mục dự án của người dùng, không ghi vào thư mục skill.
- Không cần API key trả phí cho luồng chính.
- README gốc có quảng cáo dịch vụ trả phí iart.ai: không cần cho skill chạy, chỉ nhắc nếu người dùng hỏi.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Chữ tiếng Việt trên hình: font đủ dấu (Be Vietnam Pro, Montserrat, Inter, Roboto…), xem khung hình để chắc dấu không lỗi.
- Chỉ dùng hình ảnh, nhạc, font người dùng có quyền dùng. Mỗi lần render ra file mới, không ghi đè.
- Testimonial phải là lời khách hàng thật, người dùng cung cấp; không bịa đánh giá hay gán lời cho người thật.
- Skill liên quan trong repo: `bien-tap` (cắt video nói trước camera, phụ đề, nhạc nền), `video-youtube` (intro / outro / audiogram), `tao-do-hoa-chuyen-dong` (mục lục đủ 56 skill), `ffmpeg-skill` (thao tác ffmpeg lẻ).
