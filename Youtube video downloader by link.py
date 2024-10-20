import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp
import threading

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link")
        return
    
    # Choose the download location
    save_path = filedialog.askdirectory()
    if not save_path:
        return

    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'progress_hooks': [hook],
    }

    # Download in a separate thread to avoid freezing the UI
    def download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                # Update progress once the download is finished
                update_progress_bar(100)  # Mark as finished
                # Inform the user about the completion
                messagebox.showinfo("Download Complete", "Video has been downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Download Failed", str(e))

    download_thread = threading.Thread(target=download)
    download_thread.start()
    messagebox.showinfo("Download Started", "Downloading...")

def hook(d):
    if d['status'] == 'downloading':
        # Update the progress bar based on the downloaded bytes
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)  # Avoid division by zero
        progress = downloaded / total * 100
        update_progress_bar(progress)

def update_progress_bar(value):
    # Update progress bar safely
    progress_bar.config(value=value)
    progress_bar.update_idletasks()  # Force the UI to update

def create_app():
    # Create the main window
    app = tk.Tk()
    app.title("YouTube Video Downloader")
    app.geometry("500x300")  # Increased height for credit label
    app.config(bg='#333')  # Dark mode
    
    # Credit label at the top
    credit_label = tk.Label(app, text="Made by agentfoxies", bg='#333', fg='white', font=('Arial', 14, 'bold'))
    credit_label.pack(pady=5)

    # URL label and entry
    url_label = tk.Label(app, text="YouTube Video URL:", bg='#333', fg='white', font=('Arial', 12))
    url_label.pack(pady=10)
    
    global url_entry
    url_entry = tk.Entry(app, width=50, font=('Arial', 14), bg='#555', fg='white')
    url_entry.pack(pady=5)

    # Download button
    download_button = tk.Button(app, text="Download Video", command=download_video, bg='#1db954', fg='white', font=('Arial', 12))
    download_button.pack(pady=20)

    # Progress bar
    global progress_bar
    progress_bar = ttk.Progressbar(app, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(pady=20)
    
    # Run the app
    app.mainloop()

if __name__ == '__main__':
    create_app()