"""
Helper chạy trong phiên đăng nhập của người dùng (quyền thường).

Việc của helper: những thứ chỉ làm được bên trong phiên người dùng —
  * biết cửa sổ nào đang dùng, người dùng có đang thao tác không
  * chụp màn hình
  * hiện lời nhắn, mở ứng dụng (mở với quyền thường, không phải quyền admin)
  * đóng tab YouTube vi phạm (Ctrl+W), khoá màn hình
Mọi quyết định (giới hạn, ghi thời gian, gửi lên server) nằm ở core.py chạy dưới quyền SYSTEM.
Nếu helper bị tắt, core sẽ tự chạy lại và báo cho phụ huynh.
"""
import asyncio
import base64
import ctypes
import io
import json
import logging
import os
import sys
import threading
import time
from ctypes import wintypes
from pathlib import Path

import psutil

from common import IPC_HOST, IPC_PORT, IPC_TOKEN_FILE, send_json_line

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
dwmapi = ctypes.WinDLL("dwmapi")

LOG_DIR = Path(os.environ.get("LOCALAPPDATA", ".")) / "ParentControl"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=LOG_DIR / "helper.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("helper")

# ------------------------------------------------------------------ Win32
GW_OWNER = 4
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x80
DWMWA_CLOAKED = 14
VK_CONTROL = 0x11
KEYEVENTF_KEYUP = 0x2
MB_ICONINFORMATION = 0x40
MB_SYSTEMMODAL = 0x1000
MB_SETFOREGROUND = 0x10000
MB_TOPMOST = 0x40000

user32.GetForegroundWindow.restype = wintypes.HWND
user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.IsWindowVisible.argtypes = [wintypes.HWND]
user32.GetWindow.argtypes = [wintypes.HWND, wintypes.UINT]
user32.GetWindow.restype = wintypes.HWND
user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
user32.MessageBoxW.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]


def window_title(hwnd) -> str:
    n = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(hwnd, buf, n + 1)
    return buf.value


def window_pid(hwnd) -> int:
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


_name_cache: dict[int, str] = {}


def pid_name(pid: int) -> str:
    if pid in _name_cache:
        return _name_cache[pid]
    try:
        name = psutil.Process(pid).name().lower()
    except Exception:
        name = "unknown"
    if len(_name_cache) > 500:
        _name_cache.clear()
    _name_cache[pid] = name
    return name


def is_cloaked(hwnd) -> bool:
    val = ctypes.c_int(0)
    dwmapi.DwmGetWindowAttribute(hwnd, DWMWA_CLOAKED, ctypes.byref(val), ctypes.sizeof(val))
    return val.value != 0


def idle_seconds() -> float:
    lii = LASTINPUTINFO(ctypes.sizeof(LASTINPUTINFO), 0)
    user32.GetLastInputInfo(ctypes.byref(lii))
    return ((kernel32.GetTickCount() - lii.dwTime) & 0xFFFFFFFF) / 1000.0


def foreground() -> dict:
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return {"hwnd": 0, "pid": 0, "exe": "", "title": ""}
    pid = window_pid(hwnd)
    return {"hwnd": int(hwnd), "pid": pid, "exe": pid_name(pid), "title": window_title(hwnd)}


def list_windows() -> list[dict]:
    out = []

    def cb(hwnd, _):
        if (user32.IsWindowVisible(hwnd) and not user32.GetWindow(hwnd, GW_OWNER)
                and not (user32.GetWindowLongW(hwnd, GWL_EXSTYLE) & WS_EX_TOOLWINDOW)
                and not is_cloaked(hwnd)):
            title = window_title(hwnd)
            if title and title not in ("Program Manager",):
                pid = window_pid(hwnd)
                out.append({"pid": pid, "exe": pid_name(pid), "title": title})
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return out


def screenshot(max_w: int = 1280, quality: int = 55) -> str:
    import mss
    from PIL import Image
    with mss.mss() as sct:
        raw = sct.grab(sct.monitors[0])
        img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
    if img.width > max_w:
        img = img.resize((max_w, int(img.height * max_w / img.width)))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def message_box(text: str, title: str = "Tin nhắn từ bố mẹ"):
    threading.Thread(target=user32.MessageBoxW, daemon=True,
                     args=(None, text, title, MB_ICONINFORMATION | MB_SYSTEMMODAL | MB_SETFOREGROUND | MB_TOPMOST)
                     ).start()


def close_tab(hwnd: int) -> bool:
    """Gửi Ctrl+W vào cửa sổ trình duyệt nếu nó vẫn đang ở trên cùng."""
    if int(user32.GetForegroundWindow() or 0) != hwnd:
        return False
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(ord("W"), 0, 0, 0)
    user32.keybd_event(ord("W"), 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    return True


def launch(target: str):
    os.startfile(target)  # helper chạy quyền thường nên app mở ra cũng quyền thường


OPS = {
    "screenshot": lambda a: {"img": screenshot(int(a.get("max_w", 1280)), int(a.get("quality", 55)))},
    "windows": lambda a: list_windows(),
    "message": lambda a: message_box(str(a.get("text", "")), str(a.get("title", "Tin nhắn từ bố mẹ"))),
    "close_tab": lambda a: close_tab(int(a.get("hwnd", 0))),
    "launch": lambda a: launch(str(a["target"])),
    "lock": lambda a: bool(user32.LockWorkStation()),
}


# ------------------------------------------------------------------ IPC với core
async def session(reader, writer):
    token = IPC_TOKEN_FILE.read_text().strip()
    user = os.environ.get("USERNAME", "")
    send_json_line(writer, {"t": "auth", "token": token, "user": user, "pid": os.getpid()})
    await writer.drain()

    async def ticker():
        while True:
            fg = foreground()
            fg["idle"] = idle_seconds()
            send_json_line(writer, {"t": "tick", **fg})
            await writer.drain()
            await asyncio.sleep(1)

    async def handle(req):
        try:
            data = await asyncio.to_thread(OPS[req["op"]], req.get("args") or {})
            reply = {"t": "rep", "id": req["id"], "ok": True, "data": data}
        except Exception as e:
            log.exception("op %s failed", req.get("op"))
            reply = {"t": "rep", "id": req["id"], "ok": False, "err": str(e)}
        send_json_line(writer, reply)
        await writer.drain()

    tick_task = asyncio.create_task(ticker())
    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            req = json.loads(line)
            if req.get("t") == "req":
                asyncio.create_task(handle(req))
    finally:
        tick_task.cancel()


async def main():
    while True:
        try:
            reader, writer = await asyncio.open_connection(IPC_HOST, IPC_PORT, limit=32 * 1024 * 1024)
            log.info("connected to core")
            await session(reader, writer)
        except Exception as e:
            log.info("core not reachable: %s", e)
        await asyncio.sleep(5)


if __name__ == "__main__":
    # Chỉ một helper mỗi phiên đăng nhập
    kernel32.CreateMutexW(None, False, "Local\\ParentControlHelper")
    if ctypes.get_last_error() == 183:  # ERROR_ALREADY_EXISTS
        sys.exit(0)
    asyncio.run(main())
