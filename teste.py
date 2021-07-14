import discord
from discord.ext import commands
import discord.ext.commands
import os
import random
import json

bot = commands.Bot(command_prefix='>')

ROOT_PATH = os.curdir
audio_files = f'{ROOT_PATH}/audio/'
random_audio_files = 'E:/Playlist Skype/'

pregadas = 0

def pregar():
    global pregadas
    pregadas += 1
    return pregadas

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
        voice.play(discord.FFmpegPCMAudio(f'{audio_files}/Zé.mp3'))
    else:
        await ctx.send(f'Deu erro aqui caraio')


@bot.command()
async def rplay(ctx):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    random_song = random.choice(os.listdir(random_audio_files))
    if voice_channel is not None and not is_connected(ctx):
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(f'{random_audio_files}/{random_song}'))
        await ctx.send(f'Aleatório escolhido: {random_song}')
    elif is_connected(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(f'{random_audio_files}/{random_song}'))
        await ctx.send(f'Aleatório escolhido: {random_song}')


def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        try:
            voice.stop()
        except:
            await ctx.send(f'Deu erro aqui caraio')


@bot.command()
async def dc(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.send(f'Saindo fora maluco')
    await voice.disconnect()


@bot.command()
async def rule(ctx):
    with open(f'{ROOT_PATH}/rules/rules.json') as e:
        rules = json.load(e)
    rule = random.choice(rules['rules'])
    await ctx.send(rule)


@bot.command()
async def nail(ctx):
    await ctx.send(f'A tábua já foi pregada {str(pregar())} vezes desde que estou online.')


@bot.command()
async def guinf(ctx):
    user = ctx.author.display_name
    await ctx.send(f'Olá {str(user)}, o Guinf é macho')

bot.run('ODY0MjY4MTcyMzY1NjYwMjAw.YOy-dQ.gM6ksIhcrWss2ai4uyjOaoRV12M')
