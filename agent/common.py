"""Phần dùng chung giữa core (chạy SYSTEM) và helper (chạy trong phiên người dùng)."""
import copy
import json
import os
import unicodedata
from pathlib import Path

# Thư mục cài đặt: C:\ProgramData\ParentControl (chỉ admin/SYSTEM được sửa)
BASE_DIR = Path(os.environ.get("PC_BASE_DIR", Path(__file__).resolve().parent))
DATA_DIR = BASE_DIR / "data"            # chỉ SYSTEM/Admin đọc được
CONFIG_FILE = DATA_DIR / "config.json"
IPC_TOKEN_FILE = BASE_DIR / "ipc_token.txt"
IPC_HOST = "127.0.0.1"
IPC_PORT = 47811

HELPER_TASK_NAME = "ParentControlHelper"

DEFAULT_CONFIG = {
    "device_id": "",
    "device_name": "",
    # Firebase: "tổng đài" cho web app trên GitHub Pages (bỏ trống nếu không dùng)
    "firebase": {"api_key": "", "database_url": "", "email": "", "password": ""},
    # Bot Telegram: báo động + điều khiển nhanh (bỏ trống nếu không dùng)
    "telegram": {"token": "", "pin": "", "chats": []},
    "show_notice_on_start": True,
    "idle_seconds": 120,          # không chạm chuột/phím quá lâu thì không tính giờ dùng
    "web": {
        "youtube_mode": "off",    # off | moderate | strict | block
        "keywords": [],
        "blocked_sites": [],
        "disable_incognito": False,
    },
    "limits": {},                 # {"chrome.exe": 120, "*": 240}  (phút / ngày)
    "bedtime": {"enabled": False, "start": "22:00", "end": "06:00", "action": "lock"},
    "quick_apps": [
        {"name": "Chrome", "target": "chrome"},
        {"name": "Edge", "target": "msedge"},
        {"name": "Word", "target": "winword"},
        {"name": "Máy tính", "target": "calc"},
    ],
}


def _merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict) and k not in ("limits",):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config() -> dict:
    data = {}
    if CONFIG_FILE.exists():
        data = json.loads(CONFIG_FILE.read_text("utf-8-sig"))
    return _merge(DEFAULT_CONFIG, data)


def save_config(cfg: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CONFIG_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), "utf-8")
    os.replace(tmp, CONFIG_FILE)


def norm(text: str) -> str:
    """Bỏ dấu tiếng Việt + chữ thường để so khớp từ khoá ('Kinh Dị' == 'kinh di')."""
    text = (text or "").replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return " ".join(text.casefold().split())


def send_json_line(writer, obj) -> None:
    writer.write((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
