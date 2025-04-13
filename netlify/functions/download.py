from flask import Flask, request, send_file
import youtube_dl

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get('url')
        if not video_url:
            return {"error": "No URL provided"}, 400
        ydl_opts = {'outtmpl': '/tmp/video.mp4'}  # Use /tmp for Netlify temp storage
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return send_file('/tmp/video.mp4', as_attachment=True, download_name='video.mp4')
    except Exception as e:
        return {"error": str(e)}, 500

def handler(event, context):
    with app.test_request_context(
        path=event.path,
        method=event.httpMethod,
        headers=event.headers,
        data=event.body
    ):
        return app.dispatch_request()