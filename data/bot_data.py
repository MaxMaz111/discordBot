from typing import List, Tuple, Optional

from discord import Member

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

    @staticmethod
    def get_discord_id(discord_id: int = None, ctx=None) -> int:
        if discord_id is None:
            discord_id = ctx.message.author.id
        return discord_id

    def get_guild_data(self, guild_id: int = None, ctx=None) -> Optional[GuildData]:
        guild_id = BotData.get_guild_id(guild_id=guild_id, ctx=ctx)
        return self.guild_id_to_data[guild_id]

    def get_members(self, guild_id: int = None, ctx=None):
        return self.get_guild_data(guild_id=guild_id, ctx=ctx).get_members()

    def get_member(self, discord_id: int, guild_id: int = None, ctx=None) -> Optional[Member]:
        return self.get_guild_data(guild_id=guild_id, ctx=ctx).get_member(discord_id=discord_id)

    def get_user(self,
                 ctx=None,
                 discord_id: int = None,
                 guild_id: int = None) -> Users:
        discord_id = BotData.get_discord_id(discord_id=discord_id, ctx=ctx)
        guild_id = BotData.get_guild_id(guild_id=guild_id, ctx=ctx)
        return self.db.get_user(discord_id=discord_id, guild_id=guild_id)

    def get_money(self, ctx) -> Money:
        user = self.get_user(ctx=ctx)
        return self.db.get_money(user=user)

    def update_money(self,
                     delta: int,
                     user: Users = None,
                     ctx=None):
        if user is None:
            user = self.get_user(ctx=ctx)
        self.db.update_money(user=user, delta=delta)

    def top_users_by_money(self,
                           limit: int,
                           guild_id=None,
                           ctx=None,
                           member_ids: set = None) -> List[Tuple[int, int]]:
        guild_id = BotData.get_guild_id(guild_id=guild_id, ctx=ctx)
        if member_ids is None:
            members = self.get_members(guild_id=guild_id)
            member_ids = set(map(lambda x: x.id, members))

        return self.db.top_users_by_money(
            guild_id=guild_id,
            member_ids=member_ids,
            limit=limit
        )

    def send_money(self,
                   sender: Users,
                   recipient: Users,
                   amount: int,
                   sender_money: Money = None):
        self.db.send_money(
            sender=sender,
            recipient=recipient,
            amount=amount,
            sender_money=sender_money
        )
