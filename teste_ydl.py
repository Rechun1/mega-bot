import youtube_dl

#ydl_opts = {'format': 'mp4'}

ydl_opts = {
    'format': 'bestaudio/best',
    #'outtmpl': '/audiotests/',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=G3dwKAHPC_s'])
