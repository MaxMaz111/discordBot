import re
from datetime import datetime
from typing import Tuple, Optional

import pytz
from discord.ext import commands

from bot_commands import EmbedUtils
from bot_commands.EmbedUtils import EmbedColor


class TimeCommands(commands.Cog):
    @staticmethod
    def format_date(date):
        return date.strftime("%A, %d. %B %Y %I:%M%p")

    @staticmethod
    def find_timezone(zone_str):
        zone_str = zone_str.strip().lower().replace('_', ' ')

        def zone_filter(timezone):
            return zone_str in timezone.replace('_', ' ').lower().split('/')

        zones = list(filter(zone_filter, pytz.all_timezones))
        return pytz.timezone(zones[0]) if zones else None

    @staticmethod
    def fix_gmt(zone_str):
        pattern = "GMT[\\+\\-][0-9]+"
        if re.match(pattern, zone_str):
            signs = ["+", "-"]
            for i, sign in enumerate(signs):
                if sign in zone_str:
                    other_sign = signs[1 - i]
                    return zone_str.replace(sign, other_sign)

        return zone_str

    @commands.command()
    async def time(self, ctx, city_or_timezone_or_gmt=None):
        def try_calculate(zone_argument) -> Tuple[str, EmbedColor]:
            def get_date(zone_str) -> Optional[datetime]:
                if zone_str is None:
                    return datetime.now()

                if zone_str.isnumeric():
                    zone_str = f'GMT+{zone_str}'

                zone_str = TimeCommands.fix_gmt(zone_str)

                zone = TimeCommands.find_timezone(zone_str)
                if zone is None:
                    return None

                return datetime.now(zone)

            date = get_date(zone_argument)
            if date is None:
                return 'Такого места или часового пояса нет в наших списках. ' \
                       'Введите город или часовой пояс, например Moscow, GMT+1 или 1', \
                       EmbedColor.ERROR

            return TimeCommands.format_date(date), EmbedColor.SUCCESS

        title, color = try_calculate(zone_argument=city_or_timezone_or_gmt)
        await DiscordUtils.show_embed(
            ctx=ctx,
            title=title,
            colour=color,
        )
