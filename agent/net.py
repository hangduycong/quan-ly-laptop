"""HTTP tối giản bằng thư viện chuẩn (không cần cài thêm gì). Các hàm chặn — gọi qua asyncio.to_thread."""
import json
import secrets
import urllib.error
import urllib.request

UA = "ParentControlAgent/2.0"


class HttpError(Exception):
    def __init__(self, status: int, body: str):
        super().__init__(f"HTTP {status}: {body[:300]}")
        self.status = status
        self.body = body


def request(method: str, url: str, *, json_body=None, data: bytes | None = None,
            headers: dict | None = None, timeout: float = 30):
    """Trả về JSON đã giải mã (hoặc None). Lỗi HTTP -> HttpError."""
    h = {"User-Agent": UA, **(headers or {})}
    if json_body is not None:
        data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        h["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        raise HttpError(e.code, e.read().decode("utf-8", "replace")) from None
    return json.loads(raw) if raw.strip() else None


def multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    """files = {"photo": ("screen.jpg", bytes, "image/jpeg")}"""
    boundary = "----pc" + secrets.token_hex(12)
    out = bytearray()
    for k, v in fields.items():
        out += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (fname, content, ctype) in files.items():
        out += (f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{fname}"\r\n'
                f"Content-Type: {ctype}\r\n\r\n").encode()
        out += content + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def sse_lines(url: str, timeout: float = 90):
    """Đọc luồng Server-Sent Events, sinh ra (event, data_str)."""
    req = urllib.request.Request(url, headers={"Accept": "text/event-stream", "User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        raise HttpError(e.code, e.read().decode("utf-8", "replace")) from None
    with resp:
        event, data = None, []
        for raw in resp:
            line = raw.decode("utf-8").rstrip("\r\n")
            if not line:
                if event is not None:
                    yield event, "\n".join(data)
                event, data = None, []
            elif line.startswith("event:"):
                event = line[6:].strip()
            elif line.startswith("data:"):
                data.append(line[5:].strip())
