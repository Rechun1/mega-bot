import discord
from discord.ext import commands
import discord.ext.commands
import os
import random
import json
import Functions as fn
import asyncio

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

ROOT_PATH = os.curdir
audio_files = f'{ROOT_PATH}/audio/'
big_audio_files = 'E:/playlist_skype_full/'
random_audio_files = 'E:/Playlist Skype/'
random_accel_audio_files = 'E:/Playlist Skype2x/'
random_accel_big_audio_files = 'E:/playlist_skype_full2x/'

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
        try:
            await voice_channel.connect()
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            print(voice)
            voice.play(discord.FFmpegPCMAudio(f'{audio_files}/mcgorila2.mp3'))
        except:
            await ctx.send(f'Deu erro aqui caraio')


@bot.command()
async def rplay(ctx):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    random_song = fn.find_random_audio(big_audio_files)
    if voice_channel is not None and not fn.is_connected(ctx):
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(random_song))
        await ctx.send(f'Aleatório escolhido: {random_song.split("/")[2]}')
        return
    if fn.is_connected(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(random_song))
            await ctx.send(f'Aleatório escolhido: {random_song.split("/")[2]}')
            return
        voice.stop()
        voice.play(discord.FFmpegPCMAudio(random_song))
        await ctx.send(f'Aleatório escolhido: {random_song.split("/")[2]}')
        return


@bot.command()
async def rrplay(ctx):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    random_song = fn.find_random_audio(random_accel_big_audio_files)
    print(random_song)
    if voice_channel is not None and not fn.is_connected(ctx):
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(random_song))
        await ctx.send(f'Aleatório escolhido: {random_song.split}')
        return
    if fn.is_connected(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(random_song))
            await ctx.send(f'Aleatório escolhido: {random_song.split("/")[2]}')
            return
        voice.stop()
        voice.play(discord.FFmpegPCMAudio(random_song))
        await ctx.send(f'Aleatório escolhido: {random_song.split("/")[2]}')
        return


@bot.command()
async def splay(ctx, song_to_play=None):
    if not song_to_play:
        await ctx.send(f'Escolhe um audio pra eu tocar, burro!\nSe não souber as opções, digite >audio')
        return
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    song_file = f'{random_audio_files}special_audio/{song_to_play}.mp3'
    if not os.path.exists(song_file):
        return await ctx.send(f'Esse audio não existe, burro!\nNão sabe os audios que existem né? digite >audio')
    audio = discord.FFmpegPCMAudio(song_file)
    if voice_channel is not None and not fn.is_connected(ctx):
        await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.play(audio)
        return
    voice.stop()
    voice.play(audio)
    return


@bot.command()
async def audio(ctx):
    spec_song_files = os.listdir(f'{random_audio_files}special_audio/')
    spec_final_song_files = []
    for song in spec_song_files:
        new_name = song.replace('.mp3', '')
        spec_final_song_files.append(new_name)
    return await ctx.send(f'As opções são: {", ".join(spec_final_song_files)}')


@bot.command()
async def mnt(ctx, name, time):
    channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel), type=discord.ChannelType.voice)
    members = channel.members
    time_value = int(time)
    for member in members:
        if member.name == name:
            for role in ctx.author.roles:
                if role.name == 'Patrão Chipart':
                    try:
                        await ctx.send(f'Minutinho aplicado em: {member.display_name}, logo tá de volta')
                        await member.edit(mute=True)
                        await asyncio.sleep(time_value)
                        await member.edit(mute=False)
                        return
                    except Exception as e:
                        return await ctx.send(f'Erro ao aplicar minutinho em: {member.display_name}: {e}')
            await ctx.send('Você não tem permissão para isso, agora toma dobrado!')
            if time_value < 30:
                time_value = 30
                await ctx.send(f'Tá achando oq maluco? Tá tentando me sacanear? Vai ficar {time_value * 2} segundos quietinho aí!')
            await ctx.author.edit(mute=True)
            await asyncio.sleep(int(time_value * 2))
            await ctx.author.edit(mute=False)
            return await ctx.send('Bom pra aprender.')
    await ctx.send('Deu pau aqui irmão, acho que o usuário não está aí')


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
