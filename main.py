import json
import discord
from discord.ext import commands
import os
from utils.youtube import youtube
from utils.player import endOfMusic

botDir = os.getcwd()
# 0 is a placeholder value
voice = {"vc":0, "isPlaying":False,"queue":[]}

with open(".data/settings.json","r") as settingsFile:
    settings = json.load(settingsFile)
    token = settings["token"]

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def startsong(ctx,songUrl):
    if ctx.author.voice:
        if not voice["isPlaying"]:
            await ctx.send("Holdup, setting up")
            channel = ctx.author.voice.channel
            songData = youtube.getMusicData(songUrl)

            if not os.path.isfile(f"{botDir}/.cache/music/{songData["id"]}.opus"):
                youtube.downloadSong(songUrl,botDir)

            client = await channel.connect()
            voice["vc"] = client
            voice["isPlaying"] = True

            source = await discord.FFmpegOpusAudio.from_probe(f".cache/music/{songData["id"]}.opus")
            client.play(source)
            await ctx.send("Done")
        else:
            songData = youtube.getMusicData(songUrl)
            voice["queue"].append(songData["id"])
            await ctx.send(f"Something is already plaing, adding {songData["name"]} to queue")
    else:
        await ctx.send('Cant play, you are not on any voice channel')

# wow how do you work
@bot.command()
async def pause(ctx):
    if voice["isPlaying"]:
        vc = voice["vc"]
        vc.pause()
        await ctx.send("Music is paused")
    else:
        await ctx.send("Nothing is playing")

@bot.command()
async def resume(ctx):
    if voice["isPlaying"]:
        vc = voice["vc"]
        vc.resume()
        await ctx.send("Resuming")
    else:
        await ctx.send("Nothing is playing")

@bot.command()
async def stop(ctx):
    if voice["isPlaying"]:
        vc = voice["vc"]
        vc.stop()
        await ctx.send("Stoping")
        await vc.disconnect()
        # same empty val 0 as on the beginning of this file
        voice["vc"] = 0
        voice["isPlaying"] = False
        voice["queue"] = []
    else:
        await ctx.send("Nothing is playing")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('test'):
        await message.channel.send(f"Hello world")

    await bot.process_commands(message)

bot.run(token)
