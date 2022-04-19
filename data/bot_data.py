from typing import List

from data.guild_data import GuildData


class BotData:
    def __init__(self, guilds: List[GuildData]):
        self.guild_id_to_data = {}
        for guild in guilds:
            self.guild_id_to_data[guild.guild_id] = guild

    def get_members(self, guild_id: int):
        return self.guild_id_to_data[guild_id].get_members()
