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
        user_id = ctx.message.author.id
        guild_id = ctx.guild.id
        money = self.bot_data.db.get_money(self.bot_data.db.get_user(user_id, guild_id))
        await ctx.send(f'На вашем балансе {money.balance} монет')

    @commands.command()
    async def top(self, ctx):
        ans = []
        for i in self.bot_data.get_members(ctx.guild.id, ctx):
            tmp = self.bot_data.db.get_money(self.bot_data.db.get_user(i.id, ctx.guild.id)).balance
            ans.append((f'{i.name}#{i.discriminator}', tmp))
        ans.sort(key=lambda x: (x[1], x[0]), reverse=True)
        ans = ans[:10]
        ans = [f'{x[0]} - {x[1]}' for x in ans]
        print(*ans)
        msg = 'Топ людей на сервере:\n'
        msg += '\n'.join(ans)
        await ctx.send(msg)
