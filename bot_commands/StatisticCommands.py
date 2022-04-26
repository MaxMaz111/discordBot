from discord.ext import commands
from discord.ext.commands import Context

from data.bot_data import BotData


class StatisticCommands(commands.Cog):
    def __init__(self,
                 data: BotData,
                 ):
        self.data = data

    @commands.command()
    async def stats(self,
                    ctx: Context,
                    ):
        pass
