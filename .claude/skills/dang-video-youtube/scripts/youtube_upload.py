#!/usr/bin/env python3
"""Đăng video lên YouTube bằng YouTube Data API v3 + OAuth 2.0 (PKCE). Chỉ dùng thư viện chuẩn Python.

  youtube_upload.py doctor
  youtube_upload.py login | login-url | login-finish "<url hoặc code>" | logout
  youtube_upload.py check  VIDEO --meta meta.json [--shorts]
  youtube_upload.py upload VIDEO --meta meta.json [--thumbnail f.jpg] [--privacy private|unlisted|public --yes]
                           [--publish-at 2026-12-01T19:00:00+07:00] [--shorts] [--ai-generated]
                           [--made-for-kids yes|no] [--dry-run]
  youtube_upload.py selftest

Quyền xin: chỉ https://www.googleapis.com/auth/youtube.upload. Token lưu ở $YT_CONFIG_DIR
(mặc định ~/.config/dang-video-youtube/token.json, chmod 600). Mặc định đăng ở chế độ riêng tư."""
import argparse
import base64
import hashlib
import http.server
import json
import mimetypes
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCOPE = "https://www.googleapis.com/auth/youtube.upload"
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = os.environ.get("YT_TOKEN_URL", "https://oauth2.googleapis.com/token")
REVOKE_URL = os.environ.get("YT_REVOKE_URL", "https://oauth2.googleapis.com/revoke")
UPLOAD_BASE = os.environ.get("YT_UPLOAD_BASE", "https://www.googleapis.com/upload/youtube/v3")
CHUNK = int(os.environ.get("YT_CHUNK", 8 * 1024 * 1024))  # bội số của 256 KiB
CFG = Path(os.environ.get("YT_CONFIG_DIR", Path.home() / ".config" / "dang-video-youtube"))
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".wmv", ".flv", ".mpg", ".mpeg", ".3gp", ".mts"}


def die(msg, code=1):
    print(f"LỖI: {msg}", file=sys.stderr)
    sys.exit(code)


def info(msg):
    print(msg, file=sys.stderr, flush=True)


# ───────────────────────── HTTP ─────────────────────────
class ApiError(Exception):
    def __init__(self, status, body):
        self.status, self.body = status, body
        super().__init__(f"HTTP {status}: {body[:400]}")


def reasons(body):
    try:
        return [e.get("reason", "") for e in json.loads(body)["error"]["errors"]]
    except Exception:
        return []


def _req(method, url, data=None, headers=None, timeout=120):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def explain(status, body):
    r = reasons(body)
    if "quotaExceeded" in r or "dailyLimitExceeded" in r:
        return "Hết hạn mức API trong ngày (mỗi video ≈ 1.600 / 10.000 đơn vị). Thử lại sau 0 giờ giờ Thái Bình Dương."
    if "uploadLimitExceeded" in r:
        return "Kênh đã chạm giới hạn số video upload trong ngày."
    if "forbidden" in r or "youtubeSignupRequired" in r:
        return "Tài khoản chưa có kênh YouTube, hoặc chưa cấp quyền youtube.upload (đăng nhập lại: login)."
    if "invalidTitle" in r or "invalidDescription" in r or "invalidTags" in r:
        return "Tiêu đề / mô tả / thẻ không hợp lệ (xem lệnh check)."
    if status == 401:
        return "Token hết hạn hoặc bị thu hồi: chạy lại login."
    return body[:400]


# ───────────────────────── OAuth ─────────────────────────
def client_file(args=None):
    p = (getattr(args, "client_secret", None) or os.environ.get("YT_CLIENT_SECRET_FILE")
         or str(CFG / "client_secret.json"))
    return Path(p).expanduser()


