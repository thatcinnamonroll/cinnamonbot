import json
import discord
from discord.ext import commands
import os
from utils.youtube import youtube
from utils.playerHelper import startSong, stopPlayer
from utils.botHelper import ensureCacheDir, ensureDataDir

ensureCacheDir()
ensureDataDir()

botDir = os.getcwd()

with open(".data/settings.json","r") as settingsFile:
    settings = json.load(settingsFile)
    token = settings["token"]
    allowedSongUrls = settings["allowedSongUrls"]
    cookiesState = settings["cookies"]

yt = youtube(cookiesState)

# 0 is a placeholder value
voice = {"vc":0, "isPlaying":False,"queue":[],"yt-man":yt}

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def play(ctx,songUrl):
    if not songUrl.startswith(tuple(allowedSongUrls)):
        await ctx.send("That url is not supported, only supported services are youtube and soundcloud")
        return

    if ctx.author.voice:
        await ctx.send("Holdup, setting up")
        song = youtube.getMusicData(songUrl)
        song["url"] = songUrl
        voice["queue"].append(song)
        # if vc is 0 then bot is not connected to any voice channel
        if voice["vc"] == 0:
            channel = ctx.author.voice.channel
            client = await channel.connect()
            voice["vc"] = client
        if not voice["isPlaying"]:
            await startSong(botDir,voice,ctx)
    else:
        await ctx.send("Cant play, you are not on any voice channel")

@bot.command()
async def queue(ctx):
    if voice["queue"] == []:
        await ctx.send("Queue is empty, feel free to add some songs :)")
        return

    msgList = ["SONGS IN QUEUE: \n"]
    for song in voice["queue"]:
        msgList.append(f"{song["title"]} -- by -- {song["author"]} \n")
    msg = "".join(msgList)
    await ctx.send(msg)

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
        stopPlayer(voice,ctx)
    else:
        await ctx.send("Nothing is playing")

@bot.command()
async def botsay(ctx):
    msg = ctx.message.content
    await ctx.message.delete()
    # cutting "/botsay " from message
    await ctx.send(msg[8:])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('test'):
        await message.channel.send(f"Hello world")

    await bot.process_commands(message)

bot.run(token)
