# python backend.py - Backend
# python fpython -m http.server 5500 - Frontend
from flask import Flask, request, send_file
import youtube_dl

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')
    ydl_opts = {'outtmpl': 'video.mp4'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return send_file('video.mp4', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)