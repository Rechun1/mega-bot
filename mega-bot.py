import discord
import os
import random
import json

ROOT_PATH = os.curdir
img_files = f'{ROOT_PATH}/img/sardinha/'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('\guinf'):
        await message.channel.send(f' Olá {message.author.display_name}, o Guinf é macho')

    if message.content == 'rala':
        await message.channel.send(f'Desligando')
        await client.close()

    if message.content.startswith('\sardonha'):
        file = random.choice(os.listdir(img_files))
        await message.channel.send(file=discord.File(f'{img_files}/{file}'))

    if message.content.startswith('rr'):
        with open(f'{ROOT_PATH}/rules/rules.json') as e:
            rules = json.load(e)
        rule = random.choice(rules['rules'])
        await message.channel.send(rule)

@client.event
async def on_voice_state_update(member, before, after):
    channel = client.get_channel(277591138309767168)
    if member.display_name == 'Manda Chupa':
        await channel.send('@everyone manda chupa chegou')

client.run('ODY0MjY4MTcyMzY1NjYwMjAw.YOy-dQ.gM6ksIhcrWss2ai4uyjOaoRV12M')