# YouTube MP3 Bulk Downloader

A simple CLI tool that reads song names from `songs.txt`, searches YouTube, and saves each track as an MP3 file.

Includes a one-click Windows launcher. Processes lists sequentially, skips files that already exist, and prints a summary when finished.

## Features

- **Automatic search** — Just type the song name (`Artist - Song Title`)
- **MP3 output** — 192 kbps MP3 via ffmpeg
- **Smart skip** — Won't re-download files already in `mp3/`
- **Fault tolerant** — Failed songs don't stop the rest of the list
- **URL support** — Paste a direct YouTube link if you prefer
- **Progress output** — Clear terminal logs and a final summary

## Quick Start

### 1. Requirements

| Tool | Notes |
|------|-------|
| [Python 3.10+](https://www.python.org/downloads/) | Check **Add to PATH** during install |
| [ffmpeg](https://ffmpeg.org/download.html) | Required for MP3 conversion |
| yt-dlp | Installed via `pip install -r requirements.txt` |

Install ffmpeg (PowerShell):

```powershell
winget install Gyan.FFmpeg
```

### 2. Set up the project

```powershell
git clone https://github.com/soneryesilay/youtube-mp3-indirici.git
cd youtube-mp3-indirici
pip install -r requirements.txt
```

### 3. Create your song list

```powershell
copy songs.example.txt songs.txt
```

Edit `songs.txt` and add one entry per line:

```text
Radiohead - Let Down
Dua Lipa - Levitating
https://www.youtube.com/watch?v=VIDEO_ID
```

### 4. Start downloading

**Windows:** double-click `download.bat`

**Terminal:**

```powershell
python download.py
```

Files are saved to the `mp3/` folder.

## Project Structure

```
youtube-mp3-indirici/
├── download.py           # Main script
├── download.bat          # Windows one-click launcher
├── songs.example.txt     # Example song list
├── songs.txt             # Your list (not tracked by git)
├── requirements.txt      # Python dependencies
├── mp3/                  # Downloaded MP3 files (not tracked by git)
├── download.log          # Successful download log
├── SETUP.txt             # Short setup notes
└── README.md
```

## How It Works

```mermaid
flowchart LR
    list[songs.txt] --> script[download.py]
    script --> search["YouTube search ytsearch1"]
    search --> download[yt-dlp download]
    download --> convert[ffmpeg to MP3]
    convert --> output[mp3/ folder]
```

1. Each line is searched on YouTube and the **first result** is used
2. Audio is downloaded and converted to MP3
3. Existing files are skipped automatically
4. A summary shows successful, skipped, and failed entries

## Tips

- Use `Artist - Song Title` for more accurate matches
- Auto-search may pick covers, live versions, or karaoke tracks
- Re-running the script only downloads missing songs
- Retry after temporary network errors — already downloaded files are skipped

## Limitations

- Intended for **personal use** only
- Subject to YouTube Terms of Service and copyright law
- Download speed depends on your connection and YouTube availability

## License

[MIT](LICENSE)
