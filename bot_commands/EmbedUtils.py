from enum import Enum

import discord
from discord.embeds import EmptyEmbed
import bot_commands.CommandUtils as CommandUtils


class EmbedColor(Enum):
    SUCCESS = 0x78ccf0
    PROBLEM_OCCURRED = 0x778899
    ERROR = 0xff2e2e
    ALL_OK = 0x4d4d4d


async def show_embed(ctx,
                     colour: EmbedColor,
                     description: str = EmptyEmbed,
                     title: str = EmptyEmbed,
                     author=None,
                     ):
    if author is None:
        author = ctx.message.author

    embed = discord.Embed(colour=colour.value, description=description, title=title)
    embed.set_footer(text=f'Выполнил(а) {CommandUtils.to_nickname(author)}', icon_url=author.avatar_url, )
    await ctx.send(embed=embed)
