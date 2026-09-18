import json
import discord
from discord.ext import commands
import os
from utils.youtube import downloadSong

botDir = os.getcwd()

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
        await ctx.send("Holdup, setting up")
        channel = ctx.author.voice.channel
        downloadSong(songUrl,botDir)
        client = await channel.connect()
        # source = await discord.FFmpegOpusAudio.from_probe("")
        client.play(source)
        await ctx.send("Done")
    else:
        await ctx.send('Cant play, you are not on any voice channel')




@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('test'):
        await message.channel.send(f"Hello world")

    await bot.process_commands(message)

bot.run(token)
