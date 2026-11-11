"""
Kết nối Firebase Realtime Database (thay cho server riêng).

Cấu trúc dữ liệu:
  devices/<dev>      {name, last_seen, status}         laptop cập nhật mỗi 30 giây
  cmds/<dev>/<id>    {cmd, args, ts}                   web app gửi lệnh (args là chuỗi JSON)
  results/<dev>/<id> {ok, json | err, ts}              laptop trả kết quả (json là chuỗi JSON)
  frames/<dev>       {img, ts}                         ảnh màn hình khi "xem trực tiếp"
  events/<id>        {dev, name, level, msg, ts}       thông báo

Dùng REST API + luồng sự kiện (Server-Sent Events) nên chỉ cần thư viện chuẩn của Python.
"""
import asyncio
import json
import logging
import threading
import time
from collections import deque

import net

log = logging.getLogger("firebase")
SERVER_TS = {".sv": "timestamp"}
STALE_MS = 120_000  # lệnh cũ hơn 2 phút thì bỏ (vd. lệnh tắt máy gửi lúc laptop đang tắt)


class FirebaseLink:
    def __init__(self, agent):
        self.agent = agent
        c = agent.cfg["firebase"]
        self.api_key = c["api_key"].strip()
        self.db = c["database_url"].strip().rstrip("/")
        self.email, self.password = c["email"].strip(), c["password"]
        self.dev = agent.cfg["device_id"]
        self.id_token = self.refresh_token = None
        self.expires = 0.0
        self.events: deque = deque(maxlen=300)
        self.signal = asyncio.Event()
        self.seen: set[str] = set()
        self.connected = False

    @staticmethod
    def configured(cfg) -> bool:
        c = cfg.get("firebase", {})
        return all(c.get(k) for k in ("api_key", "database_url", "email", "password"))

    # ------------------------------------------------------------ đăng nhập
    def _login(self):
        if self.refresh_token:
            try:
                r = net.request("POST", f"https://securetoken.googleapis.com/v1/token?key={self.api_key}",
                                data=f"grant_type=refresh_token&refresh_token={self.refresh_token}".encode(),
                                headers={"Content-Type": "application/x-www-form-urlencoded"})
                self.id_token, self.refresh_token = r["id_token"], r["refresh_token"]
                self.expires = time.time() + int(r["expires_in"])
                return
            except Exception as e:
                log.info("refresh failed (%s), signing in again", e)
        r = net.request("POST", "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
                                f"?key={self.api_key}",
                        json_body={"email": self.email, "password": self.password, "returnSecureToken": True})
        self.id_token, self.refresh_token = r["idToken"], r["refreshToken"]
        self.expires = time.time() + int(r["expiresIn"])

    async def token(self) -> str:
        if not self.id_token or time.time() > self.expires - 300:
            await asyncio.to_thread(self._login)
        return self.id_token

    async def call(self, method: str, path: str, body=None):
        url = f"{self.db}/{path}.json?auth={await self.token()}"
        return await asyncio.to_thread(net.request, method, url, json_body=body)

    # ------------------------------------------------------------ dùng bởi core
    def on_event(self, ev: dict):
        self.events.append(ev)
        self.signal.set()

    async def send_frame(self, img_b64: str):
        await self.call("PUT", f"frames/{self.dev}", {"img": img_b64, "ts": SERVER_TS})

    # ------------------------------------------------------------ vòng chính
    async def run(self):
        backoff = 3
        while True:
            tasks = []
            try:
                await self.token()
                await self.publish_status()
                self.connected = True
                backoff = 3
                log.info("firebase connected as %s", self.email)
                tasks = [asyncio.create_task(c) for c in (self.listen(), self.heartbeat(), self.event_sender())]
                done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
                for t in done:
                    t.result()
            except Exception as e:
                log.info("firebase: %s", e)
            finally:
                self.connected = False
                for t in tasks:
                    t.cancel()
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 120)

    async def publish_status(self):
        await self.call("PATCH", f"devices/{self.dev}", {
            "name": self.agent.cfg["device_name"], "last_seen": SERVER_TS, "status": self.agent.status()})

    async def heartbeat(self):
        while True:
            await asyncio.sleep(30)
            await self.publish_status()

    async def event_sender(self):
        while True:
            while self.events:
                ev = self.events[0]
                await self.call("POST", "events", {"dev": self.dev, "name": self.agent.cfg["device_name"],
                                                   "level": ev["level"], "msg": ev["msg"], "ts": SERVER_TS})
                self.events.popleft()
            self.signal.clear()
            await self.signal.wait()

    async def listen(self):
        loop = asyncio.get_running_loop()
        q: asyncio.Queue = asyncio.Queue()
        stop = threading.Event()
        url = f"{self.db}/cmds/{self.dev}.json?auth={await self.token()}"

        def reader():
            try:
                for item in net.sse_lines(url):
                    if stop.is_set():
                        return
                    loop.call_soon_threadsafe(q.put_nowait, item)
                loop.call_soon_threadsafe(q.put_nowait, ("error", "stream closed"))
            except Exception as e:
                if not stop.is_set():
                    loop.call_soon_threadsafe(q.put_nowait, ("error", str(e)))

        threading.Thread(target=reader, daemon=True).start()
        try:
            while True:
                ev, data = await q.get()
                if ev in ("error", "cancel", "auth_revoked"):
                    raise RuntimeError(f"stream {ev}: {data}")
                if ev not in ("put", "patch"):
                    continue  # keep-alive
                d = json.loads(data)
                path, val = d.get("path", "/"), d.get("data")
                if path == "/":
                    for k, v in (val or {}).items():
                        self.dispatch(k, v)
                else:
                    key = path.strip("/")
                    if "/" not in key and isinstance(val, dict):
                        self.dispatch(key, val)
        finally:
            stop.set()

    def dispatch(self, key: str, cmd: dict):
        if key in self.seen or not isinstance(cmd, dict):
            return
        self.seen.add(key)
        if len(self.seen) > 2000:
            self.seen = set(list(self.seen)[-500:])
        asyncio.create_task(self.handle(key, cmd))

    async def handle(self, key: str, cmd: dict):
        ts = cmd.get("ts")
        try:
            if not isinstance(ts, (int, float)) or abs(time.time() * 1000 - ts) > STALE_MS:
                raise RuntimeError("Lệnh đã quá hạn (gửi lúc laptop chưa kết nối) nên không thực hiện")
            args = cmd.get("args") or {}
            if isinstance(args, str):  # web gửi args dạng chuỗi JSON (khoá như "chrome.exe" không hợp lệ trong Firebase)
                args = json.loads(args or "{}")
            data = await self.agent.run_cmd(str(cmd.get("cmd", "")), args)
            res = {"ok": True, "json": json.dumps(data, ensure_ascii=False)}
        except Exception as e:
            log.info("cmd %s failed: %s", cmd.get("cmd"), e)
            res = {"ok": False, "err": str(e)}
        res["ts"] = SERVER_TS
        try:
            await self.call("PUT", f"results/{self.dev}/{key}", res)
            await self.call("DELETE", f"cmds/{self.dev}/{key}")
        except Exception as e:
            log.info("reply failed: %s", e)
