import json
import discord
from discord.ext import commands

with open(".data/settings.json","r") as settingsFile:
    settings = json.load(settingsFile)
    token = settings["token"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def testcommand(ctx):
    await ctx.send("Ths is soo test")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('test'):
        await message.channel.send(f"Hello world")

    await bot.process_commands(message)

bot.run(token)
