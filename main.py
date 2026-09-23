import json
import discord
from discord.ext import commands
import os
from utils.youtube import youtube
from utils.playerHelper import startSong

botDir = os.getcwd()
# 0 is a placeholder value
voice = {"vc":0, "isPlaying":False,"queue":[]}

with open(".data/settings.json","r") as settingsFile:
    settings = json.load(settingsFile)
    token = settings["token"]
    allowedSongUrls = settings["allowedSongUrls"]

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
            await startSong(botDir,voice)
    else:
        await ctx.send("Cant play, you are not on any voice channel")

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
