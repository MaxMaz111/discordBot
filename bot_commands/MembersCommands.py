from typing import Set

import discord

from data.bot_data import BotData
from discord.ext import commands
import bot_commands.CommandUtils as CommandUtils
from bot_commands import DiscordUtils
from bot_commands.DiscordUtils import EmbedColor


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
    def to_ids(members) -> Set[int]:
        return set(map(lambda x: x.id, members))

    @commands.command()
    async def members(self, ctx):
        members = self.data.get_members(ctx=ctx)
        nicknames = map(CommandUtils.to_nickname, members)
        nickname_str = '\n'.join(nicknames)
        await ctx.send(nickname_str)

    @commands.command()
    async def profile(self, ctx, discord_id=None):
        date_format = "%d.%m.%y"
        if discord_id is None:
            sender = CommandUtils.get_author(ctx)
            discord_id = int(sender.id)
        else:
            discord_id = CommandUtils.get_mentioned_id(ctx=ctx, recipient_id_argument=discord_id)

        guild_id = self.data.get_guild_id(ctx=ctx)
        guild_obj = self.data.guild_id_to_data[guild_id]
        user = guild_obj.get_member(discord_id=discord_id)
        if not user:
            await DiscordUtils.show_embed(ctx=ctx,
                                          colour=EmbedColor.ERROR,
                                          title='Пользователя с таким ID или никнеймом нет на сервере'
                                          )
            return

        user_nick = CommandUtils.to_nickname(user)
        joined_at = user.joined_at.strftime(date_format)
        created_at = user.created_at.strftime(date_format)
        user_roles = filter(lambda x: x.name != '@everyone', user.roles)
        user_name_roles = list(map(lambda x: f'`{x.name}`', user_roles))
        user_img_url = user.avatar_url
        author_nick = CommandUtils.to_nickname(ctx.author)
        author_img_url = ctx.author.avatar_url

        embed = discord.Embed(title=f'Информация о {user_nick}')\
            .set_thumbnail(url=user_img_url)\
            .add_field(name='Полное имя', value=user_nick)\
            .add_field(name='ID пользователя', value=user.id, inline=True)\
            .add_field(name='Присоединился к серверу', value=joined_at, inline=True)\
            .add_field(name='Аккаунт создан', value=created_at)\
            .add_field(name=f'Роли({len(user_name_roles)})', value=",".join(user_name_roles), inline=True)\
            .set_footer(text=f'Запросил(а) {author_nick}', icon_url=author_img_url)

        await ctx.send(embed=embed)

