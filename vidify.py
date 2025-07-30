import customtkinter as ctk
import tkinter.messagebox
import threading
import subprocess
import re
import tkinter as tk
import requests
from PIL import Image, ImageTk
import io
import os

# API anahtarını apikey.txt dosyasından oku
if os.path.exists("apikey.txt"):
    with open("apikey.txt", "r") as file:
        YOUTUBE_API_KEY = file.read().strip()
else:
    tkinter.messagebox.showerror("API Key Missing", "apikey.txt not found. Please create the file and add your YouTube API key.")
    exit()

# Tema ve pencere ayarları
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Vidify - Video Downloader")
app.geometry("1024x700")
app.minsize(800, 600)
app.iconbitmap("vidify.ico")  # ← İKON BURADA EKLENDİ

# Grid yapılandırması
app.grid_rowconfigure(2, weight=1)
for i in [0, 1, 3, 4, 5, 6, 7]:
    app.grid_rowconfigure(i, weight=0)
app.grid_columnconfigure(0, weight=1)

thumbnail_refs = []

def download_video():
    url = url_entry.get()
    format_choice = format_option.get()
    quality_choice = quality_option.get()

    if not url:
        tkinter.messagebox.showerror("Error", "Please enter a video URL.")
        return

    status_label.configure(text="Downloading...", text_color="white")
    progress_bar.set(0)

    if format_choice == "MP3":
        command = ["yt-dlp", "-x", "--audio-format", "mp3", url]
    else:
        command = ["yt-dlp", "-f", f"bestvideo[height<={quality_choice}]+bestaudio/best", "-o", "%(title)s.%(ext)s", url]

    def run():
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                print(line.strip())
                match = re.search(r'\[download\]\s+(\d{1,3}\.\d)%', line)
                if match:
                    percent = float(match.group(1))
                    progress_bar.set(percent / 100.0)
            process.wait()

            if process.returncode == 0:
                status_label.configure(text="✅ Download completed successfully.", text_color="green")
            else:
                status_label.configure(text="❌ Download failed. Please check the link.", text_color="red")

        except Exception as e:
            status_label.configure(text=f"❌ Error: {str(e)}", text_color="red")

    threading.Thread(target=run).start()

def perform_search():
    query = search_entry.get().strip()
    if not query:
        return

    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 6,
        "type": "video"
    }

    response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
    results = response.json()

    for widget in result_frame.winfo_children():
        widget.destroy()
    thumbnail_refs.clear()

    if "items" not in results:
        tkinter.messagebox.showerror("API Error", "No results found.")
        return

    for index, item in enumerate(results["items"]):
        video_data = item.get("id", {})
        video_id = video_data.get("videoId")
        if not video_id:
            continue

        title = item["snippet"].get("title", "No Title")
        channel = item["snippet"].get("channelTitle", "Unknown Channel")
        thumbnail_url = item["snippet"]["thumbnails"]["medium"]["url"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        image_data = requests.get(thumbnail_url).content
        image = Image.open(io.BytesIO(image_data)).resize((160, 90))
        tk_image = ImageTk.PhotoImage(image)
        thumbnail_refs.append(tk_image)

        card = ctk.CTkFrame(result_frame)
        card.pack(fill="x", padx=5, pady=5)

        label = tk.Label(card, image=tk_image)
        label.grid(row=0, column=0, rowspan=2, padx=10)

        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13), anchor="w")
        title_label.grid(row=0, column=1, sticky="w", padx=5)

        channel_label = ctk.CTkLabel(card, text=f"by {channel}", font=ctk.CTkFont(size=11), anchor="w")
        channel_label.grid(row=1, column=1, sticky="w", padx=5)

        def select_link(url=video_url):
            url_entry.delete(0, tk.END)
            url_entry.insert(0, url)
            status_label.configure(text="🎯 Video selected from search.", text_color="white")

        select_button = ctk.CTkButton(card, text="Select", command=select_link, width=80)
        select_button.grid(row=0, column=2, rowspan=2, padx=10)

# Başlık
title_label = ctk.CTkLabel(app, text="🎬 Vidify - Video Downloader", font=ctk.CTkFont(size=20, weight="bold"))
title_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

# Arama çubuğu
search_frame = ctk.CTkFrame(app)
search_frame.grid(row=1, column=0, sticky="ew", padx=10)

search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search YouTube...")
search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10), pady=5)

search_button = ctk.CTkButton(search_frame, text="🔍 Search", command=perform_search)
search_button.pack(side="right", pady=5)

# Arama sonuçları
result_frame = ctk.CTkScrollableFrame(app)
result_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))

# URL girişi
url_entry = ctk.CTkEntry(app, placeholder_text="Paste YouTube / TikTok URL here...")
url_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# Format ve kalite seçenekleri
options_frame = ctk.CTkFrame(app)
options_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

format_option = ctk.CTkOptionMenu(options_frame, values=["MP4", "MP3"])
format_option.pack(side="left", padx=10, pady=5)
format_option.set("MP4")

quality_option = ctk.CTkOptionMenu(options_frame, values=["144", "240", "360", "480", "720", "1080"])
quality_option.pack(side="left", padx=10, pady=5)
quality_option.set("720")

# Download butonu
download_button = ctk.CTkButton(app, text="⬇ Download", command=download_video)
download_button.grid(row=5, column=0, pady=(10, 5), sticky="ew", padx=10)

# İlerleme çubuğu
progress_bar = ctk.CTkProgressBar(app)
progress_bar.set(0)
progress_bar.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

# Durum etiketi
status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=14))
status_label.grid(row=7, column=0, padx=10, pady=(10, 15), sticky="ew")

app.mainloop()
