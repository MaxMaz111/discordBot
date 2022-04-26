from discord.ext import commands
from discord.ext.commands import Context

from bot_commands import EmbedUtils
from bot_commands.EmbedUtils import EmbedColor, ActionType, RuLocalization
from data.bot_data import BotData
from data.models import StatisticType


class StatisticCommands(commands.Cog):
    def __init__(self,
                 data: BotData,
                 ):
        self.data = data

    @commands.command()
    async def stats(self,
                    ctx: Context,
                    ):
        statistic_values = self.data.get_all_user_statistics(
            ctx=ctx
        )

        statistics_readable = [
            (RuLocalization.statistic_type_to_readable(StatisticType(statistic_name)), value)
            for value, statistic_name in statistic_values
        ]

        ans = [f'{statistic_readable} - {value}' for statistic_readable, value in statistics_readable]

        await EmbedUtils.show_embed(ctx=ctx,
                                    colour=EmbedColor.ALL_OK,
                                    title='Статиститика пользователя',
                                    description='\n'.join(ans),
                                    action_type=ActionType.ASKED,
                                    )