def load_client(args=None):
    p = client_file(args)
    if not p.exists():
        die(f"Không thấy file khóa OAuth: {p}\nXem references/huong-dan-oauth.md (tạo OAuth client loại Desktop app, tải JSON).")
    d = json.loads(p.read_text(encoding="utf-8"))
    c = d.get("installed") or d.get("web")
    if not c or "client_id" not in c:
        die(f"{p} không phải file client_secret.json hợp lệ (cần khóa 'installed').")
    return c


def save_json_private(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    os.replace(tmp, path)
    os.chmod(path, 0o600)


def token_exchange(client, params):
    body = urllib.parse.urlencode({**params, "client_id": client["client_id"],
                                   **({"client_secret": client["client_secret"]} if client.get("client_secret") else {})}).encode()
    st, _, b = _req("POST", TOKEN_URL, body, {"Content-Type": "application/x-www-form-urlencoded"})
    if st != 200:
        die(f"Google từ chối ({st}): {b.decode(errors='replace')[:300]}")
    return json.loads(b)


def store_token(tok, old=None):
    out = {"refresh_token": tok.get("refresh_token") or (old or {}).get("refresh_token"),
           "access_token": tok["access_token"], "expires_at": time.time() + int(tok.get("expires_in", 3600)) - 60,
           "scope": tok.get("scope", SCOPE)}
    if not out["refresh_token"]:
        die("Google không trả refresh token. Thu hồi quyền cũ tại https://myaccount.google.com/permissions rồi login lại.")
    save_json_private(CFG / "token.json", out)


def access_token(args=None):
    tf = CFG / "token.json"
    if not tf.exists():
        die("Chưa đăng nhập. Chạy: youtube_upload.py login (hoặc login-url + login-finish).")
    t = json.loads(tf.read_text())
    if t["expires_at"] > time.time():
        return t["access_token"]
    new = token_exchange(load_client(args), {"grant_type": "refresh_token", "refresh_token": t["refresh_token"]})
    store_token(new, t)
    return new["access_token"]


def build_auth_url(client, redirect, state, challenge):
    q = {"client_id": client["client_id"], "redirect_uri": redirect, "response_type": "code", "scope": SCOPE,
         "access_type": "offline", "prompt": "consent", "state": state,
         "code_challenge": challenge, "code_challenge_method": "S256"}
    return AUTH_URI + "?" + urllib.parse.urlencode(q)


def new_pkce():
    v = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()
    c = base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b"=").decode()
    return v, c


def finish_login(client, code, verifier, redirect):
    tok = token_exchange(client, {"grant_type": "authorization_code", "code": code, "code_verifier": verifier,
                                  "redirect_uri": redirect})
    store_token(tok)
    info(f"Đã đăng nhập. Token lưu ở {CFG/'token.json'} (quyền 600).")


def cmd_login_url(args):
    c = load_client(args)
    v, ch = new_pkce()
    state = secrets.token_urlsafe(16)
    redirect = "http://127.0.0.1:8765"
    save_json_private(CFG / "pending.json", {"verifier": v, "state": state, "redirect": redirect})
    print(build_auth_url(c, redirect, state, ch))
    info("\nMở link trên bằng trình duyệt, đăng nhập, bấm Cho phép. Trang cuối sẽ báo không kết nối được 127.0.0.1: bình thường.\n"
         'Copy toàn bộ địa chỉ trên thanh địa chỉ, rồi chạy: youtube_upload.py login-finish "<địa chỉ đó>"')


def cmd_login_finish(args):
    p = CFG / "pending.json"
    if not p.exists():
        die("Chưa chạy login-url (không có phiên đăng nhập đang chờ).")
    pend = json.loads(p.read_text())
    s = args.url.strip()
    if s.startswith("http"):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(s).query)
        if q.get("state", [""])[0] != pend["state"]:
            die("Tham số state không khớp: dùng đúng link do login-url vừa tạo.")
        if "error" in q:
            die(f"Google báo: {q['error'][0]}")
        code = q.get("code", [""])[0]
    else:
        code = s
    if not code:
        die("Không tìm thấy code trong địa chỉ đã dán.")
    finish_login(load_client(args), code, pend["verifier"], pend["redirect"])
    p.unlink(missing_ok=True)


