import discord
from discord.ext import commands

# from data import db_session
import datetime

from t import guild_id


class RandomThings(commands.Cog):
    def __init__(self, b):
        self.bot = b
        self.guild = None
        # # # db_session.global_init("db/blogs.db")
        self.members = None

    def get_guild(self):
        if self.guild is None:
            self.guild = self.bot.get_guild(int(guild_id))
        return self.guild

    def get_members(self):
        if self.members is None:
            self.members = list(map(lambda x: x.id, filter(lambda x: not x.bot, self.get_guild().members)))
        return self.members

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    @commands.command()
    async def members(self, ctx):
        await ctx.send('\n'.join(map(str, self.get_members())))

    @commands.command()
    async def time(self, ctx):
        await ctx.send(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))

    @commands.command()
    async def balance(self, ctx):
        await ctx.send('на вашем балансе....')

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
            await ctx.send('попробуй позже')

    @commands.command()
    async def give(self, ctx, id, n):
        # если n не int то округлять вниз
        members = self.get_members()
        if id in members:
            if id.isnumeric():
                if int(id) != ctx.message.author.id:
                    embed = discord.Embed(colour=0x78ccf0, description=f'Вы передали {n} :coin: пользователю <@{id}>')
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    await ctx.send(f'{id}, {ctx.message.author.id}', embed=embed)
                else:
                    embed = discord.Embed(colour=0x78ccf0, description=f'Нельзя передать монетки самому себе')
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
            else:
                id = ctx.message.mentions[0].id
                if ctx.author.id != id:
                    embed = discord.Embed(colour=0x78ccf0, description=f'Вы передали {n} :coin: пользователю <@{id}>!')
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(colour=0x78ccf0, description=f'Нельзя передать монетки самому себе')
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
        else:
            await ctx.send('человек не на сервере')
