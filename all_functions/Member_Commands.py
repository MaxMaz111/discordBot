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

    @commands.command()
    async def members(self, ctx):
        members_str = '\n'.join(map(str, self.data.get_members(ctx=ctx)))
        await ctx.send(members_str)

