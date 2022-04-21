import discord
from discord.embeds import EmptyEmbed, Embed


async def show_embed(ctx,
                     colour: int = EmptyEmbed,
                     description: str = EmptyEmbed,
                     title: str = EmptyEmbed,
                     author=None,
                     ):
    if author is None:
        author = ctx.message.author

    embed = discord.Embed(colour=colour, description=description, title=title)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    await ctx.send(embed=embed)
