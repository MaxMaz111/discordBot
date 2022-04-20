import discord
from discord.ext import commands

from data.bot_data import BotData


class DailyRewardCommands(commands.Cog):
    def __init__(self, bot_data: BotData, daily_reward: int):
        self.bot_data = bot_data
        self.daily_reward = daily_reward

    @commands.command()
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def reward(self, ctx):
        self.bot_data.update_money(ctx=ctx, delta=20)

        embed = discord.Embed(title=f"Вы успешно получили свою награду - {self.daily_reward} :coin:",
                              colour=0x778899)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @reward.error
    async def reward_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            embed = discord.Embed(title=f'Вы уже получали свою награду, приходите позже.', colour=0xff2e2e)
            await ctx.send(embed=embed)
