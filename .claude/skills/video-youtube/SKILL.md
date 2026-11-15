---
name: video-youtube
description: Video YouTube — branded channel intros (3-5 s logo sting synced to the audio hit), outros / end screens (20 s plate that leaves YouTube's subscribe and next-video zones empty), reusable brand templates for many channels, and audiograms (podcast or voiceover clip → captioned waveform video in 16:9, 1:1, 9:16). Ships a ready Remotion project (Vietnamese font) plus helpers to find a sting's impact frame, make a placeholder sting, convert SRT captions and batch-render. Use for "intro YouTube", "outro", "end screen", "màn hình kết thúc", "logo sting", "audiogram", "video podcast", "sóng âm", "/video-youtube".
---

# Video YouTube: intro, outro, audiogram

> Học và đóng gói từ [iart-ai/youtube-video-skills](https://github.com/iart-ai/youtube-video-skills) (MIT, xem `LICENSE`; commit `7838388`). Bản gốc nằm nguyên trong `goc/` (chỉ sửa lỗi `probe-mp4.sh` với ffprobe 6.x). Phần viết thêm: file này, project chạy được `template/`, các script trong `scripts/`.

## Ba việc skill này làm

| Người dùng muốn | Làm | Đọc thêm |
|---|---|---|
| Intro kênh / logo sting / bumper | composition `Intro` | `goc/skills/youtube-intro-outro/SKILL.md`, `references/intro-outro.md` |
| Outro / end screen / thẻ "đăng ký + video kế tiếp" | composition `Outro` | như trên, mục end-screen |
| Đoạn podcast / giọng đọc thành video có sóng âm + phụ đề | `Audiogram`, `AudiogramSquare`, `AudiogramVertical` | `goc/skills/audiogram/SKILL.md`, `references/waveform-render.md` |

## Luật cứng (của nền tảng, không phải sở thích)

1. **Intro 3–5 giây, logo đọc được trong 2 giây.** Dài hơn 5 giây thì người xem bỏ đi, ảnh hưởng thuật toán.
2. **Logo bật lên ĐÚNG khung có tiếng "hit" của sting**, không lệch một khung. Tìm khung đó bằng `scripts/find_impact.py`.
3. **Outro giữ ≥ 20 giây, video tổng ≥ 25 giây.** YouTube chỉ cho đặt phần tử end screen trong 5–20 giây cuối, và chỉ với video ≥ 25 giây.
4. **Bố cục outro 16:9:** thương hiệu (logo, tên kênh, lời kêu gọi) chỉ ở **1/3 bên trái**; **2/3 bên phải để trống** cho YouTube vẽ thẻ video 615×345 và nút đăng ký 294×294; tránh góc và ~12% dưới cùng (thanh tiến trình trên điện thoại). Bố cục tốt nhất: **1 thẻ video + 1 nút đăng ký**.
5. **Shorts (9:16) không có end screen:** dùng end card 2–3 giây với nút "Đăng ký" vẽ sẵn + lời kêu gọi; tránh 10% trên và 18% dưới (giao diện Shorts).
6. **Audiogram:** chiều cao sóng/cột là hàm của khung hình (giải mã file một lần), **không** dùng analyser thời gian thực; clip ≤ 90 giây; luôn có phụ đề (đa số xem không bật tiếng); có thanh tiến trình; âm thanh thật được ghép vào video.
7. Mọi chữ, màu, logo, âm thanh lấy từ props (`brand.json`, `audiogram.json`) — một mẫu, nhiều kênh.

## Quy trình

Cần Node.js 22+, ffmpeg, Python 3. **Hỏi người dùng trước khi `npm install`** (tải Remotion ~250 gói).

1. Copy `template/` ra thư mục làm việc của người dùng (không làm trong thư mục skill), `npm install`.
2. Bỏ logo (SVG/PNG) và sting vào `public/`; sửa `brand.json` (tên kênh, khẩu hiệu, màu, lời kêu gọi). Chưa có sting: `bash <skill>/scripts/make_sting.sh public/sting.wav` (âm thanh giữ chỗ — thay bằng sting có bản quyền khi làm thật).
3. `python3 <skill>/scripts/find_impact.py public/sting.wav --props brand.json` → ghi `impact` (giây) vào props.
4. **Render ảnh trước, xem rồi mới render video** (mở PNG bằng Read):
   - Intro: `npx remotion still Intro out/i-impact.png --frame=<impact×30> --props=./brand.json` (logo đủ cỡ + chớp trắng), thêm một khung trước (windup) và sau (settle).
   - Outro: `--props` với `"showGuides": true` để thấy vùng YouTube; kiểm tra thương hiệu chỉ ở 1/3 trái.
   - Audiogram: một khung đang có tiếng nói (cột phải nhảy) và một khung có phụ đề.
5. `npx remotion render Intro out/intro.mp4 --props=./brand.json` (tương tự `Outro`, `Audiogram…` với `audiogram.json`). Bản giao: `showGuides: false`.
6. Kiểm tra: `bash <skill>/goc/scripts/probe-mp4.sh out/intro.mp4 1920x1080 30` (và `1080x1920` cho dọc); intro ≤ 5 s, outro ≥ 20 s, có track âm thanh.
7. Nhiều kênh: mỗi kênh một `brands/<tên>.json`, chạy `bash <skill>/scripts/render_all.sh` trong project.

Trong môi trường không có Chrome mặc định, thêm `--browser-executable=<đường dẫn chromium>` vào lệnh `remotion` (container cloud này: `/opt/pw-browsers/chromium`).

## Audiogram: chuẩn bị âm thanh và phụ đề

- Cắt đoạn ≤ 90 s: `ffmpeg -ss <bắt đầu> -t <dài> -i tap.mp3 -ac 2 -ar 48000 public/clip.wav`; đặt `durationInSeconds` trong `audiogram.json`.
- Phụ đề: tạo SRT sạch bằng skill `bien-tap` (`captions.py`) hoặc `chinh-sua-video`, rồi `python3 <skill>/scripts/srt_to_json.py captions.srt --offset -<giây bắt đầu> --into audiogram.json`.
- `"look": "bars"` (cột equalizer, hợp nhạc) hoặc `"wave"` (sóng mảnh, hợp giọng nói).

## Đã chạy thử (Remotion 4.0.543, 15/11/2026)

`tsc` không lỗi; `Intro` 3,52 s, `Outro` 20,00 s, `AudiogramVertical` 10,01 s — đều 30 fps, H.264 + AAC, `probe-mp4.sh` đạt; chữ tiếng Việt (Be Vietnam Pro) đủ dấu; cột sóng âm nhảy theo giọng nói. Outro 20 s render mất ~2 phút do hiệu ứng blur lớn.

## Ghi nhớ

- Trả lời tiếng Việt, giữ nguyên lệnh và tên file. Mỗi lần render ra file mới, không ghi đè.
- Không dùng nhạc/sting không có bản quyền cho bản đăng thật; hỏi người dùng nguồn âm thanh.
- Dựng phần thân video (cắt, phụ đề, nhạc) bằng `bien-tap`; ghép intro/outro vào đầu/cuối bằng `ffmpeg-skill` (`join.py`) hoặc concat ffmpeg cùng độ phân giải và fps.
