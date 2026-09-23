from utils.youtube import youtube
import os
import discord
import asyncio

async def startSong(botDir,voice,ctx):
    # first song in the queue
    song = voice["queue"][0]
    # remove fist song in the queue so the first is new song
    voice["queue"].pop(0)

    if not os.path.isfile(f"{botDir}/.cache/music/{song["id"]}.opus"):
        youtube.downloadSong(song["url"],botDir)

    client = voice["vc"]

    voice["isPlaying"] = True

    source = await discord.FFmpegOpusAudio.from_probe(f".cache/music/{song["id"]}.opus")
    client.play(source,after=lambda error: onSongEnd(botDir,voice,ctx,error))
    await ctx.send(f"Playing {song["title"]} by {song["author"]}")

def onSongEnd(botDir,voice,ctx,error):
    try:
        loop = voice["vc"].client.loop

        asyncio.run_coroutine_threadsafe(
            startSong(botDir, voice,ctx),
            loop
        )
    except Exception as err:
        print(err)
