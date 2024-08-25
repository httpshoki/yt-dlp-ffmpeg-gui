import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class YTDLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("yt-dlp GUI with FFmpeg")
        
        # Link Label and Entry
        self.link_label = tk.Label(root, text="Video URL:")
        self.link_label.grid(row=0, column=0, padx=10, pady=10)
        self.link_entry = tk.Entry(root, width=50)
        self.link_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Destination Folder
        self.dest_label = tk.Label(root, text="Destination Folder:")
        self.dest_label.grid(row=1, column=0, padx=10, pady=10)
        self.dest_entry = tk.Entry(root, width=50)
        self.dest_entry.grid(row=1, column=1, padx=10, pady=10)
        self.dest_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.dest_button.grid(row=1, column=2, padx=10, pady=10)
        
        # Download Button
        self.download_button = tk.Button(root, text="Download", command=self.download_video)
        self.download_button.grid(row=2, column=1, padx=10, pady=10)
        
        # Convert Video Checkbox
        self.convert_var = tk.IntVar()
        self.convert_checkbox = tk.Checkbutton(root, text="Convert to MP4 using FFmpeg", variable=self.convert_var)
        self.convert_checkbox.grid(row=3, column=1, padx=10, pady=10)
        
        # Progress Label
        self.progress_label = tk.Label(root, text="")
        self.progress_label.grid(row=4, column=1, padx=10, pady=10)
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder_selected)
    
    def download_video(self):
        url = self.link_entry.get()
        dest_folder = self.dest_entry.get()
        
        if not url or not dest_folder:
            messagebox.showerror("Error", "Please enter a valid URL and select a destination folder.")
            return
        
        # Download video using yt-dlp
        self.progress_label.config(text="Downloading video...")
        try:
            download_command = ["yt-dlp", "-o", os.path.join(dest_folder, "%(title)s.%(ext)s"), url]
            subprocess.run(download_command, check=True)
            self.progress_label.config(text="Download completed!")
        except subprocess.CalledProcessError as e:
            self.progress_label.config(text="Download failed.")
            messagebox.showerror("Error", f"Download failed: {e}")
            return
        
        if self.convert_var.get():
            self.convert_video(dest_folder)
    
    def convert_video(self, folder):
        # Convert video to MP4 using FFmpeg
        self.progress_label.config(text="Converting video to MP4...")
        try:
            for file_name in os.listdir(folder):
                if file_name.endswith((".mkv", ".webm", ".flv")):
                    input_file = os.path.join(folder, file_name)
                    output_file = os.path.splitext(input_file)[0] + ".mp4"
                    convert_command = ["ffmpeg", "-i", input_file, output_file]
                    subprocess.run(convert_command, check=True)
                    os.remove(input_file)  # Remove the original file
            self.progress_label.config(text="Conversion completed!")
        except subprocess.CalledProcessError as e:
            self.progress_label.config(text="Conversion failed.")
            messagebox.showerror("Error", f"Conversion failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YTDLApp(root)
    root.mainloop()
