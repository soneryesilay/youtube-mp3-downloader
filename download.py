#!/usr/bin/env python3
"""Bulk YouTube MP3 downloader — searches and downloads songs from songs.txt."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yt_dlp

SCRIPT_DIR = Path(__file__).resolve().parent
SONG_LIST_FILE = SCRIPT_DIR / "songs.txt"
OUTPUT_DIR = SCRIPT_DIR / "mp3"
LOG_FILE = SCRIPT_DIR / "download.log"

YDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": str(OUTPUT_DIR / "%(title)s.%(ext)s"),
    "restrict_filenames": True,
    "noplaylist": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "extractor_args": {
        "youtube": {
            "player_client": ["android_vr", "web"],
        }
    },
    "concurrent_fragment_downloads": 4,
    "quiet": False,
    "no_warnings": False,
}


def check_ffmpeg() -> bool:
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def read_songs(path: Path) -> list[str]:
    if not path.exists():
        print(f"Error: {path.name} not found.")
        print(f"Create {path.name} and add one song per line.")
        sys.exit(1)

    songs: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        songs.append(line)

    if not songs:
        print(f"Error: no songs found in {path.name}.")
        sys.exit(1)

    return songs


def search_query(song: str) -> str:
    if song.startswith(("http://", "https://", "ytsearch")):
        return song
    return f"ytsearch1:{song}"


def first_video_info(info: dict | None) -> dict | None:
    if info is None:
        return None
    entries = info.get("entries")
    if entries:
        for entry in entries:
            if entry is not None:
                return entry
        return None
    return info


def expected_mp3_path(ydl: yt_dlp.YoutubeDL, info: dict) -> Path:
    base = Path(ydl.prepare_filename(info)).with_suffix("")
    return base.with_suffix(".mp3")


def log_success(song: str, title: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] OK: {song} -> {title}\n")


def download_song(song: str, index: int, total: int) -> tuple[str, str]:
    print(f"\n[{index}/{total}] Searching: {song}")

    opts = dict(YDL_OPTS)
    query = search_query(song)

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = first_video_info(ydl.extract_info(query, download=False))
            if info is None:
                return "failed", "No results found"

            title = info.get("title", song)
            mp3_path = expected_mp3_path(ydl, info)

            if mp3_path.exists():
                print(f"  Skipped: {title} (already exists)")
                return "skipped", title

            ydl.process_info(info)

            if not mp3_path.exists():
                mp3_files = list(OUTPUT_DIR.glob("*.mp3"))
                if mp3_files:
                    mp3_path = max(mp3_files, key=lambda p: p.stat().st_mtime)

            if not mp3_path.exists():
                return "failed", "MP3 file was not created"

            log_success(song, title)
            print(f"  Downloaded: {title}")
            return "success", title

    except Exception as exc:
        message = str(exc).strip().split("\n")[0] or type(exc).__name__
        print(f"  Error: {message}")
        return "failed", message


def main() -> None:
    if sys.platform == "win32":
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8")

    print("YouTube MP3 Bulk Downloader")
    print("=" * 40)

    if not check_ffmpeg():
        print("\nError: ffmpeg not found.")
        print("ffmpeg is required for MP3 conversion.")
        print("See SETUP.txt for installation steps.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    songs = read_songs(SONG_LIST_FILE)
    total = len(songs)
    print(f"\nFound {total} song(s). Starting download...\n")

    success_count = 0
    skipped_count = 0
    failed: list[tuple[str, str]] = []

    for i, song in enumerate(songs, start=1):
        status, detail = download_song(song, i, total)
        if status == "success":
            success_count += 1
        elif status == "skipped":
            skipped_count += 1
        else:
            failed.append((song, detail))

    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    print(f"Successful: {success_count}/{total}")
    print(f"Skipped:    {skipped_count}/{total}")
    print(f"Failed:     {len(failed)}/{total}")

    if failed:
        print("\nFailed songs:")
        for song, reason in failed:
            print(f"  - {song}")
            print(f"    Reason: {reason}")

    print(f"\nMP3 files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
