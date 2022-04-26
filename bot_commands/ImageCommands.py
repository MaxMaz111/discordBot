import random

import requests
from bs4 import BeautifulSoup as bs
from discord.ext import commands
from discord.ext.commands import Context

from data.bot_data import BotData
from data.models import StatisticType


class ImageCommands(commands.Cog):
    def __init__(self, data: BotData):
        self.bot_data = data

    @commands.command()
    async def image(self, ctx: Context, name):
        url_template = "https://imgur.com/search?q=" + name
        r = requests.get(url_template)
        soup = bs(r.text, "html.parser")
        cats = soup.find_all('div', class_='post')
        link = 'https://imgur.com' + cats[0].find('a')['href']
        await ctx.send(link)

    @commands.command()
    async def fox(self, ctx: Context):
        self.bot_data.update_user_statistic(
            statistic_type=StatisticType.SEEN_FOXES_AMOUNT,
            delta=1,
            ctx=ctx,
        )
        await ctx.send(f'https://randomfox.ca/images/{random.randint(1, 121)}.jpg')
