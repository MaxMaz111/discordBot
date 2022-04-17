import discord
from discord.ext import commands
import logging
from data import db_session
import datetime
import os
from t import TOKEN
from funcs import RandomThings
from dataClass import DataClass

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
bot = DataClass.bot


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.add_cog(RandomThings())
bot.run(TOKEN)
