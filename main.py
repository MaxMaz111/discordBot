import discord
from discord.ext import commands
import logging
from data import db_session
import datetime

from t import TOKEN


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix='!')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


class RandomThings(commands.Cog):
    def __init__(self, b):
        self.bot = b
        # db_session.global_init("db/blogs.db")
        self.members = []

    @staticmethod
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    @client.command()
    async def members(self, ctx):
        for guild in bot.guilds:
            for member in guild.members:
                await ctx.send(member)

    @client.command()
    async def time(self, ctx):
        await ctx.send(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))

    @client.command()
    async def balance(self, ctx):
        await ctx.send('на вашем балансе....')

    @client.command()
    async def award(self, ctx):
        await ctx.send('+20 очков социального рейтинга')

    @client.command()
    async def give(self, ctx, id, n):
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


bot.add_cog(RandomThings(bot))
bot.run(TOKEN)
