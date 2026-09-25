from utils.youtube import youtube
import os
import discord
import asyncio

async def stopPlayer(voice,ctx):
    vc = voice["vc"]
    vc.stop()
    await ctx.send("Stopping playing")
    await vc.disconnect()
    # same empty val 0 as on the beginning of this file
    voice["vc"] = 0
    voice["isPlaying"] = False
    voice["queue"] = []

async def startSong(botDir,voice):
    # first song in the queue
    song = voice["queue"][0]
    # remove fist song in the queue so the first is new song
    voice["queue"].pop(0)
    yt = voice["yt-man"]

    if not os.path.isfile(f"{botDir}/.cache/music/{song["id"]}.opus"):
        yt.downloadSong(song["url"],botDir)

    client = voice["vc"]

    voice["isPlaying"] = True

    source = await discord.FFmpegOpusAudio.from_probe(f".cache/music/{song["id"]}.opus")
    client.play(source,after=lambda error: onSongEnd(botDir,voice,ctx,error))
    await ctx.send(f"Playing {song["title"]} by {song["author"]}")

def onSongEnd(botDir,voice,ctx,error):
    loop = voice["vc"].client.loop
    if not voice["queue"] == []:
        try:
            asyncio.run_coroutine_threadsafe(
                startSong(botDir, voice,ctx),
                loop
            )
        except Exception as err:
            print(err)
    else:
        asyncio.run_coroutine_threadsafe(
            stopPlayer(voice,ctx),
            loop
        )
