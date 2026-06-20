@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo YouTube MP3 Bulk Downloader
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found.
    echo Follow the steps in README.md or SETUP.txt.
    pause
    exit /b 1
)

if not exist "songs.txt" (
    if exist "songs.example.txt" (
        copy /y "songs.example.txt" "songs.txt" >nul
        echo Created songs.txt. Edit the list and run again.
        pause
        exit /b 0
    )
)

pip show yt-dlp >nul 2>&1
if errorlevel 1 (
    echo Installing yt-dlp...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: failed to install yt-dlp.
        pause
        exit /b 1
    )
)

python download.py
echo.
pause
