from typing import List

from data.db_data import DbData
from data.guild_data import GuildData


class BotData:
    def __init__(self, guilds: List[GuildData], db: DbData):
        self.guild_id_to_data = {}
        for guild in guilds:
            self.guild_id_to_data[guild.guild_id] = guild

        self.db = db

    def get_members(self, guild_id=None, ctx=None):
        if guild_id is None:
            guild_id = ctx.guild.id
        return self.guild_id_to_data[guild_id].get_members()

    def get_members_nicknames(self, guild_id=None, ctx=None):
        if guild_id is None:
            guild_id = ctx.guild.id
        return self.guild_id_to_data[guild_id].get_members_nicknames()

