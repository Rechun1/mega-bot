import discord
import os
import random
from loguru import logger as lg
import time

ROOT_PATH = os.curdir
audio_files = f'{ROOT_PATH}/audio/'
big_audio_files = 'E:/playlist_skype_full/'
random_audio_files = 'E:/Playlist Skype/'
random_accel_audio_files = 'E:/Playlist Skype2x/'
random_accel_big_audio_files = 'E:/playlist_skype_full2x/'


def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


def find_random_audio(location):
    try:
        random_audio = random.choice(os.listdir(location))
        return f'{location}{random_audio}'
    except Exception as e:
        lg.error(f'Erro ao encontrar um arquivo de audio aleatório: {e}')
