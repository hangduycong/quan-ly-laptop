"""
Core agent — chạy dưới quyền SYSTEM (Task Scheduler, khởi động cùng Windows).

  * Nhận lệnh từ điện thoại qua Firebase (web app trên GitHub Pages) và bot Telegram.
  * Nhận "nhịp" mỗi giây từ helper (cửa sổ đang dùng, thời gian rảnh tay) để:
      - ghi thời gian sử dụng từng ứng dụng theo giờ
      - áp dụng giới hạn thời gian / giờ đi ngủ
      - đóng tab YouTube có tiêu đề chứa từ khoá cấm, ghi lịch sử video đã xem
  * Tắt/khởi động lại/ngủ máy, đóng ứng dụng, áp dụng chặn web.
  * Tự chạy lại helper nếu bị tắt, và báo cho phụ huynh.
"""
import asyncio
import ctypes
import datetime as dt
import json
import logging
import logging.handlers
import re
import secrets
import socket
import subprocess
import sys
import time

import psutil

import webfilter
from firebase_link import FirebaseLink
from telegram_bot import TelegramBot
from common import (DATA_DIR, HELPER_TASK_NAME, IPC_HOST, IPC_PORT, IPC_TOKEN_FILE,
                    load_config, norm, save_config, send_json_line)
from usage_db import UsageDB

IS_WIN = sys.platform == "win32"
NO_WINDOW = 0x08000000 if IS_WIN else 0
BROWSERS = {"chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe",
            "browser.exe", "vivaldi.exe", "coccoc.exe"}
PROTECTED = {"system", "smss.exe", "csrss.exe", "wininit.exe", "winlogon.exe", "services.exe",
             "lsass.exe", "svchost.exe", "dwm.exe", "explorer.exe", "python.exe", "pythonw.exe",
             "taskhostw.exe", "fontdrvhost.exe", "sihost.exe"}
YT_SUFFIX = re.compile(r"\s*-\s*YouTube.*$", re.I)

DATA_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.handlers.RotatingFileHandler(DATA_DIR / "core.log", maxBytes=2_000_000,
                                                                   backupCount=2, encoding="utf-8"),
                              logging.StreamHandler()])
log = logging.getLogger("core")


def today() -> str:
    return dt.date.today().strftime("%Y-%m-%d")


def exe_key(name: str) -> str:
    name = name.strip().lower()
    return name if name == "*" or "." in name else name + ".exe"


def in_window(now: dt.time, start: str, end: str) -> bool:
    s = dt.time.fromisoformat(start)
    e = dt.time.fromisoformat(end)
    return (s <= now < e) if s < e else (now >= s or now < e)


def minutes_until(now: dt.datetime, hhmm: str) -> float:
    t = dt.datetime.combine(now.date(), dt.time.fromisoformat(hhmm))
    if t < now:
        t += dt.timedelta(days=1)
    return (t - now).total_seconds() / 60


