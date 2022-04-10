import discord
from discord.ext import commands
import logging

import datetime

from token import TOKEN


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix='!')
bot = commands.Bot(command_prefix='!', intents=intents)


class RandomThings(commands.Cog):
    def __init__(self, b):
        self.bot = b

    @staticmethod
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )



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
        embed = discord.Embed(colour=0x78ccf0, description=f'Вы передали {n} :coin: пользователю <@{id}>')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


bot.add_cog(RandomThings(bot))
bot.run(TOKEN)
