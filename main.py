import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot_commands.BalanceCommands import BalanceCommands
from bot_commands.DailyRewardCommands import DailyRewardCommands
from bot_commands.ImageCommands import ImageCommands
from bot_commands.MembersCommands import MemberCommands
from bot_commands.TimeCommands import TimeCommands
from bot_commands.MarketCommands import MarketCommands
from data.bot_data import BotData
from data.db_data import DbData
from data.guild_data import GuildData
from discord_components import DiscordComponents

from utils import LogUtils

LogUtils.init_logger('discord')
LogUtils.init_logger(LogUtils.BOT_LOGGER_NAME)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
guild_id = 481470012192980993

role_cost = 50
guilds = [
    GuildData(
        bot=bot,
        guild_id=guild_id,
        market_role_id_to_cost={
            967438691809235044: role_cost,
            967439014695157780: role_cost,
        }
    )
]

db_directory = 'db'
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

db_name = f'{db_directory}/accounts.db'
db = DbData(db_name=db_name)

bot_data = BotData(guilds=guilds, db=db)
print(bot_data)
load_dotenv()


@bot.event
async def on_ready():
    DiscordComponents(bot)
    LogUtils.get_bot_logger().info(msg='We have logged in as {0.user}'.format(bot))

daily_reward = 20
top_balances_limit = 10

bot.add_cog(DailyRewardCommands(bot_data=bot_data, daily_reward=daily_reward))
bot.add_cog(TimeCommands())
bot.add_cog(ImageCommands(data=bot_data))
bot.add_cog(MarketCommands(bot_data=bot_data))
bot.add_cog(BalanceCommands(data=bot_data, top_limit=top_balances_limit))
bot.add_cog(MemberCommands(data=bot_data))
bot.run(os.getenv('TOKEN'))
