from typing import Optional, List

from discord import Member, Guild
from discord.ext.commands import Bot


class GuildData:
    def __init__(self, bot: Bot, guild_id: int, roles: List[int]):
        self.bot = bot
        self.guild_id = guild_id
        self.roles = roles
        self.role_price = 50

        self.guild = None
        self.members = None

    def get_guild(self) -> Guild:
        if self.guild is None:
            self.guild = self.bot.get_guild(self.guild_id)
        return self.guild

    def get_members(self) -> List[Member]:
        if self.members is None:
            members = self.get_guild().members
            self.members = list(filter(lambda x: not x.bot, members))
        return self.members

    def get_member(self, discord_id: int) -> Optional[Member]:
        members = self.get_members()
        member = list(filter(lambda x: x.id == discord_id, members))
        return member[0] if len(member) > 0 else None


