import discord
from discord.ext import commands
import logging
from data import db_session
import datetime
import os
from t import TOKEN, guild_id
from funcs import RandomThings


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.add_cog(RandomThings(bot))
bot.run(TOKEN)