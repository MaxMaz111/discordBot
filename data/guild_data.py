from typing import Optional, List, Dict, Tuple

from discord import Member, Guild, Role
from discord.ext.commands import Bot


class GuildData:
    def __init__(self,
                 bot: Bot,
                 guild_id: int,
                 market_role_id_to_cost: Optional[Dict[int, int]] = None,
                 ):
        self.bot = bot

        self.guild_id = guild_id
        self.guild = None

        self.market_role_id_to_cost = market_role_id_to_cost or dict()
        self.market_role_costs = None

    def get_guild(self) -> Guild:
        if self.guild is None:
            self.guild = self.bot.get_guild(self.guild_id)
        return self.guild

    def get_members(self) -> List[Member]:
        return list(filter(lambda x: not x.bot, self.get_guild().members))

    def get_member(self, discord_id: int) -> Optional[Member]:
        members = self.get_members()
        member = list(filter(lambda x: x.id == discord_id, members))
        return member[0] if len(member) > 0 else None

    def get_market_role_costs(self) -> List[Tuple[Role, int]]:
        if self.market_role_costs is None:
            self.market_role_costs = []
            for role_id, cost in self.market_role_id_to_cost.items():
                role = self.get_guild().get_role(role_id=role_id)
                self.market_role_costs.append((role, cost))

        return self.market_role_costs
