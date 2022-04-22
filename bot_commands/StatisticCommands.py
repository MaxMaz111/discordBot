from discord.ext import commands

from data.bot_data import BotData


class StatisticCommands(commands.Cog):
    def __init__(self, data: BotData):
        self.bot_data = data

    @commands.command
    async def stats(self):
        pass
