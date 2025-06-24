import yt_dlp
import os

def download_video(url, path='downloads/', resolution='720p', audio_only=False, progress_callback=None):
    """
    Downloads a YouTube video using yt_dlp with optional resolution and audio-only mode.

    Args:
        url (str): YouTube video URL.
        path (str): Folder to save the downloaded file.
        resolution (str): Maximum resolution (e.g., '1080p', '720p').
        audio_only (bool): If True, download as MP3.
        progress_callback (function): yt_dlp progress hook.
    """
    if not os.path.exists(path):
        os.makedirs(path)

    ydl_opts = {
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_callback] if progress_callback else [],
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': False,
    }

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        max_res = resolution.rstrip('p')
        ydl_opts.update({
            'format': f"bestvideo[height<={max_res}]+bestaudio/best",
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print("[ERROR] yt_dlp failed:", e)
        raise
