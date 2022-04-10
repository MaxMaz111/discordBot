import discord
from discord.ext import commands
import logging

from token import TOKEN


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True


class RandomThings(commands.Cog):
    def __init__(self, b):
        self.bot = b

    @staticmethod
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_connect(self):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')


bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_cog(RandomThings(bot))
bot.run(TOKEN)
