#!/usr/bin/env bash
# Tạo sting mẫu 3.5 s (whoosh 0–0.8 s, tiếng hit đúng 0.8 s, đuôi ngân) để thử intro.
# Dùng: make_sting.sh out.wav [impact_seconds=0.8]
# Đây chỉ là âm thanh giữ chỗ: thay bằng sting có bản quyền của kênh khi làm thật.
set -euo pipefail
out=${1:?out.wav}; hit=${2:-0.8}
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i "anoisesrc=d=3.5:c=pink:r=48000:a=0.5" \
  -f lavfi -i "sine=f=55:d=3.5:r=48000" \
  -f lavfi -i "anoisesrc=d=3.5:c=white:r=48000:a=0.8" \
  -filter_complex "\
[0:a]highpass=f=400,lowpass=f=6000,volume='if(lt(t,$hit),pow(t/$hit,3),0)':eval=frame,volume=0.5[w];\
[1:a]volume='if(gte(t,$hit),exp(-(t-$hit)*4),0)':eval=frame,volume=1.6[b];\
[2:a]highpass=f=3000,volume='if(gte(t,$hit),exp(-(t-$hit)*12),0)':eval=frame,volume=0.6[c];\
[w][b][c]amix=inputs=3:normalize=0,alimiter=limit=0.9,aformat=channel_layouts=stereo[out]" \
  -map "[out]" -t 3.5 -c:a pcm_s16le "$out"
echo "đã tạo $out (tiếng hit ở ${hit}s)"
