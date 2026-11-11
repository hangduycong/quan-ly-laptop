"""Lưu thời gian sử dụng theo (ngày, giờ, ứng dụng) vào SQLite."""
import datetime as dt
import sqlite3
import threading
from collections import defaultdict
from pathlib import Path


class UsageDB:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS usage(date TEXT, hour INTEGER, exe TEXT, seconds REAL,"
            " PRIMARY KEY(date, hour, exe))")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS videos(date TEXT, title TEXT, seconds REAL, last REAL,"
            " PRIMARY KEY(date, title))")
        self.conn.commit()
        self.lock = threading.Lock()
        self.buffer: dict[tuple, float] = defaultdict(float)
        self.vbuffer: dict[tuple, float] = defaultdict(float)

    def add(self, exe: str, seconds: float, when: dt.datetime | None = None):
        when = when or dt.datetime.now()
        with self.lock:
            self.buffer[(when.strftime("%Y-%m-%d"), when.hour, exe.lower())] += seconds

    def add_video(self, title: str, seconds: float):
        with self.lock:
            self.vbuffer[(dt.date.today().strftime("%Y-%m-%d"), title[:300])] += seconds

    def flush(self):
        with self.lock:
            items, self.buffer = list(self.buffer.items()), defaultdict(float)
            vids, self.vbuffer = list(self.vbuffer.items()), defaultdict(float)
        now = dt.datetime.now().timestamp()
        self.conn.executemany(
            "INSERT INTO videos(date,title,seconds,last) VALUES(?,?,?,?) "
            "ON CONFLICT(date,title) DO UPDATE SET seconds = seconds + excluded.seconds, last = excluded.last",
            [(d, t, s, now) for (d, t), s in vids])
        self.conn.executemany(
            "INSERT INTO usage(date,hour,exe,seconds) VALUES(?,?,?,?) "
            "ON CONFLICT(date,hour,exe) DO UPDATE SET seconds = seconds + excluded.seconds",
            [(d, h, e, s) for (d, h, e), s in items])
        self.conn.commit()

    # ------------------------------------------------------------ truy vấn
    def videos(self, date: str) -> list[dict]:
        self.flush()
        rows = self.conn.execute("SELECT title, seconds, last FROM videos WHERE date=? AND seconds >= 5 "
                                 "ORDER BY last DESC LIMIT 200", (date,)).fetchall()
        return [{"title": t, "seconds": round(s), "last": l} for t, s, l in rows]

    def day(self, date: str) -> dict:
        self.flush()
        rows = self.conn.execute("SELECT hour, exe, seconds FROM usage WHERE date=?", (date,)).fetchall()
        hours = [0.0] * 24
        apps: dict[str, float] = defaultdict(float)
        for h, exe, s in rows:
            hours[h] += s
            apps[exe] += s
        used = [h for h in range(24) if hours[h] >= 30]
        return {
            "date": date,
            "total": sum(hours),
            "hours": [round(x) for x in hours],
            "first": used[0] if used else None,
            "last": used[-1] if used else None,
            "apps": [{"exe": e, "seconds": round(s)} for e, s in sorted(apps.items(), key=lambda x: -x[1])],
        }

    def today_by_app(self) -> dict[str, float]:
        """Số giây đã dùng hôm nay của từng app (gồm cả phần chưa ghi xuống đĩa)."""
        date = dt.date.today().strftime("%Y-%m-%d")
        out: dict[str, float] = defaultdict(float)
        for exe, s in self.conn.execute("SELECT exe, SUM(seconds) FROM usage WHERE date=? GROUP BY exe", (date,)):
            out[exe] += s
        with self.lock:
            for (d, _h, exe), s in self.buffer.items():
                if d == date:
                    out[exe] += s
        return dict(out)

    def days(self, n: int) -> list[dict]:
        self.flush()
        out = []
        for i in range(n):
            d = (dt.date.today() - dt.timedelta(days=i)).strftime("%Y-%m-%d")
            (s,) = self.conn.execute("SELECT COALESCE(SUM(seconds),0) FROM usage WHERE date=?", (d,)).fetchone()
            out.append({"date": d, "total": round(s)})
        return out
