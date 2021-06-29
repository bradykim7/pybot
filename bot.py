# bot.py
import os
import random
import requests
import json

import discord
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    engineWow = [
        '엔진님 최고양!',
        '엔진킹! 갓엔진!',
    ]

    if message.content == '!엔진':
        response = random.choice(engineWow)
        await message.channel.send(response)

    if message.content.startswith("!raider"):
        searchData = message.content.split("/")
        region = searchData[1]
        realm = searchData[2]
        name = searchData[3]
        raiderURL = 'https://raider.io/api/v1/characters/profile?region='+region+'&realm='+realm+'&name='+name+'&fields=mythic_plus_best_runs'
        raiderResponseData = requests.get(raiderURL)
        raiderData = raiderResponseData.json()
        totalscore = 0
        for i in range(8):
            totalscore+=float(raiderData['mythic_plus_best_runs'][i]['score'])
            # pprint(raiderData['mythic_plus_best_runs'][i]['score'])
        
        await message.channel.send('\t'+raiderData['name']+'\'s Mythic+ Score :\t'+ str(round(totalscore)) + '\n' +'More Info\t:\t'+raiderData['profile_url'])

client.run(TOKEN)
