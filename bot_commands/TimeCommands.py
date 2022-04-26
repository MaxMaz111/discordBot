import re
from datetime import datetime
from typing import Optional

import pytz
from discord.ext import commands
from discord.ext.commands import Context

from bot_commands import EmbedUtils
from bot_commands.BotException import BotException
from bot_commands.EmbedUtils import EmbedColor, ActionType
from utils import ErrorUtils


class TimeCommands(commands.Cog):
    @staticmethod
    def format_date(date: datetime):
        return date.strftime("%A, %d. %B %Y %I:%M%p")

    @staticmethod
    def find_timezone(zone_str: str):
        zone_str = zone_str.strip().lower().replace('_', ' ')

        def zone_filter(timezone: str):
            return zone_str in timezone.replace('_', ' ').lower().split('/')

        zones = list(filter(zone_filter, pytz.all_timezones))
        return pytz.timezone(zones[0]) if zones else None

    @staticmethod
    def fix_gmt(zone_str: str):
        pattern = "GMT[\\+\\-][0-9]+"
        if re.match(pattern, zone_str.upper()):
            signs = ["+", "-"]
            for i, sign in enumerate(signs):
                if sign in zone_str:
                    other_sign = signs[1 - i]
                    return zone_str.replace(sign, other_sign)

        return zone_str

    @commands.command()
    async def time(self,
                   ctx: Context,
                   city_or_timezone_or_gmt: str = None,
                   ):

        def calculate_date(zone_str: Optional[str]) -> datetime:
            if zone_str is None:
                return datetime.now()

            try:
                zone_int = int(zone_str)
                zone_sign = '-' if zone_int < 0 else '+'
                zone_str = f'GMT{zone_sign}{abs(zone_int)}'
            except ValueError:
                pass

            zone_str = TimeCommands.fix_gmt(zone_str)

            zone = TimeCommands.find_timezone(zone_str)
            if zone is None:
                raise BotException(message=f'Не найдено соответствие для {zone_str}')

            return datetime.now(zone)

        date = calculate_date(zone_str=city_or_timezone_or_gmt)
        date_str = TimeCommands.format_date(date)
        await EmbedUtils.show_embed(
            ctx=ctx,
            title=date_str,
            colour=EmbedColor.SUCCESS,
            action_type=ActionType.ASKED,
        )

    @time.error
    async def time_error(self,
                         ctx: Context,
                         error: Exception
                         ):
        await ErrorUtils.process_error(
            ctx=ctx,
            error=error,
            title_prefix='Ошибка вычисления времени',
            description='Введите город или часовой пояс (относительно GMT), например Moscow, GMT+3 или 3',
        )
