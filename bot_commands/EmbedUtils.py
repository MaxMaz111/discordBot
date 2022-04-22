from enum import Enum

import discord
from discord import Member
from discord.embeds import EmptyEmbed, Embed
import bot_commands.CommandUtils as CommandUtils


class EmbedColor(Enum):
    SUCCESS = 0x78ccf0
    PROBLEM_OCCURRED = 0x778899
    ERROR = 0xff2e2e
    ALL_OK = 0x4d4d4d


def create_command_embed(ctx,
                         colour: EmbedColor,
                         description: str = EmptyEmbed,
                         title: str = EmptyEmbed,
                         author: Member = None,
                         ) -> Embed:
    if author is None:
        author = ctx.message.author

    embed = discord.Embed(colour=colour.value, description=description, title=title)
    embed.set_footer(text=f'Выполнил(а) {CommandUtils.to_nickname(author)}', icon_url=author.avatar_url, )

    return embed


async def show_embed(ctx,
                     embed: Embed = None,
                     **kwargs
                     ):
    if embed is None:
        embed = create_command_embed(
            ctx=ctx,
            **kwargs
        )

    await ctx.send(embed=embed)
