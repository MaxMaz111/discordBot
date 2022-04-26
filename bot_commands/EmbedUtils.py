from enum import Enum

import discord
from discord import Member
from discord.embeds import EmptyEmbed, Embed
from discord.ext.commands import Context

import bot_commands.CommandUtils as CommandUtils
from localization.RuLocalization import RuLocalization


class EmbedColor(Enum):
    SUCCESS = 0x78ccf0
    PROBLEM_OCCURRED = 0x778899
    ERROR = 0xff2e2e
    ALL_OK = 0x4d4d4d


class ActionType(Enum):
    ASKED = 'asked'
    EXECUTED = 'executed'


def create_command_embed(ctx: Context = None,
                         colour: EmbedColor = EmbedColor.SUCCESS,
                         description: str = EmptyEmbed,
                         title: str = EmptyEmbed,
                         author: Member = None,
                         action_type: ActionType = ActionType.ASKED,
                         ) -> Embed:
    if author is None:
        author = ctx.message.author

    embed = discord.Embed(colour=colour.value, description=description, title=title)

    action_verb = RuLocalization.action_type_to_verb(action_type)
    embed.set_footer(text=f'{action_verb} {CommandUtils.to_nickname(author)}', icon_url=author.avatar_url, )

    return embed


async def show_embed(ctx: Context,
                     embed: Embed = None,
                     **kwargs
                     ):
    if embed is None:
        embed = create_command_embed(
            ctx=ctx,
            **kwargs
        )

    await ctx.send(embed=embed)
