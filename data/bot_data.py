from typing import List

from data.db_data import DbData
from data.guild_data import GuildData
from data.models import Users, Money


class BotData:
    def __init__(self, guilds: List[GuildData], db: DbData):
        self.guild_id_to_data = {}
        for guild in guilds:
            self.guild_id_to_data[guild.guild_id] = guild
        self.db = db

    def get_members(self, guild_id: int = None, ctx=None):
        if guild_id is None:
            guild_id = ctx.guild.id
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


