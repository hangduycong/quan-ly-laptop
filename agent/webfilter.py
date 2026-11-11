"""
Hạn chế YouTube và chặn trang web. Cần quyền Administrator/SYSTEM.

Hai lớp:
 1. Chính sách (policy) của Chrome và Edge trong registry:
      ForceYouTubeRestrict  (0 = tắt, 1 = vừa, 2 = nghiêm)
      URLBlocklist          (danh sách trang bị chặn)
    Chrome/Edge tự nạp lại policy sau ít phút; mở chrome://policy -> "Reload policies" để áp dụng ngay.
 2. File hosts (cho các trình duyệt khác như Firefox, Cốc Cốc, Brave):
      - Restricted Mode: trỏ tên miền YouTube về restrict.youtube.com / restrictmoderate.youtube.com
        (cách Google hướng dẫn cho quản trị mạng).
      - Chặn: trỏ về 0.0.0.0
"""
import re
import subprocess
import sys

IS_WIN = sys.platform == "win32"
if IS_WIN:
    import winreg

HOSTS = r"C:\Windows\System32\drivers\etc\hosts"
MARK_BEGIN = "# >>> ParentControl"
MARK_END = "# <<< ParentControl"

YT_RESTRICT_IP = {"strict": "216.239.38.120", "moderate": "216.239.38.119"}
YT_RESTRICT_HOSTS = ["www.youtube.com", "m.youtube.com", "youtubei.googleapis.com",
                     "youtube.googleapis.com", "www.youtube-nocookie.com"]
YT_BLOCK_HOSTS = ["youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com",
                  "youtu.be", "youtubei.googleapis.com", "www.youtube-nocookie.com"]

POLICY_KEYS = [r"SOFTWARE\Policies\Google\Chrome", r"SOFTWARE\Policies\Microsoft\Edge",
               r"SOFTWARE\Policies\BraveSoftware\Brave"]
YT_LEVEL = {"off": 0, "moderate": 1, "strict": 2, "block": 2}


def clean_site(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"^[a-z]+://", "", s)
    s = s.split("/")[0].split(":")[0]
    return s[4:] if s.startswith("www.") else s


def build_hosts_block(mode: str, sites: list[str]) -> list[str]:
    lines = [MARK_BEGIN]
    if mode in YT_RESTRICT_IP:
        lines += [f"{YT_RESTRICT_IP[mode]} {h}" for h in YT_RESTRICT_HOSTS]
    elif mode == "block":
        lines += [f"0.0.0.0 {h}" for h in YT_BLOCK_HOSTS]
    for s in sites:
        lines += [f"0.0.0.0 {s}", f"0.0.0.0 www.{s}"]
    lines.append(MARK_END)
    return lines


def rewrite_hosts(content: str, block: list[str]) -> str:
    out, skip = [], False
    for line in content.splitlines():
        if line.strip() == MARK_BEGIN:
            skip = True
            continue
        if line.strip() == MARK_END:
            skip = False
            continue
        if not skip:
            out.append(line)
    while out and not out[-1].strip():
        out.pop()
    if len(block) > 2:
        out += [""] + block
    return "\n".join(out) + "\n"


def _set_policies(level: int, blocklist: list[str], no_incognito: bool):
    for path in POLICY_KEYS:
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "ForceYouTubeRestrict", 0, winreg.REG_DWORD, level)
        # Tuỳ chọn: tắt cửa sổ ẩn danh / InPrivate
        name = "InPrivateModeAvailability" if "Edge" in path else "IncognitoModeAvailability"
        if no_incognito:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, 1)
        else:
            try:
                winreg.DeleteValue(key, name)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        # Xoá rồi ghi lại URLBlocklist
        try:
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, path + r"\URLBlocklist")
        except FileNotFoundError:
            pass
        if blocklist:
            bl = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path + r"\URLBlocklist", 0, winreg.KEY_ALL_ACCESS)
            for i, url in enumerate(blocklist, 1):
                winreg.SetValueEx(bl, str(i), 0, winreg.REG_SZ, url)
            winreg.CloseKey(bl)


def apply(web: dict) -> None:
    mode = web.get("youtube_mode", "off")
    sites = [clean_site(s) for s in web.get("blocked_sites", []) if clean_site(s)]
    blocklist = list(sites)
    if mode == "block":
        blocklist += ["youtube.com", "youtu.be", "youtube-nocookie.com"]
    if not IS_WIN:
        return
    _set_policies(YT_LEVEL.get(mode, 0), blocklist, bool(web.get("disable_incognito")))
    with open(HOSTS, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    new = rewrite_hosts(content, build_hosts_block(mode, sites))
    if new != content:
        with open(HOSTS, "w", encoding="utf-8") as f:
            f.write(new)
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True, creationflags=0x08000000)


def remove_all() -> None:
    """Gỡ mọi hạn chế (dùng khi gỡ cài đặt)."""
    if not IS_WIN:
        return
    for path in POLICY_KEYS:
        for sub in (r"\URLBlocklist", ""):
            try:
                if sub:
                    winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, path + sub)
                else:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS)
                    for name in ("ForceYouTubeRestrict", "IncognitoModeAvailability", "InPrivateModeAvailability"):
                        try:
                            winreg.DeleteValue(key, name)
                        except FileNotFoundError:
                            pass
                    winreg.CloseKey(key)
            except FileNotFoundError:
                pass
    with open(HOSTS, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    with open(HOSTS, "w", encoding="utf-8") as f:
        f.write(rewrite_hosts(content, [MARK_BEGIN, MARK_END]))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--remove":
    remove_all()
