### 📄 `README.md` – İngilizce Açıklama:

```markdown
# Vidify - Video Downloader

Vidify is a desktop application for downloading videos or audio (MP4/MP3) from YouTube or TikTok.  
Built with **CustomTkinter**, it provides a clean GUI with integrated YouTube search via the **YouTube Data API**.

## 🎯 Features

- 🔍 Search videos directly using YouTube API
- 📥 Download in MP4 (video) or MP3 (audio)
- 🎚️ Choose video quality (144p – 1080p)
- ✅ Clean, modern UI with real-time download progress
- 🎞️ Displays video thumbnails and titles
- 💾 Auto-fetch YouTube API key from `apikey.txt`

## 📦 Requirements

See `requirements.txt`:

## 🚀 How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Create an `apikey.txt` file in the project folder with your YouTube API key:
    ```
    YOUR_API_KEY_HERE
    ```

3. Run the application:
    ```bash
    python main.py
    ```

## 🔒 Notes

- Make sure `yt-dlp` is installed and in your system path.
- Tested on Windows with Python 3.10+

---

Created with ❤️ by Burak
