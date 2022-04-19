from typing import Dict

from data.guild_data import GuildData


class BotData:
    def __init__(self, guild_id_to_data: Dict[str, GuildData]):
        self.guild_id_to_data = guild_id_to_data

    def get_members(self, guild_id: str):
        return self.guild_id_to_data[guild_id].get_members()
