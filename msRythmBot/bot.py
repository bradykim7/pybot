from os import WIFCONTINUED
import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv

from music_cog import music_cog

bot = commands.Bot(command_prefix='!')

bot.add_cog(music_cog(bot))

load_dotenv()
bot.run(os.getenv("TOKEN"))
