# Run this server with:
# cd "C:\Users\sulth\OneDrive\เอกสาร\Major projects\YouTube_Downloader\backend"
# python -m uvicorn backend:app --reload

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI()

# Enable CORS for frontend running on localhost (e.g., 127.0.0.1:5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://127.0.0.1:5500"] to restrict access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_video(link: str, filename: str):
    save_path = r"C:\Users\sulth\Videos\videos of utube"
    os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists

    ydl_opts = {
        'outtmpl': os.path.join(save_path, f'{filename}.mp4'),
        'format': '18',  # Safer format than 'best' due to signature issues
        'quiet': False,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

@app.post("/download")
async def download(link: str = Form(...)):
    try:
        download_video(link, "downloaded_video")
        return {"status": "success", "message": "Video downloaded successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Download failed: {str(e)}"}