class Agent:
    def __init__(self):
        self.cfg = load_config()
        if not self.cfg.get("device_id"):
            self.cfg["device_id"] = re.sub(r"[^a-z0-9_-]", "-", socket.gethostname().lower())
        if not self.cfg.get("device_name"):
            self.cfg["device_name"] = socket.gethostname()
        self.db = UsageDB(DATA_DIR / "usage.sqlite")
        self.ipc_token = secrets.token_hex(24)
        IPC_TOKEN_FILE.write_text(self.ipc_token)

        self.helper_writer = None
        self.helper_user = ""
        self.helper_was_connected = False
        self.helper_pending: dict[str, asyncio.Future] = {}
        self.tick: dict = {}
        self.last_tick_ts = 0.0

        self.firebase = FirebaseLink(self) if FirebaseLink.configured(self.cfg) else None
        self.telegram = TelegramBot(self) if TelegramBot.configured(self.cfg) else None
        self.transports = [t for t in (self.firebase, self.telegram) if t]
        self.stream_until = 0.0
        self.stream_fps = 1.0
        self.shutdown_at = None

        # trạng thái để không báo/lặp lại liên tục
        self.flags: dict[str, float] = {}
        self.yt_last = ("", 0.0)

    # ================================================================ tiện ích
    def once(self, key: str, every: float) -> bool:
        """True nếu hành động `key` chưa làm trong `every` giây qua."""
        now = time.time()
        if now - self.flags.get(key, 0) >= every:
            self.flags[key] = now
            return True
        return False

    def event(self, msg: str, level: str = "info"):
        log.info("EVENT[%s] %s", level, msg)
        ev = {"level": level, "msg": msg, "ts": time.time()}
        for t in self.transports:
            t.on_event(ev)

    async def helper(self, op: str, timeout: float = 15, **args):
        if not self.helper_writer:
            raise RuntimeError("Chưa có ai đăng nhập Windows (hoặc helper chưa chạy)")
        rid = secrets.token_hex(6)
        fut = asyncio.get_running_loop().create_future()
        self.helper_pending[rid] = fut
        send_json_line(self.helper_writer, {"t": "req", "id": rid, "op": op, "args": args})
        await self.helper_writer.drain()
        try:
            return await asyncio.wait_for(fut, timeout)
        finally:
            self.helper_pending.pop(rid, None)

    async def notify_child(self, text: str):
        try:
            await self.helper("message", text=text, title="Thông báo")
        except Exception:
            pass

    async def notify_then_lock(self, text: str):
        await self.notify_child(text)
        await asyncio.sleep(3)
        try:
            await self.helper("lock")
        except Exception:
            pass

    def spawn(self, coro):
        """Chạy nền. Bắt buộc dùng trong on_tick: on_tick chạy trong vòng đọc của helper,
        nếu await trả lời của helper ở đây sẽ tự khoá chết."""
        task = asyncio.create_task(coro)
        task.add_done_callback(lambda t: t.cancelled() or t.exception() and log.warning("bg: %s", t.exception()))
        return task

    # ================================================================ IPC: helper
    async def on_helper(self, reader, writer):
        try:
            first = json.loads(await asyncio.wait_for(reader.readline(), 10))
            if first.get("t") != "auth" or first.get("token") != self.ipc_token:
                writer.close()
                return
        except Exception:
            writer.close()
            return
        if self.helper_writer:
            self.helper_writer.close()
        self.helper_writer, self.helper_user = writer, first.get("user", "")
        log.info("helper connected (user=%s)", self.helper_user)
        if not self.helper_was_connected:
            self.helper_was_connected = True
            if self.cfg.get("show_notice_on_start"):
                self.spawn(self.notify_child("Máy tính này được bố mẹ quản lý: thời gian sử dụng, ứng dụng "
                                             "và màn hình có thể được xem từ xa."))
        if self.once("login:" + self.helper_user, 1800):
            self.event(f"Tài khoản {self.helper_user} đang dùng máy")
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                m = json.loads(line)
                if m.get("t") == "tick":
                    await self.on_tick(m)
                elif m.get("t") == "rep":
                    fut = self.helper_pending.get(m.get("id"))
                    if fut and not fut.done():
                        if m.get("ok"):
                            fut.set_result(m.get("data"))
                        else:
                            fut.set_exception(RuntimeError(m.get("err", "lỗi helper")))
        except Exception as e:
            log.info("helper link error: %s", e)
        finally:
            if self.helper_writer is writer:
                self.helper_writer = None
                self.tick = {}
                log.info("helper disconnected")

    async def on_tick(self, t: dict):
        now = time.time()
        elapsed = min(now - self.last_tick_ts, 5) if self.last_tick_ts else 1
        self.last_tick_ts = now
        self.tick = t
        exe, title, idle = t.get("exe", ""), t.get("title", ""), float(t.get("idle", 0))
        if not exe or idle > self.cfg["idle_seconds"]:
            return
        self.db.add(exe, elapsed)

        # ---- lịch sử YouTube + từ khoá cấm
        if exe in BROWSERS and "youtube" in title.lower():
            video = YT_SUFFIX.sub("", title).strip()
            if video and video.lower() != "youtube":
                self.db.add_video(video, elapsed)
                kws = [norm(k) for k in self.cfg["web"].get("keywords", []) if norm(k)]
                hit = next((k for k in kws if k in norm(video)), None)
                if hit and self.once("yt_close", 3):
                    self.spawn(self.helper("close_tab", hwnd=t["hwnd"]))
                    if self.once("yt_msg:" + video, 60):
                        self.spawn(self.notify_child("Video này không được phép xem."))
                        self.event(f"Đã chặn video YouTube “{video}” (từ khoá: {hit})", "alert")

        # ---- giới hạn thời gian
        limits = {exe_key(k): v for k, v in self.cfg.get("limits", {}).items()}
        if not limits:
            return
        used = self.db.today_by_app()
        checks = []
        if exe in limits:
            checks.append((exe, used.get(exe, 0)))
        if "*" in limits:
            checks.append(("*", sum(used.values())))
        for key, secs in checks:
            limit = float(limits[key]) * 60
            label = "máy tính" if key == "*" else key
            left = limit - secs
            if 0 < left <= 300 and self.once(f"warn:{today()}:{key}", 86400):
                self.spawn(self.notify_child(f"Còn khoảng {max(1, round(left / 60))} phút sử dụng {label} hôm nay."))
            if left <= 0:
                if self.once(f"limit_evt:{today()}:{key}", 86400):
                    self.event(f"Đã hết giờ dùng {label} hôm nay ({limits[key]} phút)", "warn")
                if self.once("limit_act:" + key, 8):
                    if key == "*":
                        self.spawn(self.notify_then_lock("Hôm nay đã hết thời gian dùng máy."))
                    else:
                        self.kill_by_name(key)
                        if self.once("limit_msg:" + key, 60):
                            self.spawn(self.notify_child(f"Hôm nay đã hết thời gian dùng {key}."))

    # ================================================================ vòng lặp phụ
    async def maintenance_loop(self):
        last_apply = 0.0
        while True:
            await asyncio.sleep(20)
            try:
                self.db.flush()
                if time.time() - last_apply > 600:
                    last_apply = time.time()
                    await asyncio.to_thread(webfilter.apply, self.cfg["web"])
                await self.check_bedtime()
                await self.watchdog()
            except Exception:
                log.exception("maintenance")

    async def check_bedtime(self):
        b = self.cfg["bedtime"]
        if not b.get("enabled"):
            return
        now = dt.datetime.now()
        if not in_window(now.time(), b["start"], b["end"]):
            if 0 < minutes_until(now, b["start"]) <= 5 and self.once("bed_warn:" + today(), 86400):
                await self.notify_child("Còn 5 phút nữa là đến giờ đi ngủ. Hãy lưu bài và chuẩn bị tắt máy nhé!")
            return
        if not self.helper_writer:
            return
        if b["action"] == "shutdown":
            if self.once("bed_shutdown", 600):
                self.event("Đến giờ đi ngủ — máy sẽ tắt sau 2 phút", "warn")
                await self.notify_child("Đến giờ đi ngủ. Máy sẽ tự tắt sau 2 phút.")
                self.power("shutdown", 120)
        else:
            if self.tick.get("idle", 999) < 60 and self.once("bed_lock", 60):
                if self.once("bed_lock_evt:" + today(), 3600):
                    self.event("Đến giờ đi ngủ — đã khoá màn hình", "warn")
                await self.notify_then_lock("Đến giờ đi ngủ rồi!")

    async def watchdog(self):
        """Nếu có người đăng nhập mà helper không chạy -> chạy lại + báo phụ huynh."""
        if self.helper_writer or not IS_WIN:
            return
        logged_in = any(p.info["name"] and p.info["name"].lower() == "explorer.exe"
                        for p in psutil.process_iter(["name"]))
        if logged_in and self.once("helper_restart", 60):
            subprocess.run(["schtasks", "/run", "/tn", HELPER_TASK_NAME], capture_output=True,
                           creationflags=NO_WINDOW)
            if self.helper_was_connected and self.once("helper_tamper", 1800):
                self.event("Phần theo dõi trên laptop bị tắt — đã tự chạy lại", "alert")

    # ================================================================ hành động
    def kill_by_name(self, name: str) -> int:
        name = exe_key(name)
        if name in PROTECTED:
            raise RuntimeError(f"Không cho phép đóng tiến trình hệ thống {name}")
        n = 0
        for p in psutil.process_iter(["name"]):
            if (p.info["name"] or "").lower() == name:
                try:
                    p.kill()
                    n += 1
                except Exception:
                    pass
        return n

    def power(self, action: str, delay: int = 0):
        delay = max(0, min(int(delay or 0), 86400))
        if action in ("shutdown", "restart"):
            flag = "/s" if action == "shutdown" else "/r"
            subprocess.run(["shutdown", flag, "/f", "/t", str(max(delay, 5)), "/c",
                            "Máy tính sẽ " + ("tắt" if action == "shutdown" else "khởi động lại") +
                            " theo yêu cầu của bố mẹ."], capture_output=True, creationflags=NO_WINDOW)
            self.shutdown_at = time.time() + max(delay, 5)
        elif action == "cancel":
            subprocess.run(["shutdown", "/a"], capture_output=True, creationflags=NO_WINDOW)
            self.shutdown_at = None
        elif action == "sleep":
            ctypes.WinDLL("powrprof").SetSuspendState(False, False, False)
        else:
            raise RuntimeError("Lệnh nguồn không hợp lệ")

    def status(self) -> dict:
        t = self.tick
        bat = psutil.sensors_battery() if hasattr(psutil, "sensors_battery") else None
        if self.shutdown_at and self.shutdown_at < time.time():
            self.shutdown_at = None
        return {
            "helper": bool(self.helper_writer),
            "user": self.helper_user if self.helper_writer else "",
            "fg_app": t.get("exe", ""),
            "fg_title": t.get("title", ""),
            "idle": round(t["idle"]) if "idle" in t else None,
            "today_total": round(sum(self.db.today_by_app().values())),
            "boot": psutil.boot_time(),
            "battery": round(bat.percent) if bat else None,
            "plugged": bat.power_plugged if bat else None,
            "cpu": round(psutil.cpu_percent()),
            "ram": round(psutil.virtual_memory().percent),
            "shutdown_at": self.shutdown_at,
        }

    def public_settings(self) -> dict:
        return {k: self.cfg[k] for k in ("web", "limits", "bedtime", "quick_apps")}

    async def set_settings(self, a: dict) -> dict:
        web = a.get("web", {})
        mode = web.get("youtube_mode", "off")
        if mode not in ("off", "moderate", "strict", "block"):
            raise RuntimeError("Chế độ YouTube không hợp lệ")
        self.cfg["web"] = {
            "youtube_mode": mode,
            "keywords": [str(k).strip() for k in web.get("keywords", []) if str(k).strip()][:500],
            "blocked_sites": [webfilter.clean_site(str(s)) for s in web.get("blocked_sites", [])
                              if webfilter.clean_site(str(s))][:500],
            "disable_incognito": bool(web.get("disable_incognito")),
        }
        self.cfg["limits"] = {exe_key(k): max(0, int(v)) for k, v in (a.get("limits") or {}).items() if k.strip()}
        b = a.get("bedtime", {})
        dt.time.fromisoformat(b.get("start", "22:00"))
        dt.time.fromisoformat(b.get("end", "06:00"))
        self.cfg["bedtime"] = {"enabled": bool(b.get("enabled")), "start": b.get("start", "22:00"),
                               "end": b.get("end", "06:00"),
                               "action": "shutdown" if b.get("action") == "shutdown" else "lock"}
        self.cfg["quick_apps"] = [{"name": str(q["name"])[:40], "target": str(q["target"])[:500]}
                                  for q in (a.get("quick_apps") or []) if q.get("target")][:30]
        save_config(self.cfg)
        await asyncio.to_thread(webfilter.apply, self.cfg["web"])
        self.event("Đã cập nhật cài đặt hạn chế")
        return self.public_settings()

    async def apps(self) -> list:
        wins = await self.helper("windows")
        used = self.db.today_by_app()
        groups: dict[str, dict] = {}
        for w in wins:
            g = groups.setdefault(w["exe"], {"exe": w["exe"], "title": w["exe"].removesuffix(".exe"),
                                             "windows": [], "today": round(used.get(w["exe"], 0))})
            g["windows"].append(w["title"])
        return sorted(groups.values(), key=lambda g: -g["today"])

    # ================================================================ lệnh từ điện thoại
    async def run_cmd(self, cmd: str, a: dict):
        if cmd == "status":
            return self.status()
        if cmd == "apps":
            return await self.apps()
        if cmd == "kill":
            n = self.kill_by_name(str(a.get("name", "")))
            self.event(f"Phụ huynh đã đóng {a.get('name')} ({n} tiến trình)")
            return {"killed": n}
        if cmd == "launch":
            await self.helper("launch", target=str(a["target"]))
            return True
        if cmd == "message":
            await self.helper("message", text=str(a.get("text", ""))[:1000])
            return True
        if cmd == "power":
            action = a.get("action")
            if action == "lock":
                return await self.helper("lock")
            # trả lời trước rồi mới thực hiện, để điện thoại nhận được kết quả
            asyncio.get_running_loop().call_later(1, self.power, action, a.get("delay", 0))
            self.event(f"Lệnh nguồn: {action}" + (f" sau {int(a.get('delay', 0)) // 60} phút" if a.get("delay") else ""))
            return True
        if cmd == "screenshot":
            return await self.helper("screenshot", timeout=20, max_w=int(a.get("max_w", 1280)),
                                     quality=int(a.get("quality", 55)))
        if cmd == "stream":
            if a.get("on"):
                self.stream_fps = max(0.2, min(float(a.get("fps", 1)), 3))
                self.stream_until = time.time() + 300  # tự dừng sau 5 phút
                asyncio.create_task(self.stream_loop())
            else:
                self.stream_until = 0
            return True
        if cmd == "usage":
            d = self.db.day(str(a.get("date") or today()))
            d["videos"] = self.db.videos(d["date"])
            return d
        if cmd == "usage_days":
            return self.db.days(min(int(a.get("days", 7)), 60))
        if cmd == "get_settings":
            return self.public_settings()
        if cmd == "set_settings":
            return await self.set_settings(a)
        raise RuntimeError(f"Lệnh không hỗ trợ: {cmd}")

    async def stream_loop(self):
        if getattr(self, "_streaming", False):
            return
        self._streaming = True
        try:
            while time.time() < self.stream_until and self.firebase and self.firebase.connected:
                try:
                    r = await self.helper("screenshot", max_w=960, quality=45)
                    await self.firebase.send_frame(r["img"])
                except Exception as e:
                    log.info("stream: %s", e)
                    await asyncio.sleep(2)
                await asyncio.sleep(1 / self.stream_fps)
        finally:
            self._streaming = False

    # ================================================================
    async def main(self):
        try:
            await asyncio.to_thread(webfilter.apply, self.cfg["web"])
        except Exception:
            log.exception("webfilter apply")
        server = await asyncio.start_server(self.on_helper, IPC_HOST, IPC_PORT, limit=32 * 1024 * 1024)
        log.info("IPC listening on %s:%s", IPC_HOST, IPC_PORT)
        self.event("Laptop đã bật")
        async with server:
            await asyncio.gather(self.maintenance_loop(), *(t.run() for t in self.transports))


if __name__ == "__main__":
    _cfg = load_config()
    if not (FirebaseLink.configured(_cfg) or TelegramBot.configured(_cfg)):
        raise SystemExit("Chưa cấu hình Firebase hoặc Telegram trong data/config.json")
    asyncio.run(Agent().main())
