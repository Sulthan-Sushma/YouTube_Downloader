import json
import base64
import youtube_dl

def handler(event, context):
    try:
        print(f"Received event: {event}")  # Debug log
        body = json.loads(event.get('body', '{}'))
        video_url = body.get('url')
        if not video_url:
            print("Error: No URL provided")  # Debug log
            return {'statusCode': 400, 'body': 'No URL provided'}

        print(f"Processing URL: {video_url}")  # Debug log
        ydl_opts = {'outtmpl': '/tmp/video.mp4', 'format': 'best'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        with open('/tmp/video.mp4', 'rb') as f:
            file_data = f.read()
            print(f"File size: {len(file_data)} bytes")  # Debug log

        return {
            'statusCode': 200,
            'body': base64.b64encode(file_data).decode('utf-8'),
            'headers': {
                'Content-Type': 'video/mp4',
                'Content-Disposition': 'attachment; filename="video.mp4"'
            },
            'isBase64Encoded': True
        }
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Debug log
        return {'statusCode': 500, 'body': str(e)}