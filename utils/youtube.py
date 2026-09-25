import yt_dlp as ytdlp

class youtube:
    def __init__(self,cookies):
        self._cookiesState = cookies

    def downloadSong(self,url,botDir):
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

        if self._cookiesState == True:
            ytdlpOptions["cookiefile"] = ".data/cookies.txt"

        urlList = [url]
        ytdlp.YoutubeDL(ytdlpOptions).download(urlList)

    def getMusicData(self,url):
        musicData = {}

        ydlpOpts = {
            'quiet': True,
            'skip_download': True,
        }

        if self._cookiesState == True:
            ytdlpOptions["cookiefile"] = ".data/cookies.txt"

        with ytdlp.YoutubeDL(ydlpOpts) as ydl:
            info = ydl.extract_info(url, download=False)

        musicData["id"] = info["id"]
        musicData["title"] = info["title"]
        musicData["author"] = info["uploader"]

        return musicData

