import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from all_functions.DailyReward import DailyReward
from all_functions.TimeCommands import TimeCommands
from bot_data import BotData
from data import db_session
from funcs import RandomThings

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
guild_id = 481470012192980993

bot_data = BotData(bot=bot, guild_id=guild_id)
load_dotenv()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

db_session.global_init('db/accounts.db')
bot.add_cog(RandomThings(data=bot_data))
bot.add_cog(DailyReward())
bot.add_cog(TimeCommands())
bot.run(os.getenv('TOKEN'))
