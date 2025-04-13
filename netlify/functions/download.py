import youtube_dl
import base64

def handler(event, context):
    try:
        body = event.get('body')
        if not body:
            return {'statusCode': 400, 'body': 'No body provided'}
        data = eval(body)  # Replace with json.loads for safety
        video_url = data.get('url')
        if not video_url:
            return {'statusCode': 400, 'body': 'No URL provided'}

        ydl_opts = {'outtmpl': '/tmp/video.mp4'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        with open('/tmp/video.mp4', 'rb') as f:
            file_data = f.read()
        return {
            'statusCode': 200,
            'body': base64.b64encode(file_data).decode('utf-8'),  # Base64 encode binary
            'headers': {
                'Content-Type': 'video/mp4',
                'Content-Disposition': 'attachment; filename="video.mp4"'
            },
            'isBase64Encoded': True  # Indicate base64 encoding
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}