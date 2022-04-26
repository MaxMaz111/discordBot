from discord.ext import commands
from discord.ext.commands import Context

from data.bot_data import BotData
from data.models import StatisticType


class StatisticCommands(commands.Cog):
    def __init__(self,
                 data: BotData,
                 ):
        self.data = data

    @commands.before_invoke
    async def register_call(self,
                            ctx: Context,
                            ):
        self.data.update_user_statistic(
            ctx=ctx,
            statistic_type=StatisticType.BOT_COMMANDS_AMOUNT,
            delta=1,
        )

    @commands.command
    async def stats(self,
                    ctx: Context,
                    ):
        pass