def cmd_login(args):
    c = load_client(args)
    v, ch = new_pkce()
    state = secrets.token_urlsafe(16)
    result = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" in q or "error" in q:
                result.update({k: v[0] for k, v in q.items()})
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h3>Xong. Có thể đóng tab này.</h3>".encode())
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    url = build_auth_url(c, redirect, state, ch)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    info("Mở link này trong trình duyệt để đăng nhập:\n" + url)
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass
    t0 = time.time()
    while not result and time.time() - t0 < 300:
        time.sleep(0.3)
    srv.shutdown()
    if not result:
        die("Hết 5 phút chưa nhận được phản hồi. Nếu không có trình duyệt trên máy này, dùng login-url + login-finish.")
    if result.get("state") != state:
        die("state không khớp.")
    if "error" in result:
        die(f"Google báo: {result['error']}")
    finish_login(c, result["code"], v, redirect)


def cmd_logout(args):
    tf = CFG / "token.json"
    if tf.exists():
        t = json.loads(tf.read_text())
        try:
            _req("POST", REVOKE_URL, urllib.parse.urlencode({"token": t["refresh_token"]}).encode(),
                 {"Content-Type": "application/x-www-form-urlencoded"}, timeout=20)
        except Exception as e:
            info(f"(không thu hồi được trên Google: {e}; vẫn xóa token cục bộ)")
        tf.unlink()
    (CFG / "pending.json").unlink(missing_ok=True)
    print("Đã xóa token. Kiểm tra thêm tại https://myaccount.google.com/permissions")


def cmd_doctor(args):
    ok = True
    cf = client_file(args)
    print(f"{'OK ' if cf.exists() else 'THIẾU'} file khóa OAuth: {cf}")
    ok &= cf.exists()
    tf = CFG / "token.json"
    print(f"{'OK ' if tf.exists() else 'THIẾU'} đã đăng nhập (token): {tf}")
    ok &= tf.exists()
    if tf.exists():
        mode = oct(tf.stat().st_mode & 0o777)
        print(f"{'OK ' if mode == '0o600' else 'CẢNH BÁO'} quyền file token {mode}")
    print(f"{'OK ' if shutil.which('ffprobe') else 'tùy chọn'} ffprobe (để kiểm tra độ dài / khổ Shorts)")
    print("Lưu ý: project chưa qua audit → video upload bị khóa riêng tư. Xem SKILL.md.")
    sys.exit(0 if ok else 1)


# ───────────────────────── Metadata ─────────────────────────
def probe(path):
    if not shutil.which("ffprobe"):
        return None
    try:
        o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height:format=duration", "-of", "json", str(path)],
                           capture_output=True, text=True, timeout=30).stdout
        j = json.loads(o)
        s = j["streams"][0]
        return {"w": s["width"], "h": s["height"], "dur": float(j["format"]["duration"])}
    except Exception:
        return None


def tags_len(tags):
    return sum(len(t) + (2 if " " in t else 0) for t in tags) + max(0, len(tags) - 1)


