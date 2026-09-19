import yt_dlp as ytdlp

class youtube:
    def downloadSong(url,botDir):
        ytdlpOptions = {'extract_flat': 'discard_in_playlist',
        'format': 'bestaudio/best',
        'fragment_retries': 10,
        'outtmpl': {'default': '%(id)s.%(ext)s'},
        'ignoreerrors': 'only_download',
        'paths': {'home': f"{botDir}/.cache/music"},
        'postprocessors': [{'key': 'FFmpegExtractAudio',
                            'nopostoverwrites': False,
                            'preferredcodec': 'opus',
                            'preferredquality': '5'},
                            {'key': 'FFmpegConcat',
                            'only_multi_video': True,
                            'when': 'playlist'}],
        'retries': 10}

        urlList = [url]
        ytdlp.YoutubeDL(ytdlpOptions).download(urlList)

    def getMusicData(url):
        musicData = {}

        ydlpOpts = {
            'quiet': True,
            'skip_download': True,
        }

        with ytdlp.YoutubeDL(ydlpOpts) as ydl:
            info = ydl.extract_info(url, download=False)

        musicData["id"] = info["id"]
        musicData["title"] = info["title"]
        musicData["author"] = info["uploader"]

        return musicData

