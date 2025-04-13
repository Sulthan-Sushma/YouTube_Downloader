import youtube_dl

def handler(event, context):
    try:
        # Parse the event body (Netlify passes JSON as a string)
        body = event.get('body')
        if not body:
            return {'statusCode': 400, 'body': 'No body provided'}
        data = eval(body)  # Caution: Use json.loads for production safety
        video_url = data.get('url')
        if not video_url:
            return {'statusCode': 400, 'body': 'No URL provided'}

        # Download the video
        ydl_opts = {'outtmpl': '/tmp/video.mp4'}  # Use /tmp for temporary storage
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Read and return the file as a binary response
        with open('/tmp/video.mp4', 'rb') as f:
            file_data = f.read()
        return {
            'statusCode': 200,
            'body': file_data.decode('latin1'),  # Encode binary data as string
            'headers': {
                'Content-Type': 'video/mp4',
                'Content-Disposition': 'attachment; filename="video.mp4"'
            },
            'isBase64Encoded': False
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}