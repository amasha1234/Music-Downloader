import pytubefix as pt
import customtkinter
import os
import subprocess
import re
import hashlib

root = customtkinter.CTk()
root.geometry("600x250")
root.title("Music Downloader")

# Labels
title = customtkinter.CTkLabel(root, text="Music Downloader", font=("Helvetica", 18))
title.place(x=230, y=30)

label_one = customtkinter.CTkLabel(root, text="", font=("Helvetica", 16))
label_one.place(x=260, y=190)

# Entry
url_entry = customtkinter.CTkEntry(root, placeholder_text="Enter the URL", width=300)
url_entry.place(x=155, y=80)

# Function to sanitize and shorten filename
def sanitize_and_shorten_title(title, max_length=50):
    # Remove special characters
    sanitized_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', title)
    # Shorten title if it's too long
    if len(sanitized_title) > max_length:
        # Append a short hash to ensure uniqueness
        hash_suffix = hashlib.md5(sanitized_title.encode()).hexdigest()[:6]
        sanitized_title = sanitized_title[:max_length] + '_' + hash_suffix
    return sanitized_title

# Functions
def download():
    label_one.configure(text="")
    url = url_entry.get()
    yt = pt.YouTube(url)
    stream = yt.streams.get_audio_only()

    # Get and sanitize the title
    original_title = yt.title
    shortened_title = sanitize_and_shorten_title(original_title)

    # Define input and output paths
    download_path = fr"D:\Python\My Beginner Python\Music Downloader"
    input_path = os.path.join(download_path, f"{shortened_title}.mp4")
    output_path = os.path.join(download_path, f"{shortened_title}.mp3")

    # Download with the shortened filename
    stream.download(output_path=download_path, filename=f"{shortened_title}.mp4")

    # FFmpeg command
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "128k",
        "-ar", "44100",
        "-y",
        output_path
    ]

    try:
        # Run the FFmpeg command
        subprocess.run(ffmpeg_cmd, check=True)
        label_one.configure(text="Completed!", text_color="green")
    except subprocess.CalledProcessError as e:
        print(f"Conversion Failed: {e}")

    # Optionally, delete the original MP4 file after conversion
    if os.path.exists(input_path):
        os.remove(input_path)

# Button
download_button = customtkinter.CTkButton(root, text="Download", width=90, command=download)
download_button.place(x=256, y=140)

root.mainloop()