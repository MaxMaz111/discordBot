import random

from discord.ext import commands
from discord.ext.commands import Context

from data.bot_data import BotData


class ImageCommands(commands.Cog):
    def __init__(self, data: BotData):
        self.bot_data = data

    @commands.command()
    async def fox(self, ctx: Context):
        await ctx.send(f'https://randomfox.ca/images/{random.randint(1, 121)}.jpg')
