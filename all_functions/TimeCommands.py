import discord
from discord.ext import commands
from datetime import datetime
import pytz


class TimeCommands(commands.Cog):
    @commands.command()
    async def time(self, ctx, zone=None):
        if zone is None:
            embed = discord.Embed(title=datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
        elif not zone.isnumeric():
            zones = list(filter(lambda x: zone.strip().lower().replace('_', ' ') in
                                x.replace('_', ' ').lower().split('/'),
                                pytz.all_timezones))
            if zones:
                embed = discord.Embed(title=datetime.now(pytz.timezone(zones[0])).strftime("%A, %d. %B %Y %I:%M%p"))
            else:
                embed = discord.Embed(title='Такого места или часового пояса нет в наших списках.'
                                            ' Введите город или часовой пояс, напрмер GMT+1', colour=0xff2e2e)

        else:
            embed = discord.Embed(title='Неверный формат. Введите город или часовой пояс, напрмер GMT+1',
                                  colour=0xff2e2e)

        await ctx.send(embed=embed)
