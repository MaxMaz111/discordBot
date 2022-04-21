from typing import Set

from discord.ext import commands
from data.bot_data import BotData


class MemberCommands(commands.Cog):
    def __init__(self, data: BotData):
        self.data = data

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    @staticmethod
    def to_nickname(member) -> str:
        return member.name + '#' + member.discriminator

    @staticmethod
    def to_ids(members) -> Set[int]:
        return set(map(lambda x: x.id, members))

    @commands.command()
    async def members(self, ctx):
        members = self.data.get_members(ctx=ctx)
        nicknames = map(MemberCommands.to_nickname, members)
        nickname_str = '\n'.join(nicknames)
        await ctx.send(nickname_str)

