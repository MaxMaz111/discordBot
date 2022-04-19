import discord
from discord.ext import commands


class DailyReward(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def award(self, ctx):
        embed = discord.Embed(title="Вы успешно получили свою награду - 20 :coin:",
                              colour=0x778899)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @award.error
    async def award_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            embed = discord.Embed(title=f'Вы уже получали свою награду, приходите снова через', colour=0xff2e2e)
            await ctx.send(embed=embed)