def build_body(args, meta, video):
    errs, warns = [], []
    title = (meta.get("title") or "").strip()
    desc = meta.get("description") or ""
    tags = [t.strip() for t in meta.get("tags", []) if t.strip()]
    if not title:
        errs.append("thiếu title")
    if len(title) > 100:
        errs.append(f"tiêu đề dài {len(title)} ký tự (tối đa 100)")
    if re.search(r"[<>]", title + desc + "".join(tags)):
        errs.append("tiêu đề / mô tả / thẻ không được chứa < hoặc >")
    if len(desc.encode("utf-8")) > 5000:
        errs.append(f"mô tả {len(desc.encode('utf-8'))} byte (tối đa 5000)")
    if tags_len(tags) > 500:
        errs.append(f"tổng độ dài thẻ {tags_len(tags)} (tối đa 500)")
    p = Path(video)
    if not p.is_file():
        errs.append(f"không thấy file video: {video}")
    elif p.suffix.lower() not in VIDEO_EXT:
        warns.append(f"đuôi file lạ {p.suffix} (YouTube nhận mp4, mov, webm, mkv, avi…)")
    if args.shorts:
        pr = probe(video) if p.is_file() else None
        if pr:
            if pr["dur"] > 180:
                errs.append(f"Shorts phải ≤ 180 giây, video dài {pr['dur']:.0f}s")
            if pr["h"] < pr["w"]:
                warns.append("video ngang: YouTube chỉ xếp vào Shorts nếu khung vuông hoặc dọc")
        else:
            warns.append("không đọc được thông số video (thiếu ffprobe?) nên chưa kiểm tra Shorts")
        if "#shorts" not in desc.lower() and "#shorts" not in title.lower():
            desc = (desc.rstrip() + "\n\n#Shorts").strip()
    if args.publish_at:
        try:
            dt = datetime.fromisoformat(args.publish_at.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                errs.append("--publish-at cần múi giờ, ví dụ 2026-12-01T19:00:00+07:00")
            elif dt <= datetime.now(timezone.utc):
                errs.append("--publish-at phải ở tương lai")
        except ValueError:
            errs.append("--publish-at không đúng định dạng ISO 8601")
        if args.privacy != "private":
            warns.append("hẹn giờ: video sẽ được đặt riêng tư cho đến giờ đó")
    privacy = "private" if args.publish_at else args.privacy
    if args.privacy == "public" and not args.yes and not args.publish_at:
        errs.append("đăng công khai cần --yes (chỉ thêm sau khi người dùng đồng ý công khai)")
    if args.thumbnail:
        t = Path(args.thumbnail)
        if not t.is_file():
            errs.append(f"không thấy thumbnail: {t}")
        elif t.stat().st_size > 2 * 1024 * 1024:
            errs.append("thumbnail tối đa 2 MB")
        elif t.suffix.lower() not in (".jpg", ".jpeg", ".png", ".gif", ".bmp"):
            errs.append("thumbnail nên là jpg / png")
    status = {"privacyStatus": privacy, "selfDeclaredMadeForKids": args.made_for_kids == "yes",
              "containsSyntheticMedia": bool(args.ai_generated)}
    if args.publish_at:
        status["publishAt"] = datetime.fromisoformat(args.publish_at.replace("Z", "+00:00")).astimezone(timezone.utc) \
            .strftime("%Y-%m-%dT%H:%M:%SZ") if not errs else args.publish_at
    snippet = {"title": title, "description": desc, "categoryId": str(meta.get("categoryId", "22"))}
    if tags:
        snippet["tags"] = tags
    if meta.get("defaultLanguage"):
        snippet["defaultLanguage"] = meta["defaultLanguage"]
        snippet["defaultAudioLanguage"] = meta.get("defaultAudioLanguage", meta["defaultLanguage"])
    return {"snippet": snippet, "status": status}, errs, warns


def load_meta(args):
    if not args.meta:
        die("Thiếu --meta meta.json (xem mau-meta.json).")
    try:
        return json.loads(Path(args.meta).read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Không đọc được {args.meta}: {e}")


def prepare(args):
    body, errs, warns = build_body(args, load_meta(args), args.video)
    for w in warns:
        info(f"CẢNH BÁO: {w}")
    if errs:
        for e in errs:
            info(f"LỖI: {e}")
        sys.exit(1)
    return body


def cmd_check(args):
    body = prepare(args)
    print(json.dumps(body, ensure_ascii=False, indent=2))
    print("Hợp lệ.")


# ───────────────────────── Upload ─────────────────────────
def start_session(tok, body, size, ctype):
    url = f"{UPLOAD_BASE}/videos?uploadType=resumable&part=snippet,status"
    st, h, b = _req("POST", url, json.dumps(body).encode(), {
        "Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": ctype})
    if st != 200:
        die(f"Không mở được phiên upload ({st}): {explain(st, b.decode(errors='replace'))}")
    loc = {k.lower(): v for k, v in h.items()}.get("location")
    if not loc:
        die("Google không trả địa chỉ phiên upload.")
    return loc


def resume_offset(loc, tok, size):
    st, h, _ = _req("PUT", loc, b"", {"Authorization": f"Bearer {tok}", "Content-Range": f"bytes */{size}",
                                      "Content-Length": "0"})
    if st in (200, 201):
        return None
    rng = {k.lower(): v for k, v in h.items()}.get("range")
    return int(rng.split("-")[1]) + 1 if rng else 0


def upload_file(path, body, tok, args):
    size = Path(path).stat().st_size
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    loc = start_session(tok, body, size, ctype)
    off, tries, t0 = 0, 0, time.time()
    with open(path, "rb") as f:
        while True:
            f.seek(off)
            chunk = f.read(CHUNK)
            end = off + len(chunk) - 1
            try:
                st, h, b = _req("PUT", loc, chunk, {"Authorization": f"Bearer {tok}", "Content-Type": ctype,
                                                    "Content-Range": f"bytes {off}-{end}/{size}"}, timeout=300)
            except (urllib.error.URLError, socket.timeout, ConnectionError) as e:
                st, h, b = 599, {}, str(e).encode()
            if st in (200, 201):
                info(f"\r  tải lên: 100% ({size/1e6:.1f} MB, {time.time()-t0:.0f}s)")
                return json.loads(b)
            if st == 308:
                rng = {k.lower(): v for k, v in h.items()}.get("range")
                off = int(rng.split("-")[1]) + 1 if rng else 0
                tries = 0
                info(f"\r  tải lên: {off*100//size}%")
                continue
            if st in (500, 502, 503, 504, 599) and tries < 8:
                tries += 1
                time.sleep(min(2 ** tries, 60))
                r = resume_offset(loc, tok, size)
                if r is None:
                    die("Phiên đã hoàn tất nhưng không đọc được kết quả; kiểm tra trong YouTube Studio.")
                off = r
                continue
            die(f"Upload thất bại ({st}): {explain(st, b.decode(errors='replace'))}")


def set_thumbnail(vid, thumb, tok):
    ctype = mimetypes.guess_type(thumb)[0] or "image/jpeg"
    st, _, b = _req("POST", f"{UPLOAD_BASE}/thumbnails/set?videoId={vid}&uploadType=media", Path(thumb).read_bytes(),
                    {"Authorization": f"Bearer {tok}", "Content-Type": ctype})
    if st != 200:
        info(f"CẢNH BÁO: video đã lên nhưng đặt thumbnail lỗi ({st}): {explain(st, b.decode(errors='replace'))}"
             " (kênh cần xác minh số điện thoại để dùng thumbnail tùy chỉnh)")
        return False
    return True


def cmd_upload(args):
    body = prepare(args)
    st = body["status"]
    size = Path(args.video).stat().st_size
    info(f"Video: {args.video} ({size/1e6:.1f} MB)\nTiêu đề: {body['snippet']['title']}\nChế độ: {st['privacyStatus']}"
         + (f", hẹn công khai {st['publishAt']}" if "publishAt" in st else "")
         + f"\nAI tạo: {'có' if st['containsSyntheticMedia'] else 'không'} · cho trẻ em: {'có' if st['selfDeclaredMadeForKids'] else 'không'}"
         + f"\nThumbnail: {args.thumbnail or 'không'}")
    if args.dry_run:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        info("--dry-run: chưa gửi gì lên YouTube.")
        return
    tok = access_token(args)
    res = upload_file(args.video, body, tok, args)
    vid = res["id"]
    thumb_ok = set_thumbnail(vid, args.thumbnail, tok) if args.thumbnail else None
    out = {"id": vid, "url": f"https://youtu.be/{vid}", "studio": f"https://studio.youtube.com/video/{vid}/edit",
           "privacy": st["privacyStatus"], "thumbnail": thumb_ok,
           "uploadStatus": res.get("status", {}).get("uploadStatus")}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if st["privacyStatus"] == "private" and args.privacy != "private":
        info("Lưu ý: nếu video vẫn riêng tư dù đã chọn công khai, project chưa qua YouTube API audit (xem SKILL.md).")


# ───────────────────────── Tự kiểm tra với server giả ─────────────────────────
def cmd_selftest(args):
    import tempfile
    state = {"chunks": [], "thumb": None, "meta": None, "fail_once": True}

    class H(http.server.BaseHTTPRequestHandler):
        def _send(self, code, obj=None, hdr=None):
            b = json.dumps(obj).encode() if obj is not None else b""
            self.send_response(code)
            for k, v in (hdr or {}).items():
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(n)
            if self.path.startswith("/token"):
                return self._send(200, {"access_token": "AT1", "refresh_token": "RT1", "expires_in": 3600, "scope": SCOPE})
            if self.headers.get("Authorization") != "Bearer AT1":
                return self._send(401, {"error": {"errors": [{"reason": "authError"}]}})
            if "/videos" in self.path:
                state["meta"] = json.loads(data)
                host = self.headers["Host"]
                return self._send(200, None, {"Location": f"http://{host}/session/1"})
            if "/thumbnails/set" in self.path:
                state["thumb"] = data
                return self._send(200, {"items": []})
            self._send(404)

        def do_PUT(self):
            n = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(n)
            cr = self.headers.get("Content-Range", "")
            if cr.startswith("bytes */"):
                got = sum(len(c) for c in state["chunks"])
                return self._send(308, None, {"Range": f"bytes=0-{got-1}"} if got else {})
            m = re.match(r"bytes (\d+)-(\d+)/(\d+)", cr)
            a, b, total = map(int, m.groups())
            if a == 262144 * 2 and state["fail_once"]:  # giả lỗi 503 một lần để thử tự nối lại
                state["fail_once"] = False
                return self._send(503, {"error": {"errors": [{"reason": "backendError"}]}})
            got = sum(len(c) for c in state["chunks"])
            if a != got:
                return self._send(400, {"error": "offset sai"})
            state["chunks"].append(data)
            if b + 1 >= total:
                return self._send(200, {"id": "MOCK123", "status": {"uploadStatus": "uploaded"}})
            self._send(308, None, {"Range": f"bytes=0-{b}"})

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"
    tmp = Path(tempfile.mkdtemp())
    (tmp / "cs.json").write_text(json.dumps({"installed": {"client_id": "cid", "client_secret": "sec"}}))
    video = tmp / "v.mp4"
    video.write_bytes(os.urandom(262144 * 5 + 1234))
    (tmp / "t.jpg").write_bytes(b"\xff\xd8\xff\xd9")
    (tmp / "meta.json").write_text(json.dumps({"title": "Thử", "description": "mô tả", "tags": ["a", "b c"]}))
    env = {**os.environ, "YT_CONFIG_DIR": str(tmp / "cfg"), "YT_TOKEN_URL": base + "/token", "YT_UPLOAD_BASE": base,
           "YT_CHUNK": str(262144 * 2), "YT_CLIENT_SECRET_FILE": str(tmp / "cs.json")}
    me = [sys.executable, os.path.abspath(__file__)]

    def run(*a, expect=0):
        r = subprocess.run(me + list(a), env=env, capture_output=True, text=True)
        return r

    fails = []

    def ok(name, cond, extra=""):
        print(("OK   " if cond else "LỖI ") + name + (f" — {extra}" if (extra and not cond) else ""))
        if not cond:
            fails.append(name)

    # 1. login-url + finish
    r = run("login-url")
    url = r.stdout.strip()
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    ok("login-url tạo link có PKCE + scope tối thiểu", q.get("code_challenge_method") == ["S256"] and q.get("scope") == [SCOPE])
    r = run("login-finish", f"http://127.0.0.1:8765/?state={q['state'][0]}&code=abc")
    tf = tmp / "cfg" / "token.json"
    ok("login-finish lưu token chmod 600", tf.exists() and oct(tf.stat().st_mode & 0o777) == "0o600", r.stderr)
    r = run("login-finish", "http://127.0.0.1:8765/?state=sai&code=abc")
    ok("state sai bị từ chối", r.returncode != 0)
    # 2. kiểm tra metadata
    bad = tmp / "bad.json"
    bad.write_text(json.dumps({"title": "x" * 101}))
    ok("check bắt tiêu đề quá dài", run("check", str(video), "--meta", str(bad)).returncode != 0)
    r = run("upload", str(video), "--meta", str(tmp / "meta.json"), "--privacy", "public", "--dry-run")
    ok("public không có --yes bị chặn", r.returncode != 0)
    r = run("upload", str(video), "--meta", str(tmp / "meta.json"), "--dry-run")
    ok("dry-run mặc định riêng tư, không gửi", r.returncode == 0 and '"privacyStatus": "private"' in r.stdout and state["meta"] is None)
    # 3. upload thật với server giả (có lỗi 503 giữa chừng)
    r = run("upload", str(video), "--meta", str(tmp / "meta.json"), "--thumbnail", str(tmp / "t.jpg"),
            "--ai-generated", "--shorts")
    try:
        out = json.loads(r.stdout)
    except Exception:
        out = {}
    ok("upload trả id + link", out.get("id") == "MOCK123" and out.get("url") == "https://youtu.be/MOCK123", r.stderr[-300:])
    ok("nối lại sau lỗi 503, đủ byte, đúng thứ tự", b"".join(state["chunks"]) == video.read_bytes())
    ok("thumbnail đã gửi", state["thumb"] == b"\xff\xd8\xff\xd9")
    ok("metadata: riêng tư + khai báo AI + #Shorts", state["meta"] and state["meta"]["status"]["privacyStatus"] == "private"
       and state["meta"]["status"]["containsSyntheticMedia"] is True and "#Shorts" in state["meta"]["snippet"]["description"])
    # 4. refresh token khi hết hạn
    t = json.loads(tf.read_text())
    t["expires_at"] = 0
    tf.write_text(json.dumps(t))
    state.update(chunks=[], fail_once=False)
    r = run("upload", str(video), "--meta", str(tmp / "meta.json"))
    ok("tự làm mới access token khi hết hạn", r.returncode == 0 and "MOCK123" in r.stdout, r.stderr[-300:])
    # 5. logout
    run("logout")
    ok("logout xóa token", not tf.exists())
    srv.shutdown()
    shutil.rmtree(tmp, ignore_errors=True)
    print("\nĐẠT" if not fails else f"\nKHÔNG ĐẠT: {', '.join(fails)}")
    sys.exit(1 if fails else 0)


# ───────────────────────── CLI ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client-secret")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n, f in (("doctor", cmd_doctor), ("login", cmd_login), ("login-url", cmd_login_url), ("logout", cmd_logout),
                 ("selftest", cmd_selftest)):
        sub.add_parser(n).set_defaults(fn=f)
    p = sub.add_parser("login-finish")
    p.add_argument("url")
    p.set_defaults(fn=cmd_login_finish)
    for n, f in (("check", cmd_check), ("upload", cmd_upload)):
        p = sub.add_parser(n)
        p.add_argument("video")
        p.add_argument("--meta")
        p.add_argument("--thumbnail")
        p.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
        p.add_argument("--yes", action="store_true", help="xác nhận đăng công khai")
        p.add_argument("--publish-at")
        p.add_argument("--shorts", action="store_true")
        p.add_argument("--ai-generated", action="store_true")
        p.add_argument("--made-for-kids", choices=["yes", "no"], default="no")
        p.add_argument("--dry-run", action="store_true")
        p.set_defaults(fn=f)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
