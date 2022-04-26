from typing import Optional

from discord import Member
from discord.ext.commands import Context


def get_target_id(ctx: Context,
                  mentioned_id_argument: Optional[str] = None
                  ) -> int:
    mentioned_id = ctx.message.mentions[0].id if ctx.message.mentions else mentioned_id_argument
    return int(mentioned_id) if mentioned_id else get_author(ctx=ctx).id


def get_author(ctx: Context
               ) -> Member:
    return ctx.message.author


def to_nickname(member: Member
                ) -> str:
    return member.name + '#' + member.discriminator
