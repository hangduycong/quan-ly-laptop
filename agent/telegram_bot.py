"""
Bot Telegram: báo động tức thì + điều khiển nhanh bằng nút bấm.

Laptop tự hỏi Telegram có tin nhắn mới không (long polling), nên không cần server.
Chỉ những cuộc trò chuyện đã nhập đúng mã PIN mới điều khiển được.
"""
import asyncio
import base64
import datetime as dt
import logging
import time

import net
from common import save_config

log = logging.getLogger("telegram")

B_STATUS, B_SHOT, B_APPS, B_TODAY = "📊 Trạng thái", "📷 Chụp màn hình", "🗂 Ứng dụng", "⏱ Hôm nay"
B_LOCK, B_SLEEP, B_RESTART, B_OFF = "🔒 Khoá máy", "🌙 Cho ngủ", "🔄 Khởi động lại", "⏻ Tắt máy"
KEYBOARD = {"keyboard": [[B_STATUS, B_SHOT], [B_APPS, B_TODAY], [B_LOCK, B_SLEEP], [B_RESTART, B_OFF]],
            "resize_keyboard": True, "is_persistent": True}
HELP = ("Các nút bên dưới để điều khiển laptop.\n"
        "Lệnh gõ tay:\n"
        "/nhan <lời nhắn> — hiện lời nhắn lên màn hình laptop\n"
        "/tat <số phút> — hẹn giờ tắt máy\n"
        "/huy — huỷ hẹn tắt máy\n"
        "/mo <tên app hoặc trang web> — mở trên laptop\n"
        "Cài đặt hạn chế (YouTube, giới hạn giờ…) làm trên trang web quản lý.")
ICON = {"info": "🔔", "warn": "⚠️", "alert": "🚨"}


