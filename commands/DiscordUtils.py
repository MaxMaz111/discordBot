import discord
from discord.embeds import EmptyEmbed, Embed


async def show_embed(ctx,
                     colour: int = EmptyEmbed, description: str = EmptyEmbed, title: str = EmptyEmbed,
                     footer_text: str = EmptyEmbed, footer_icon_url: str = EmptyEmbed):
    print(colour, description, title, footer_text, footer_icon_url)
    embed = discord.Embed(colour=colour, description=description, title=title)
    embed.set_footer(text=footer_text, icon_url=footer_icon_url)
    await ctx.send(embed=embed)
