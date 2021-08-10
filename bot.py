import discord
from discord.ext import commands
import discord.ext.commands
import os
import random
import json
import functions as fn
import asyncio
from loguru import logger as lg
from dotenv import load_dotenv
import datetime

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

ROOT_PATH = 'C:/Users/Pedro/Desktop/mega-bot'
audio_files = f'{ROOT_PATH}/audio/'
big_audio_files = 'E:/playlist_skype_full/'
random_audio_files = 'E:/Playlist Skype/'
random_accel_audio_files = 'E:/Playlist Skype2x/'
random_accel_big_audio_files = 'E:/playlist_skype_full2x/'
img_files = f'{ROOT_PATH}/img/'
text_files_path = f'{ROOT_PATH}/files'


@bot.event
async def on_ready():
    lg.success(f'Bot iniciado com sucesso...')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='o Gui falar merda'))


@bot.command()
async def rplay(ctx):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    random_song = fn.find_random_audio(big_audio_files)
    lg.info(f'Aleatório escolhido normal: {random_song.split("/")[2]}')
    if voice_channel is not None and not fn.is_connected(ctx):
        await voice_channel.connect()
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
    lg.info(f'Aleatório escolhido acelerado: {random_song.split("/")[2]}')
    if voice_channel is not None and not fn.is_connected(ctx):
        await voice_channel.connect()
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
async def mnt(ctx, name=None, time=None, id=277572928583761920):

    user_roles = [role.name for role in ctx.author.roles]
    if 'Patrão Chipart' not in user_roles:
        return await ctx.send('Não tem permissão, mamou!')

    if name is None:
        member = discord.utils.get(ctx.guild.members, id=id)
    else:
        member = discord.utils.get(ctx.guild.members, name=name)

    if member is None:
        return await ctx.send(f'Deu pau aqui irmão, usuário não encontrado')

    if time is None:
        if not os.path.exists(f'{text_files_path}/users/{member.id}.txt'):
            fn.write_to_file(f'{text_files_path}/users/{member.id}.txt', 'w', '60')
        time_value = fn.get_int_from_file(f'{text_files_path}/users/{member.id}.txt')
        fn.write_to_file(f'{text_files_path}/users/{member.id}.txt', 'w', str(time_value + 10))
    else:
        time_value = int(time)
    await ctx.send(f'Minutinho de {time_value} aplicado em **{member.display_name}**, logo tá de volta')
    lg.info(f'Minutinho de {time_value} aplicado em {member.display_name}')
    fn.write_to_file(f'{text_files_path}/mnt_log.txt', 'a', f'{datetime.date.today()};{time_value};{member.display_name}')
    await member.edit(mute=True)
    await asyncio.sleep(time_value)
    await member.edit(mute=False)
    return


@bot.command()
async def smnt_old(ctx, name, time):
    channel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel),
                                type=discord.ChannelType.voice)
    members = channel.members
    for member in members:
        if member.name == name:
            for role in ctx.author.roles:
                if role.name == 'Patrão Chipart':
                    try:
                        if os.path.exists(f'{text_files_path}/users/{member.name}.txt'):
                            fn.write_to_file(f'{text_files_path}/users/{member.name}.txt', 'w', str(time))
                            return await ctx.send(f'Tempo base para {member.display_name} setado para {time} segundos')
                        return await ctx.send(f'Arquivo do usuário {member.display_name} não encontrado. Acho que nunca tomou minutinho automatico.')
                    except:
                        return await ctx.send(f'Erro ao alterar tempo base para o usuário {member.display_name}')
            return await ctx.send(f'Você não tem permissão para isso, mamou!')


@bot.command()
async def smnt(ctx, name, time):
    user_roles = [role.name for role in ctx.author.roles]
    if "Patrão Chipart" not in user_roles:
        return await ctx.send('Você não tem permissão para isso, mamou!')

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
    with open(f'{ROOT_PATH}/files/rules.json') as e:
        rules = json.load(e)
    found_rule = random.choice(rules['rules'])
    await ctx.send(found_rule)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if str(message.author.id) != '277572928583761920':
        await bot.process_commands(message)
        return

    await bot.process_commands(message)
    lg.info(f'Enviando selo')
    file = f'{img_files}selo.png'
    await message.channel.send(file=discord.File(file))

load_dotenv(dotenv_path=f'{ROOT_PATH}/.env')
bot.run(os.getenv('bot_key'))
