#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step2: YouTubeチャンネルから動画一覧を取得してCSVに保存
"""

import csv
from datetime import datetime
from pathlib import Path
import yt_dlp

OUT_CSV = Path("data/videos.csv")

# 日本M&Aセンター公式チャンネルのURL（仮）
CHANNEL_URL = "https://www.youtube.com/@nihonma/videos"

def fetch_videos(channel_url: str, limit: int = 10):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,   # 動画本体をDLせず一覧情報だけ取る
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return info.get("entries", [])[:limit]

def write_csv(videos, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if out.exists():
        with out.open("r", encoding="utf-8") as f:
            next(f, None)  # header
            for line in f:
                existing.add(line.split(",", 1)[0])  # 先頭列: id

    new_file = not out.exists()
    with out.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["id", "title", "url", "added_at"])
        now = datetime.now().isoformat(timespec="seconds")
        added = 0
        for v in videos:
            vid = v["id"]
            if vid in existing:
                continue
            w.writerow([vid, v["title"], f"https://www.youtube.com/watch?v={vid}", now])
            added += 1
    print(f"✅ 新規 {added} 件だけCSVに追記しました。")


def main():
    videos = fetch_videos(CHANNEL_URL, limit=5)
    if not videos:
        print("⚠️ 動画が取得できませんでした。URLを確認してください。")
        return
    write_csv(videos, OUT_CSV)
    print(f"✅ {len(videos)}件の動画を {OUT_CSV} に保存しました。")

if __name__ == "__main__":
    main()
