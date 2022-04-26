from discord.ext import commands
from discord.ext.commands import Context

from bot_commands import EmbedUtils, CommandUtils
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
                    discord_id: str = None,
                    ):
        discord_id = CommandUtils.get_target_id(ctx=ctx, mentioned_id_argument=discord_id)

        statistic_values = self.data.get_all_user_statistics(
            ctx=ctx, discord_id=discord_id
        )

        statistics_readable = [
            (RuLocalization.statistic_type_to_readable(StatisticType(statistic_name)), value)
            for value, statistic_name in statistic_values
        ]

        ans = [f'{statistic_readable} - {value}' for statistic_readable, value in statistics_readable]
        description = '\n'.join(ans) if len(ans) > 0 else 'Ни одной статистики не собрано'

        await EmbedUtils.show_embed(ctx=ctx,
                                    colour=EmbedColor.ALL_OK,
                                    title='Статиститика пользователя',
                                    description=description,
                                    action_type=ActionType.ASKED,
                                    )
