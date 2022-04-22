from enum import Enum, auto

from discord.ext import commands
from data.bot_data import BotData


class StatisticType(Enum):
    BOT_COMMANDS_AMOUNT = auto()


class StatisticCommands(commands.Cog):
    def __init__(self, data: BotData):
        self.bot_data = data

    @commands.command
    async def stats(self):
        pass
