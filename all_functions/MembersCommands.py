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
        members = self.data.get_members(ctx=ctx)
        nicknames = map(lambda x: x.name + '#' + x.discriminator, members)
        nickname_str = '\n'.join(nicknames)
        await ctx.send(nickname_str)

