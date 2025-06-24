import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from downloader.core import download_video
import threading
import os
import time

def run_gui():
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            path_var.set(folder)

    def format_eta(seconds):
        if seconds is None:
            return "--:--"
        seconds = int(seconds)
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02}:{mins:02}:{secs:02}" if hrs > 0 else f"{mins:02}:{secs:02}"

    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            percent = int(downloaded * 100 / total_bytes) if total_bytes else 0
            eta_str = format_eta(d.get('eta'))

            progressbar["value"] = percent
            status_label.config(text=f"⬇️ Downloading... {percent}% | Time Remaining: {eta_str}")
            window.update_idletasks()

        elif d['status'] == 'finished':
            progressbar["value"] = 100
            filename = os.path.basename(d.get('filename', ''))
            status_label.config(text=f"✅ Finished: {filename}")

    def threaded_download():
        try:
            download_video(
                url_var.get(),
                path_var.get(),
                res_var.get(),
                audio_var.get(),
                progress_callback=progress_hook
            )
        except Exception as e:
            messagebox.showerror("Download Failed", str(e))
            status_label.config(text="❌ Failed")
        finally:
            download_button.config(state="normal")
            progressbar.pack_forget()

    def start_download():
        if not url_var.get():
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        download_button.config(state="disabled")
        progressbar["value"] = 0
        progressbar.pack(pady=(5, 5))  # Only show when downloading
        status_label.config(text="⬇️ Starting download...")
        window.update_idletasks()

        threading.Thread(target=threaded_download, daemon=True).start()

    def enable_right_click(entry):
        def do_popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        menu = tk.Menu(window, tearoff=0, bg="#2d2d44", fg="white", font=("Segoe UI", 10))
        menu.add_command(label="Cut", command=lambda: entry.event_generate("<<Cut>>"))
        menu.add_command(label="Copy", command=lambda: entry.event_generate("<<Copy>>"))
        menu.add_command(label="Paste", command=lambda: entry.event_generate("<<Paste>>"))
        entry.bind("<Button-3>", do_popup)

    # Main window
    window = tk.Tk()
    window.title("🎬 YouTube Video Downloader by github.com/AhmedShaikh0")
    window.geometry("900x500")
    window.configure(bg="#1e1e2f")

    # Optional: set icon if available
    # window.iconbitmap("assets/icon.ico")

    font = ("Segoe UI", 11)
    style_opts = {'bg': "#1e1e2f", 'fg': "#ffffff", 'font': font}
    entry_opts = {'bg': "#2d2d44", 'fg': "#ffffff", 'insertbackground': "#ffffff", 'font': font, 'relief': 'flat'}

    # YouTube URL
    tk.Label(window, text="YouTube URL", **style_opts).pack(pady=(20, 5))
    url_var = tk.StringVar()
    url_entry = tk.Entry(window, textvariable=url_var, width=45, **entry_opts)
    url_entry.pack()
    enable_right_click(url_entry)

    # Save to Folder
    tk.Label(window, text="Save to Folder", **style_opts).pack(pady=(15, 5))
    path_frame = tk.Frame(window, bg="#1e1e2f")
    path_frame.pack()
    path_var = tk.StringVar(value="downloads/")
    path_entry = tk.Entry(path_frame, textvariable=path_var, width=30, **entry_opts)
    path_entry.pack(side=tk.LEFT, padx=(0, 5))
    enable_right_click(path_entry)
    tk.Button(path_frame, text="Browse", command=browse_folder, bg="#3a3a5a", fg="white", font=font).pack(side=tk.LEFT)

    # Resolution Dropdown
    tk.Label(window, text="Resolution", **style_opts).pack(pady=(15, 5))
    res_var = tk.StringVar(value="720p")
    resolution_menu = tk.OptionMenu(window, res_var, "1080p", "720p", "480p", "360p")
    resolution_menu.config(
        bg="#2d2d44", fg="white", font=font,
        activebackground="#007acc", activeforeground="white",
        bd=0, relief=tk.FLAT, highlightthickness=0
    )
    resolution_menu["menu"].config(
        bg="#2d2d44", fg="white", font=font,
        activebackground="#007acc", activeforeground="white",
        bd=0
    )
    resolution_menu.pack()

    # Audio Only Checkbox
    audio_var = tk.BooleanVar()
    tk.Checkbutton(window, text="Audio Only (MP3)", variable=audio_var,
                   bg="#1e1e2f", fg="white", font=font, selectcolor="#1e1e2f").pack(pady=(10, 5))

    # Download Button
    download_button = tk.Button(window, text="⬇️ Download", command=start_download,
                                bg="#007acc", fg="white", font=("Segoe UI", 12, "bold"),
                                padx=10, pady=5)
    download_button.pack(pady=(15, 5))

    # Progress Bar and Status
    progressbar = ttk.Progressbar(window, orient="horizontal", mode="determinate", length=300)
    status_label = tk.Label(window, text="", **style_opts)
    status_label.pack()

    window.mainloop()
