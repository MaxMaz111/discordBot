import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot_commands.BalanceCommands import BalanceCommands
from bot_commands.DailyRewardCommands import DailyRewardCommands
from bot_commands.MembersCommands import MemberCommands
from bot_commands.TimeCommands import TimeCommands
from data.bot_data import BotData
from data.db_data import DbData
from data.guild_data import GuildData
from utils import LogUtils

LogUtils.init_logger('discord')
LogUtils.init_logger(LogUtils.BOT_LOGGER_NAME)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
guild_id = 481470012192980993

guilds = [
    GuildData(bot=bot, guild_id=guild_id)
]

db_name = 'db/accounts.db'
db = DbData(db_name=db_name)

bot_data = BotData(guilds=guilds, db=db)
load_dotenv()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

daily_reward = 20
bot.add_cog(DailyRewardCommands(bot_data=bot_data, daily_reward=daily_reward))
bot.add_cog(TimeCommands())

top_limit = 10
bot.add_cog(BalanceCommands(data=bot_data, top_limit=top_limit))
bot.add_cog(MemberCommands(data=bot_data))
bot.run(os.getenv('TOKEN'))
