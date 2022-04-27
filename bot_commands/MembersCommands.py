from typing import Set, List

from discord import Member
from discord.ext import commands
from discord.ext.commands import Context

import bot_commands.CommandUtils as CommandUtils
from bot_commands import EmbedUtils
from bot_commands.BotException import BotException
from bot_commands.EmbedUtils import EmbedColor, ActionType
from data.bot_data import BotData
from utils import ErrorUtils


class MemberCommands(commands.Cog):
    def __init__(self,
                 data: BotData,
                 ):
        self.data = data

    @commands.Cog.listener()
    async def on_member_join(self,
                             member: Member,
                             ):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    @staticmethod
    def to_ids(members: List[Member],
               ) -> Set[int]:
        return set(map(lambda x: x.id, members))

    @commands.command()
    async def members(self,
                      ctx: Context,
                      ):
        members = self.data.get_members(ctx=ctx)
        nicknames = map(CommandUtils.to_nickname, members)
        nickname_str = '\n'.join(nicknames)
        await ctx.send(nickname_str)

    @commands.command()
    async def members_amount(self,
                             ctx: Context,
                             ):
        guild_data = self.data.get_guild_data(ctx=ctx)
        guild_name = guild_data.get_guild().name
        members_amount = len(guild_data.get_members())

        await EmbedUtils.show_embed(ctx=ctx,
                                    colour=EmbedColor.ALL_OK,
                                    description=f'Количество пользователей на сервере {guild_name} - {members_amount}',
                                    action_type=ActionType.ASKED,
                                    )

    @commands.command()
    async def profile(self,
                      ctx: Context,
                      discord_id: str = None,
                      ):
        discord_id = CommandUtils.get_target_id(ctx=ctx, mentioned_id_argument=discord_id)

        user = self.data.get_member(discord_id=discord_id, ctx=ctx)
        if not user:
            raise BotException(f'Пользователь <@{discord_id}> не найден на сервере')

        date_format = "%d.%m.%y"
        user_nick = CommandUtils.to_nickname(user)
        joined_at = user.joined_at.strftime(date_format)
        created_at = user.created_at.strftime(date_format)
        user_roles = filter(lambda x: x.name != '@everyone', user.roles)
        user_role_names = list(map(lambda x: f'`{x.name}`', user_roles))
        user_role_names_list = ",".join(user_role_names) if user_role_names else 'Роли отсутствуют'
        user_img_url = user.avatar_url

        embed = EmbedUtils.create_command_embed(
            ctx=ctx,
            title=f'Информация о {user_nick}',
            action_type=ActionType.ASKED,
        )

        embed.set_thumbnail(url=user_img_url) \
            .add_field(name='Полное имя', value=user_nick) \
            .add_field(name='ID пользователя', value=user.id, inline=True) \
            .add_field(name='Присоединился к серверу', value=joined_at, inline=True) \
            .add_field(name='Аккаунт создан', value=created_at) \
            .add_field(name=f'Роли({len(user_role_names)})', value=user_role_names_list, inline=True) \

        await EmbedUtils.show_embed(ctx=ctx, embed=embed)

    @profile.error
    async def profile_error(self,
                            ctx: Context,
                            error: Exception
                            ):
        await ErrorUtils.process_error(
            ctx=ctx,
            error=error,
            title_prefix='Не удалось обработать запрос',
            description='При запросе профиля другого пользователя укажите его id или линк',
        )
