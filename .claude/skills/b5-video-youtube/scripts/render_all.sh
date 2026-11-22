#!/usr/bin/env bash
# Render intro + outro cho mọi file brands/*.json (chạy trong thư mục project Remotion).
# Mỗi file brands/<tên>.json có cùng dạng với brand.json. Kết quả: out/<tên>-intro.mp4, out/<tên>-outro.mp4
set -euo pipefail
mkdir -p out
for f in brands/*.json; do
  n=$(basename "$f" .json)
  npx remotion render Intro "out/${n}-intro.mp4" --props="$f"
  npx remotion render Outro "out/${n}-outro.mp4" --props="$f"
done
