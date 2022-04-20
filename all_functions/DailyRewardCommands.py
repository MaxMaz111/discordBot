import discord
from discord.ext import commands

from data.bot_data import BotData


class DailyRewardCommands(commands.Cog):
    def __init__(self, bot_data: BotData):
        self.bot_data = bot_data

    @commands.command()
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def reward(self, ctx):
        embed = discord.Embed(title="Вы успешно получили свою награду - 20 :coin:",
                              colour=0x778899)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        user_id = ctx.message.author.id
        guild_id = ctx.guild.id
        self.bot_data.db.add_money(self.bot_data.db.get_user(user_id, guild_id), 20)
        await ctx.send(embed=embed)

    @reward.error
    async def reward_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            embed = discord.Embed(title=f'Вы уже получали свою награду, приходите позже.', colour=0xff2e2e)
            await ctx.send(embed=embed)
