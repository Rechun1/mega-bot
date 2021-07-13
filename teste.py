import discord
from discord.ext import commands
import discord.ext.commands
import os

bot = commands.Bot(command_prefix='>')

ROOT_PATH = os.curdir
audio_files = f'{ROOT_PATH}/audio/'
client = commands.Bot(command_prefix='natan ')

@bot.command()
async def play(ctx, url:str):
    channel_name = ctx.author.voice.channel
    await ctx.send(f'Nome do canal: {channel_name}, pesquisa: {url}')
    print(channel_name)
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    print(voice_channel)
    if voice_channel is not None:
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        print(voice)
        voice.play(discord.FFmpegPCMAudio(f'{audio_files}/gaikoz.mp3'))
    else:
        await ctx.send(f'Algum erro ocorreu')
@bot.command()
async def dc(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.send(f'Saindo fora maluco')
    await voice.disconnect()

bot.run('ODY0MjY4MTcyMzY1NjYwMjAw.YOy-dQ.gM6ksIhcrWss2ai4uyjOaoRV12M')