def dur(s) -> str:
    s = int(s or 0)
    h, m = divmod(s // 60, 60)
    return f"{h} giờ {m} phút" if h else (f"{m} phút" if m else f"{s} giây")


class TelegramBot:
    def __init__(self, agent):
        self.agent = agent
        c = agent.cfg["telegram"]
        self.token = c["token"].strip()
        self.pin = str(c.get("pin", "")).strip()
        self.chats: list[int] = [int(x) for x in c.get("chats", [])]
        self.base = f"https://api.telegram.org/bot{self.token}/"
        self.queue: asyncio.Queue = asyncio.Queue()
        self.denied: dict[int, float] = {}

    @staticmethod
    def configured(cfg) -> bool:
        return bool(cfg.get("telegram", {}).get("token"))

    # ------------------------------------------------------------ Telegram API
    async def api(self, method: str, timeout: float = 30, **params):
        r = await asyncio.to_thread(net.request, "POST", self.base + method, json_body=params, timeout=timeout)
        if not r or not r.get("ok"):
            raise RuntimeError(f"telegram {method}: {r}")
        return r["result"]

    async def send(self, chat: int, text: str, **kw):
        return await self.api("sendMessage", chat_id=chat, text=text[:4000], **kw)

    async def send_photo(self, chat: int, jpg: bytes, caption: str = ""):
        body, ctype = net.multipart({"chat_id": chat, "caption": caption[:1000]},
                                    {"photo": ("man-hinh.jpg", jpg, "image/jpeg")})
        await asyncio.to_thread(net.request, "POST", self.base + "sendPhoto", data=body,
                                headers={"Content-Type": ctype}, timeout=60)

    # ------------------------------------------------------------ dùng bởi core
    def on_event(self, ev: dict):
        if self.queue.qsize() < 200:
            self.queue.put_nowait(ev)

    async def run(self):
        await asyncio.gather(self.poller(), self.notifier())

    async def notifier(self):
        while True:
            ev = await self.queue.get()
            text = f"{ICON.get(ev['level'], '🔔')} {self.agent.cfg['device_name']}: {ev['msg']}"
            for chat in list(self.chats):
                while True:
                    try:
                        await self.send(chat, text)
                        break
                    except Exception as e:
                        log.info("notify failed: %s", e)
                        await asyncio.sleep(15)

    async def poller(self):
        offset = 0
        while True:
            try:
                updates = await self._get_updates(offset)
                for u in updates:
                    offset = max(offset, u["update_id"] + 1)
                    asyncio.create_task(self.safe(self.on_update(u)))
            except Exception as e:
                log.info("getUpdates: %s", e)
                await asyncio.sleep(10)

    async def _get_updates(self, offset: int):
        # "timeout" của Telegram (giây chờ tin mới) khác timeout của kết nối HTTP
        params = {"offset": offset, "timeout": 50, "allowed_updates": ["message", "callback_query"]}
        r = await asyncio.to_thread(net.request, "POST", self.base + "getUpdates", json_body=params, timeout=70)
        return r.get("result", []) if r else []

    async def safe(self, coro):
        try:
            await coro
        except Exception as e:
            log.exception("telegram handler: %s", e)

    # ------------------------------------------------------------ xử lý tin nhắn
    async def on_update(self, u: dict):
        if "callback_query" in u:
            return await self.on_callback(u["callback_query"])
        msg = u.get("message") or {}
        chat = msg.get("chat", {}).get("id")
        text = (msg.get("text") or "").strip()
        if chat is None:
            return
        if chat not in self.chats:
            return await self.pair(chat, text)
        await self.on_text(chat, text)

    async def pair(self, chat: int, text: str):
        if self.pin and text.split()[-1:] == [self.pin]:
            self.chats.append(chat)
            self.agent.cfg["telegram"]["chats"] = self.chats
            save_config(self.agent.cfg)
            self.agent.event("Có thêm một tài khoản Telegram vừa kết nối với bot")
            await self.send(chat, f"✅ Đã kết nối với {self.agent.cfg['device_name']}.\n\n{HELP}",
                            reply_markup=KEYBOARD)
        elif time.time() - self.denied.get(chat, 0) > 60:
            self.denied[chat] = time.time()
            await self.send(chat, "🔐 Đây là bot riêng. Hãy gửi mã PIN đã đặt khi cài phần mềm.")

    async def on_text(self, chat: int, text: str):
        cmd, _, rest = text.partition(" ")
        cmd = cmd.split("@")[0].lower()
        run = self.agent.run_cmd
        try:
            if text == B_STATUS or cmd == "/trangthai":
                await self.send(chat, self.fmt_status(await run("status", {})))
            elif text == B_SHOT or cmd == "/chup":
                r = await run("screenshot", {"max_w": 1920, "quality": 70})
                await self.send_photo(chat, base64.b64decode(r["img"]),
                                      "Màn hình lúc " + dt.datetime.now().strftime("%H:%M:%S"))
            elif text == B_APPS or cmd == "/ungdung":
                await self.send_apps(chat)
            elif text == B_TODAY or cmd == "/homnay":
                await self.send(chat, self.fmt_usage(await run("usage", {})))
            elif text == B_LOCK or cmd == "/khoa":
                await run("power", {"action": "lock"})
                await self.send(chat, "🔒 Đã khoá màn hình.")
            elif text == B_SLEEP:
                await self.ask_power(chat, "sleep", "Cho laptop ngủ?")
            elif text == B_RESTART:
                await self.ask_power(chat, "restart", "Khởi động lại laptop?")
            elif text == B_OFF:
                await self.ask_power(chat, "shutdown", "Tắt laptop?")
            elif cmd == "/tat":
                minutes = int(rest or 0)
                await run("power", {"action": "shutdown", "delay": minutes * 60})
                await self.send(chat, f"⏻ Laptop sẽ tắt sau {minutes} phút. Gõ /huy để huỷ.")
            elif cmd == "/huy":
                await run("power", {"action": "cancel"})
                await self.send(chat, "Đã huỷ hẹn tắt máy.")
            elif cmd == "/nhan" and rest:
                await run("message", {"text": rest})
                await self.send(chat, "✉️ Đã hiện lời nhắn lên laptop.")
            elif cmd == "/mo" and rest:
                await run("launch", {"target": rest})
                await self.send(chat, f"Đã mở {rest}.")
            else:
                await self.send(chat, HELP, reply_markup=KEYBOARD)
        except Exception as e:
            await self.send(chat, f"⚠️ Không làm được: {e}")

    async def ask_power(self, chat: int, action: str, question: str):
        if action == "sleep":
            rows = [[{"text": "Cho ngủ ngay", "callback_data": "p:sleep:0"}]]
        else:
            rows = [[{"text": "Ngay", "callback_data": f"p:{action}:0"},
                     {"text": "Sau 5 phút", "callback_data": f"p:{action}:300"},
                     {"text": "Sau 15 phút", "callback_data": f"p:{action}:900"}]]
        rows.append([{"text": "Thôi", "callback_data": "x"}])
        await self.send(chat, question, reply_markup={"inline_keyboard": rows})

    async def send_apps(self, chat: int):
        apps = await self.agent.run_cmd("apps", {})
        if not apps:
            return await self.send(chat, "Không có ứng dụng nào đang mở.")
        lines, rows = [], []
        for a in apps[:20]:
            lines.append(f"• {a['exe']} (hôm nay {dur(a['today'])})\n   " +
                         "\n   ".join(w[:70] for w in a["windows"][:3]))
            if len(a["exe"]) <= 60:
                rows.append([{"text": f"❌ Đóng {a['title']}", "callback_data": "k:" + a["exe"]}])
        await self.send(chat, "Ứng dụng đang mở:\n\n" + "\n".join(lines),
                        reply_markup={"inline_keyboard": rows[:20]})

    async def on_callback(self, q: dict):
        chat = q.get("message", {}).get("chat", {}).get("id")
        mid = q.get("message", {}).get("message_id")
        await self.api("answerCallbackQuery", callback_query_id=q["id"])
        if chat not in self.chats:
            return
        data = q.get("data", "")
        try:
            if data.startswith("p:"):
                _, action, delay = data.split(":")
                await self.agent.run_cmd("power", {"action": action, "delay": int(delay)})
                name = {"shutdown": "tắt", "restart": "khởi động lại", "sleep": "ngủ"}[action]
                text = f"✅ Laptop sẽ {name} " + (f"sau {int(delay) // 60} phút. Gõ /huy để huỷ."
                                                   if int(delay) else "ngay bây giờ.")
            elif data.startswith("k:"):
                r = await self.agent.run_cmd("kill", {"name": data[2:]})
                text = f"✅ Đã đóng {data[2:]} ({r['killed']} tiến trình)."
            else:
                text = "Đã huỷ."
        except Exception as e:
            text = f"⚠️ Không làm được: {e}"
        if data.startswith("k:"):
            await self.send(chat, text)
        else:
            await self.api("editMessageText", chat_id=chat, message_id=mid, text=text)

    # ------------------------------------------------------------ định dạng
    def fmt_status(self, s: dict) -> str:
        lines = [f"💻 {self.agent.cfg['device_name']} — đang bật",
                 f"👤 Người dùng: {s.get('user') or '(chưa đăng nhập Windows)'}"]
        if s.get("fg_app"):
            lines.append(f"🪟 Đang dùng: {s['fg_app']}\n    {s.get('fg_title', '')[:120]}")
        if s.get("idle") is not None:
            lines.append(f"⌨️ Không thao tác: {dur(s['idle'])}")
        lines.append(f"⏱ Hôm nay đã dùng: {dur(s.get('today_total'))}")
        lines.append("🔌 Bật máy lúc: " + dt.datetime.fromtimestamp(s["boot"]).strftime("%H:%M %d/%m"))
        if s.get("battery") is not None:
            lines.append(f"🔋 Pin: {s['battery']}%" + (" (đang sạc)" if s.get("plugged") else ""))
        if s.get("shutdown_at"):
            lines.append("⏻ Hẹn tắt lúc " + dt.datetime.fromtimestamp(s["shutdown_at"]).strftime("%H:%M"))
        return "\n".join(lines)

    @staticmethod
    def fmt_usage(d: dict) -> str:
        if not d["total"]:
            return "Hôm nay chưa dùng máy."
        lines = [f"⏱ Hôm nay đã dùng {dur(d['total'])} (khoảng {d['first']}h – {d['last'] + 1}h)", ""]
        lines += [f"• {a['exe']}: {dur(a['seconds'])}" for a in d["apps"][:10]]
        if d.get("videos"):
            lines += ["", "▶️ Video YouTube đã xem:"]
            lines += [f"• {v['title'][:80]} ({dur(v['seconds'])})" for v in d["videos"][:10]]
        return "\n".join(lines)
