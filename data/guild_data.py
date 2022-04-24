from typing import Optional, List, Dict

from discord import Member, Guild, Role
from discord.ext.commands import Bot


class GuildData:
    def __init__(self,
                 bot: Bot,
                 guild_id: int,
                 market_role_id_to_cost: Dict[int, int]
                 ):
        self.bot = bot

        self.guild_id = guild_id
        self.guild = None

        self.members = None

        self.market_role_id_to_cost = market_role_id_to_cost
        self.market_role_to_cost = None

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

    def get_market_role_to_cost(self) -> Dict[Role, int]:
        if self.market_role_to_cost is None:
            self.market_role_to_cost = {}
            for role_id, cost in self.market_role_id_to_cost.items():
                role = self.get_guild().get_role(role_id=role_id)
                self.market_role_to_cost[role] = cost

        return self.market_role_to_cost
