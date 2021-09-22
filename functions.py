import json

import discord
import os
import random
from loguru import logger as lg
import re
import youtube_dl

ROOT_PATH = os.curdir
audio_files = f'{ROOT_PATH}/audio/'
big_audio_files = 'E:/playlist_skype_full/'
random_audio_files = 'E:/Playlist Skype/'
random_accel_audio_files = 'E:/Playlist Skype2x/'
random_accel_big_audio_files = 'E:/playlist_skype_full2x/'


async def find_and_connect_to_vc(ctx):
    vc = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    if vc is not None and not is_connected(ctx):
        await vc.connect()
    return vc


def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


def find_random_audio(location):
    try:
        random_audio = random.choice(os.listdir(location))
        return f'{location}{random_audio}'
    except Exception as e:
        lg.error(f'Erro ao encontrar um arquivo de audio aleatório: {e}')


def write_to_file(file_path, mode, content):
    with open(file_path, mode) as e:
        e.write(content)


def get_int_from_file(file_path):
    with open(file_path, 'r') as e:
        return int(e.read())


def read_json_file(file_path):
    with open(file_path, 'r') as e:
        return json.load(e)


def remoji(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def fix_title(title):
    title_corrections = {
        '/': '_',
        '\\': '_',
        '|': '_'
    }

    for key, value in title_corrections.items():
        title = title.replace(key, value)
    return title


def check_song_list():
    lg.debug(f'Terminou de rodar')


def download_file(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{ROOT_PATH}/audiotests/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = fix_title(info_dict['title'])
        if os.path.exists(f'{ROOT_PATH}/audiotests/{title}.mp3'):
            lg.debug(f'Arquivo de áudio: {title}.mp3 já existe, não será baixado novamente')
            return title
        ydl.download([url])
    lg.success(f'{title} baixado e pronto...')
    return title
