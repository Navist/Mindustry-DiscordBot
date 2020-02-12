import datetime
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.converter import MemberConverter
import asyncio
import json

#Written by Navist (Discord: Navist#8018)
# Version 1.0

botConfig = {}

with open('botConfig.json', 'r') as f:
    botConfig = json.load(f)

BOT_PREFIX = botConfig['prefix']
client = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

client.config = {}

with open('config.json', 'r') as f:
    client.config = json.load(f)

EXTENSIONS = ['moderation']

@client.event
async def on_ready():
    timeFormatted = datetime.datetime.now().strftime('@%H:%M:%S%p')
    print('-- ECN Bot Initializing --')
    print('-- %s --' % timeFormatted)
    for extension in EXTENSIONS:
        try:
            client.load_extension(extension)
            print('{} was loaded successfully.'.format(extension))
        except Exception as error:
            print('{} could not be loaded. {}'.format(extension, error))
    print('SUCCESS! Listening...')
    print('-----------------------------')


DiscordToken = client.config['discordToken']



client.run(DiscordToken)


