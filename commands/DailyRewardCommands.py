import discord
from discord.ext import commands

from commands import DiscordUtils
from data.bot_data import BotData


class DailyRewardCommands(commands.Cog):
    def __init__(self, bot_data: BotData, daily_reward: int):
        self.bot_data = bot_data
        self.daily_reward = daily_reward

    @commands.command()
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def reward(self, ctx):
        self.bot_data.update_money(ctx=ctx, delta=self.daily_reward)

        await DiscordUtils.show_embed(
            ctx=ctx,
            title=f"Вы успешно получили свою награду - {self.daily_reward} :coin:",
            colour=0x778899,
        )

    @reward.error
    async def reward_error(self, ctx, error):
        print(error.args)
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await DiscordUtils.show_embed(
                ctx=ctx,
                title=f'Вы уже получали свою награду, приходите позже.',
                colour=0xff2e2e,
            )
