from typing import Optional

import discord
from discord import Member


class GuildData:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id

        self.guild = None
        self.members = None

    def get_guild(self) -> discord.Guild:
        if self.guild is None:
            self.guild = self.bot.get_guild(self.guild_id)
        return self.guild

    def get_members(self):
        if self.members is None:
            members = self.get_guild().members
            self.members = list(filter(lambda x: not x.bot, members))
        return self.members

    def get_member(self, discord_id: int) -> Optional[Member]:
        members = self.get_members()
        member = list(filter(lambda x: x.id == discord_id, members))
        return member[0] if len(member) > 0 else None


