# Dựng bằng DaVinci Resolve Studio (tùy chọn — dùng khi đã mua)

Mặc định skill `b4-bien-tap` dựng bằng ffmpeg. Phần này chỉ dùng khi người dùng **đã mua DaVinci Resolve Studio** (bản miễn phí không cho điều khiển bằng script) và muốn bản dựng nằm trong Resolve để tự chỉnh tiếp. Resolve chạy trên **máy tính của người dùng**, nên các bước dưới đây phải chạy ở đó (không chạy trong container cloud).

## Chuẩn bị (một lần)

1. Resolve: Preferences → System → General → *External scripting using: Local*, khởi động lại Resolve.
2. Trong project của người dùng: các bin (mặc định `01_Footage`, `02_Audio`, `03_Graphics`, `04_Timelines`) và một **template timeline** (giữ chuỗi hiệu ứng track: xử lý giọng ở A1, nhạc ở A2). Ghi tên vào mục `davinci` của `system/config.json`.
3. Viết cùng người dùng script `system/scripts/resolve_build.py` theo `resolve-scripting.md`. Nó **đọc `cuts.json`** do `plan.py` tạo (cùng quyết định cắt với bản ffmpeg), nên mọi bước ingest / keep.json / plan giữ nguyên.

## Quy trình khi dựng trong Resolve

Bước 1–4 như SKILL.md (doctor, ingest, keep.json, plan). Thay bước "Dựng" bằng:

1. footage vào bin footage;
2. copy template timeline vào bin timelines thành "<video> - Transcript cut" (v2, v3… không ghi đè) rồi làm rỗng bản copy (giữ chuỗi FX của track);
3. khung tùy chỉnh nếu được yêu cầu (vd. 4:3 2880x2160, footage *scale to fill with crop* = `scaleToCrop`);
4. đặt các đoạn của `cuts.json` lên V1/A1 (`AppendToTimeline`, endFrame **exclusive**), zoom theo cột `zoom`, tô xanh lá các đoạn B-roll;
5. grade (chỉ footage log);
6. marker từ `cuts.json.markers` (hồng: ghi chú cho editor);
7. **âm thanh cuối cùng**: Normalize Audio Level trên A1 (ITU-R BS.1770-4, −2 dBTP, −16 LKFS, Independent).

Phụ đề: `captions.py <v> --resolve` (cue đầu bắt đầu ở 00:00:00,000 vì Resolve dời mọi thứ theo cue đầu), người dùng import bằng File → Import → Subtitle. Nhạc: `score.py` tạo `music/bed_vN.wav` / `sfx_vN.wav` → đặt lên A2 / A3. Xuất: `youtube-export-resolve.md`.

**Luôn đọc lại timeline từ Resolve trước bước tiếp theo** (người dùng hay tự sửa tay: cắt, xóa clip) và không bao giờ đặt lại thứ họ đã xóa.

## Tài liệu

- `resolve-scripting.md` — API Resolve: cái chạy được, cái âm thầm thất bại, cái làm Resolve crash (Resolve 21).
- `youtube-export-resolve.md` — thiết lập trang Deliver cho YouTube.
- Mục `davinci` trong `templates/config.example.json` — tên template, bin, track, thông số normalize.
