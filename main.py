import logging

import discord
from discord.ext import commands
from local_config import TOKEN

from bot_data import BotData
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


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.add_cog(RandomThings(data=bot_data))
bot.run(TOKEN)
