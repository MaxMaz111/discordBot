import random

import requests
from bs4 import BeautifulSoup as bs
from discord.ext import commands
from discord.ext.commands import Context

from bot_commands.BotException import BotException
from data.bot_data import BotData
from data.models import StatisticType
from utils import ErrorUtils


class ImageCommands(commands.Cog):
    def __init__(self, data: BotData):
        self.bot_data = data

    @commands.command()
    async def image(self,
                    ctx: Context,
                    name: str,
                    ):
        url_template = "https://imgur.com/search?q=" + name
        r = requests.get(url_template)
        soup = bs(r.text, "html.parser")
        images = soup.find_all('div', class_='post')

        if len(images) == 0:
            raise BotException(f'Ни одной картинки для \'{name}\' не найдено')

        selected_image = random.choice(images)
        link = 'https://imgur.com' + selected_image.find('a')['href']
        await ctx.send(link)

    @image.error
    async def image_error(self,
                          ctx: Context,
                          error: Exception,
                          ):
        await ErrorUtils.process_error(
            ctx=ctx,
            error=error,
            title_prefix='Ошибка при показе картинки',
        )

    @commands.command()
    async def fox(self,
                  ctx: Context
                  ):
        self.bot_data.update_user_statistic(
            statistic_type=StatisticType.SEEN_FOXES_AMOUNT,
            delta=1,
            ctx=ctx,
        )
        await ctx.send(f'https://randomfox.ca/images/{random.randint(1, 121)}.jpg')
