import discord
import os
from discord.ext import commands

ROOT_PATH = os.curdir
audio_files = f'{ROOT_PATH}/audio/'
client = commands.Bot(command_prefix='>')

@client.command()
async def play(ctx, url:str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Geral')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio(f'{audio_files}/gaikoz.mp3'))

@client.command()
async def dc(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()


client.run('ODY0MjY4MTcyMzY1NjYwMjAw.YOy-dQ.gM6ksIhcrWss2ai4uyjOaoRV12M')