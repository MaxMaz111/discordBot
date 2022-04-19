import discord
from discord.ext import commands
from data.bot_data import BotData


class RandomThings(commands.Cog):
    def __init__(self, data: BotData):
        # db_session.global_init("db/blogs.db")
        self.data = data

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    def get_members(self, ctx):
        guild_id = ctx.guild.id
        return list(self.data.get_members(guild_id))

    @commands.command()
    async def members(self, ctx):
        members_str = '\n'.join(map(str, self.get_members(ctx)))
        await ctx.send(members_str)

    # @commands.command()
    # async def time(self, ctx):
    #     await ctx.send(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))


    #
    # @commands.command()
    # @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    # async def award(self, ctx):
    #     embed = discord.Embed(title="Вы успешно получили свою награду - 20 :coin:",
    #                           colour=0x778899)
    #     embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)
    #
    # @award.error
    # async def award_error(self, ctx, error):
    #     if isinstance(error, discord.ext.commands.CommandOnCooldown):
    #         await ctx.send('попробуй позже')

    # @commands.command()
    # async def give(self, ctx, id, n: int):
    #     members = self.get_members(ctx)
    #     if ctx.message.mentions:
    #         id = ctx.message.mentions[0].id
    #     id = int(id)
    #     if id in members:
    #         if id != ctx.message.author.id:
    #             embed = discord.Embed(colour=0x78ccf0, description=f'Вы передали {n} :coin: пользователю <@{id}>')
    #             embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    #             await ctx.send(embed=embed)
    #         else:
    #             embed = discord.Embed(colour=0x78ccf0, description=f'Нельзя передать монетки самому себе')
    #             embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    #             await ctx.send(embed=embed)
    #     else:
    #         embed = discord.Embed(colour=0x78ccf0,
    #                               description=f'<@{id}> нет на сервере.\n\nНе удастся передать монетки')
    #         embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    #         await ctx.send(embed=embed)
    #
    # @give.error
    # async def give_error(self, ctx, error):
    #     if isinstance(error, discord.ext.commands.CommandError):
    #         embed = discord.Embed(colour=0xff2e2e, title='Не удалось передать монтеки',
    #                               description='Укажите человека, его id или линк, а затем количество монеток,'
    #                                           ' которое вы хотите передать')
    #         await ctx.send(embed=embed)
