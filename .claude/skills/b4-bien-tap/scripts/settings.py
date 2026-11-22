#!/usr/bin/env python3
"""Per-video overrides on top of system/config.json.

Usage:
  python3 settings.py <video> show
  python3 settings.py <video> set cut.max_pause=0.5 cut.pause_keep=0.3
  python3 settings.py <video> unset cut.max_pause
Values are parsed as JSON when possible (numbers, true/false, null, lists), else kept as text.
"""
from __future__ import annotations

import argparse
import json

from common import find_workspace, load_config, read_json, say, video_dir, workspace_arg, write_json


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("action", choices=["show", "set", "unset"])
    ap.add_argument("items", nargs="*")
    workspace_arg(ap)
    a = ap.parse_args()
    ws = find_workspace(a.workspace)
    path = video_dir(ws, a.video) / "settings.json"
    data = read_json(path, {})
    if a.action == "set":
        for item in a.items:
            key, _, raw = item.partition("=")
            try:
                val = json.loads(raw)
            except json.JSONDecodeError:
                val = raw
            node = data
            parts = key.split(".")
            for p in parts[:-1]:
                node = node.setdefault(p, {})
            node[parts[-1]] = val
        write_json(path, data)
    elif a.action == "unset":
        for key in a.items:
            node, parts = data, key.split(".")
            for p in parts[:-1]:
                node = node.get(p, {})
            node.pop(parts[-1], None)
        write_json(path, data)
    say("ghi đè của video: " + json.dumps(data, ensure_ascii=False))
    cfg = load_config(ws, a.video)
    say("cut hiệu lực: " + json.dumps(cfg["cut"], ensure_ascii=False))


if __name__ == "__main__":
    main()
