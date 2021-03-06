from discord.ext import commands
from discord.ext.commands import Context

from bot_commands import EmbedUtils
from bot_commands.EmbedUtils import EmbedColor, ActionType
from data.bot_data import BotData
from utils import ErrorUtils


class DailyRewardCommands(commands.Cog):
    def __init__(self,
                 bot_data: BotData,
                 daily_reward: int,
                 ):
        self.bot_data = bot_data
        self.daily_reward = daily_reward

    @commands.command()
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.member)
    async def reward(self,
                     ctx: Context,
                     ):
        self.bot_data.update_money(ctx=ctx, delta=self.daily_reward)

        await EmbedUtils.show_embed(
            ctx=ctx,
            title=f"Вы успешно получили свою награду - {self.daily_reward} :coin:",
            colour=EmbedColor.SUCCESS,
            action_type=ActionType.ASKED,
        )

    @reward.error
    async def reward_error(self,
                           ctx: Context,
                           error: Exception,
                           ):
        await ErrorUtils.process_error(
            ctx=ctx,
            error=error,
            title_prefix='Вы уже получали свою награду, приходите позже.',
        )
