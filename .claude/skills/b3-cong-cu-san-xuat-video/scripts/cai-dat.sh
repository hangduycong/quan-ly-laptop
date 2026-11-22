#!/usr/bin/env bash
# Tải và cài claude-code-video-toolkit đúng phiên bản đã kiểm tra.
# Dùng: bash cai-dat.sh [thư mục]   (mặc định: $VIDEO_TOOLKIT_ROOT hoặc ~/claude-code-video-toolkit)
#       COMMIT=<sha> bash cai-dat.sh    để chọn phiên bản khác
# Không cài gì ngoài thư mục đó (Python deps nằm trong <thư mục>/.venv do uv tạo).
set -euo pipefail
COMMIT="${COMMIT:-01e85f4bbf5b3edffc7f8138406f3acc1dc43c66}"
ROOT="${1:-${VIDEO_TOOLKIT_ROOT:-$HOME/claude-code-video-toolkit}}"
URL=https://github.com/digitalsamba/claude-code-video-toolkit.git
command -v git >/dev/null || { echo "thiếu git"; exit 1; }
command -v node >/dev/null || echo "cảnh báo: chưa có Node.js (cần 22+ cho template Remotion)"
command -v ffmpeg >/dev/null || echo "cảnh báo: chưa có ffmpeg"
if [ -d "$ROOT/.git" ]; then
  echo "đã có bộ công cụ ở $ROOT — chuyển sang commit ${COMMIT:0:7}"
  git -C "$ROOT" fetch -q --depth 1 origin "$COMMIT"
else
  mkdir -p "$ROOT"
  git -C "$ROOT" init -q
  git -C "$ROOT" remote add origin "$URL"
  git -C "$ROOT" fetch -q --depth 1 origin "$COMMIT"
fi
git -C "$ROOT" -c advice.detachedHead=false checkout -q FETCH_HEAD
echo "bộ công cụ: $ROOT @ $(git -C "$ROOT" rev-parse --short HEAD)"
if command -v uv >/dev/null; then
  (cd "$ROOT" && uv sync -q) && echo "Python deps: đã cài (uv sync)"
else
  echo "chưa có uv — cài: curl -LsSf https://astral.sh/uv/install.sh | sh  (hỏi người dùng trước), rồi chạy lại"
fi
echo "tiếp theo: export VIDEO_TOOLKIT_ROOT=\"$ROOT\"; cd \"\$VIDEO_TOOLKIT_ROOT\" && uv run tools/verify_setup.py"
