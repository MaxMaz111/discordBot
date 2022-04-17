from discord.ext import commands
import discord


class DataClass:
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    guild_id = 481470012192980993

    def __init__(self):
        self.guild = None
        self.members = None

    def get_guild(self):
        if self.guild is None:
            self.guild = self.bot.get_guild(self.guild_id)
        return self.guild

    def get_members(self):
        if self.members is None:
            self.members = list(map(lambda x: x.id, filter(lambda x: not x.bot, self.get_guild().members)))
        return self.members
