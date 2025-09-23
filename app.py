from flask import Flask, render_template
from pathlib import Path
import csv
import re
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CSV_PATH = Path("data/videos.csv")

def load_videos():
    rows: list[dict] = []

    def extract_id(row: dict) -> str:
        vid = (row.get("id") or "").strip()
        if vid:
            return vid
        url = (row.get("url") or "").strip()
        if not url:
            return ""
        # try v= query
        try:
            qs_v = parse_qs(urlparse(url).query).get("v", [""])[0]
        except Exception:
            qs_v = ""
        if qs_v:
            return qs_v
        # try common YouTube path patterns (shorts, youtu.be, /watch/, /live/ etc.)
        m = re.search(r"(?:youtu\.be/|/shorts/|/live/|/watch\?v=|/embed/)([A-Za-z0-9_-]{6,})", url)
        return m.group(1) if m else ""

    if CSV_PATH.exists():
        with CSV_PATH.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                vid = extract_id(row)
                if not vid:
                    # skip rows we can't understand
                    continue
                row["id"] = vid
                # YouTube公式のサムネURL（保存してなくてもIDから表示できる）
                row["thumb"] = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                rows.append(row)

    # 追加日時の新しい順に（なければ末尾）
    rows.sort(key=lambda x: x.get("added_at", ""), reverse=True)
    return rows

@app.route("/")
def index():
    videos = load_videos()
    return render_template("index.html", videos=videos)

if __name__ == "__main__":
    app.run(debug=True, port=5001)