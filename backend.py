# python backend.py - Backend
# python fpython -m http.server 5500 - Frontend
import os
import yt_dlp
from fastapi import FastAPI, Form,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse



app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the current directory
DOWNLOAD_FOLDER = r"C:\Users\sulth\Videos\Captures"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.post("/download")
def download_video(link: str = Form(...)):
    youtube_dl_options = {
        "format": "best",  # Selects the best quality available
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, f"Video{link[-11:]}.mp4")  # Save video as VideoXXXXXX.mp4 in the current directory
    }
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([link])
        return {"status": "success", "filePath": os.path.join(DOWNLOAD_FOLDER, f"Video{link[-11:]}.mp4")}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




