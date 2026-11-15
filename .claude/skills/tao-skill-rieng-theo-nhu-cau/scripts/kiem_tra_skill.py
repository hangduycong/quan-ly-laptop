#!/usr/bin/env python3
"""Kiểm tra skill: frontmatter đúng đặc tả (quick_validate của skill-creator) + mọi liên kết tương đối
trong các file .md trỏ tới file có thật + tên thư mục trùng `name`.
Liên kết hỏng trong README / CHANGELOG / CONTRIBUTING (thường trỏ tới demo, tài liệu repo gốc đã bỏ khi nhập)
chỉ là cảnh báo; trong SKILL.md và file tham chiếu là lỗi.

Dùng:
  python3 kiem_tra_skill.py .claude/skills/<tên>        một skill
  python3 kiem_tra_skill.py .claude/skills               mọi skill trong thư mục
Thoát mã 1 nếu có lỗi.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "goc/skill-creator/scripts"))
from quick_validate import validate_skill  # noqa: E402  (cần PyYAML)

import yaml  # noqa: E402

LINK = re.compile(r"\]\((?!https?:|mailto:|#)([^)\s#]+)(?:#[^)]*)?\)")


DOCS = {"readme.md", "changelog.md", "contributing.md", "code_of_conduct.md", "security.md"}


def check(skill: Path) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    ok, msg = validate_skill(skill)
    if not ok:
        errs.append(f"frontmatter: {msg}")
    else:
        fm = yaml.safe_load((skill / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1])
        if fm["name"] != skill.name:
            errs.append(f"tên thư mục '{skill.name}' khác name '{fm['name']}'")
    for md in skill.rglob("*.md"):
        if "node_modules" in md.parts:
            continue
        text = re.sub(r"(?ms)^(```|~~~).*?^\1", "", md.read_text(encoding="utf-8", errors="ignore"))  # bỏ khối code ví dụ
        for m in LINK.finditer(text):
            target = m.group(1)
            if "{" in target or "<" in target:
                continue  # placeholder trong mẫu
            if not (md.parent / target).exists():
                (warns if md.name.lower() in DOCS else errs).append(f"liên kết hỏng: {md.relative_to(skill)} → {target}")
    return errs, warns


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1])
    skills = [root] if (root / "SKILL.md").exists() else sorted(p.parent for p in root.glob("*/SKILL.md"))
    bad = 0
    for s in skills:
        errs, warns = check(s)
        print(f"{'OK ' if not errs else 'LỖI'} {s.name}" + (f"  ({len(warns)} cảnh báo trong README/tài liệu phụ)" if warns else ""))
        for e in errs[:20]:
            print(f"     - {e}")
        bad += bool(errs)
    print(f"{len(skills) - bad}/{len(skills)} skill đạt")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
