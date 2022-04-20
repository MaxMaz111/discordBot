from typing import List, Tuple

from data.db_data import DbData
from data.guild_data import GuildData
from data.models import Users, Money


class BotData:
    def __init__(self, guilds: List[GuildData], db: DbData):
        self.guild_id_to_data = {}
        for guild in guilds:
            self.guild_id_to_data[guild.guild_id] = guild
        self.db = db

    @staticmethod
    def get_guild_id(guild_id: int = None, ctx=None) -> int:
        if guild_id is None:
            guild_id = ctx.guild.id
        return guild_id

    def get_members(self, guild_id: int = None, ctx=None):
        guild_id = BotData.get_guild_id(guild_id=guild_id, ctx=ctx)
        return self.guild_id_to_data[guild_id].get_members()

    def get_user(self, ctx) -> Users:
        discord_id = ctx.message.author.id
        guild_id = ctx.guild.id
        return self.db.get_user(discord_id=discord_id, guild_id=guild_id)

    def get_money(self, ctx) -> Money:
        user = self.get_user(ctx=ctx)
        return self.db.get_money(user=user)

    def update_money(self, delta: int, user: Users = None, ctx=None):
        if user is None:
            user = self.get_user(ctx=ctx)

        self.db.update_money(user=user, delta=delta)

    def top_users_by_money(self, limit, guild_id=None, ctx=None, member_ids: set = None) -> List[Tuple[Users, Money]]:
        guild_id = BotData.get_guild_id(guild_id=guild_id, ctx=ctx)
        if member_ids is None:
            members = self.get_members(guild_id=guild_id)
            member_ids = set(map(lambda x: x.id, members))

        return self.db.top_users_by_money(guild_id=guild_id, member_ids=member_ids, limit=limit)