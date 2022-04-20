import discord
from discord.ext import commands

from data.bot_data import BotData


class BalanceCommands(commands.Cog):
    def __init__(self, data: BotData):
        self.bot_data = data

    @commands.command()
    async def give(self, ctx, id, n: int):
        members = self.bot_data.get_members(ctx)
        if ctx.message.mentions:
            id = ctx.message.mentions[0].id
        id = int(id)
        if id in members:
            if id != ctx.message.author.id:
                embed = discord.Embed(colour=0x78ccf0, description=f'Вы передали {n} :coin: пользователю <@{id}>')
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=0x78ccf0, description=f'Нельзя передать монетки самому себе')
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0x78ccf0,
                                  description=f'<@{id}> нет на сервере.\n\nНе удастся передать монетки')
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            embed = discord.Embed(colour=0xff2e2e, title='Не удалось передать монтеки',
                                  description='Укажите человека, его id или линк, а затем количество монеток,'
                                              ' которое вы хотите передать')
            await ctx.send(embed=embed)

    @commands.command()
    async def balance(self, ctx):
        money = self.bot_data.get_money(ctx)
        await ctx.send(f'На вашем балансе {money.balance} монет')
