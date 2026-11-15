#!/usr/bin/env python3
"""Create a bien-tap workspace: folders, system/config.json, CLAUDE.md, .gitignore.

Usage: python3 init.py [DIR]          (default: current directory)
Never overwrites an existing config.json or CLAUDE.md.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from common import SKILL_DIR, say

FOLDERS = ["raw video", "export edited video", "brand/music", "brand/sfx", "system/scripts",
           "system/looks", "system/motion", "system/videos"]

GITIGNORE = """# bien-tap: không commit video, bản render hay key
raw video/
export edited video/
system/keys.env
system/videos/*/renders/
system/videos/*/audio/
system/videos/*/frames/
system/videos/*/verify/
system/.trash/
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", nargs="?", default=".")
    args = ap.parse_args()
    ws = Path(args.dir).resolve()
    for f in FOLDERS:
        (ws / f).mkdir(parents=True, exist_ok=True)
    made = []
    cfg = ws / "system" / "config.json"
    if not cfg.exists():
        shutil.copy(SKILL_DIR / "templates" / "config.example.json", cfg)
        made.append("system/config.json")
    cl = ws / "CLAUDE.md"
    if not cl.exists():
        shutil.copy(SKILL_DIR / "templates" / "CLAUDE.template.md", cl)
        made.append("CLAUDE.md")
    brand = ws / "brand" / "BRAND.md"
    if not brand.exists():
        brand.write_text("# Brand\n\nMàu, font, logo, giọng văn. Điền cùng người dùng.\n", encoding="utf-8")
        made.append("brand/BRAND.md")
    gi = ws / ".gitignore"
    old = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if "bien-tap:" not in old:
        gi.write_text(old + ("\n" if old and not old.endswith("\n") else "") + GITIGNORE, encoding="utf-8")
        made.append(".gitignore (thêm mục bien-tap)")
    say(f"workspace: {ws}")
    say("đã tạo: " + (", ".join(made) if made else "không có gì mới (đã tồn tại)"))
    say("tiếp theo: người dùng tự tạo system/keys.env với dòng SPEECH_TO_TEXT_API_KEY=... "
        "(hoặc lưu key trong môi trường), rồi chạy doctor.py")


if __name__ == "__main__":
    main()
