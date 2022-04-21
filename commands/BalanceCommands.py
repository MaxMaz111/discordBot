import discord
from discord.ext import commands

from commands import DiscordUtils
from commands.MembersCommands import MemberCommands
from data.bot_data import BotData


class BalanceCommands(commands.Cog):
    def __init__(self, data: BotData, top_limit: int):
        self.bot_data = data
        self.top_limit = top_limit

    @staticmethod
    def get_recipient_id(ctx, recipient_id_argument):
        recipient_id = ctx.message.mentions[0].id if ctx.message.mentions else recipient_id_argument
        return int(recipient_id)

    @staticmethod
    def get_sender(ctx):
        return ctx.message.author

    @commands.command()
    async def give(self, ctx, recipient_id, amount: int):
        sender = BalanceCommands.get_sender(ctx)
        sender_id = int(sender.id)

        recipient_id = BalanceCommands.get_recipient_id(ctx=ctx, recipient_id_argument=recipient_id)

        def try_give() -> str:
            members = self.bot_data.get_members(ctx=ctx)
            member_ids = MemberCommands.to_ids(members)
            if recipient_id not in member_ids:
                return f'<@{recipient_id}> нет на сервере.\n\nНе удастся передать монетки'

            if recipient_id == sender_id:
                return f'Нельзя передать монетки самому себе'

            return f'Вы передали {amount} :coin: пользователю <@{recipient_id}>'

        description = try_give()
        await DiscordUtils.show_embed(
            ctx,
            colour=0x78ccf0,
            description=description,
            footer_text=sender.name,
            footer_icon_url=sender.avatar_url,
        )

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            print(error.args)
            embed = discord.Embed(colour=0xff2e2e, title='Не удалось передать монтеки',
                                  description='Укажите человека, его id или линк, а затем количество монеток,'
                                              f' которое вы хотите передать')
            await ctx.send(embed=embed)

    @commands.command()
    async def balance(self, ctx):
        money = self.bot_data.get_money(ctx)
        await ctx.send(f'На вашем балансе {money.balance} монет')

    @commands.command()
    async def top_balances(self, ctx):
        top_id_balances = self.bot_data.top_users_by_money(ctx=ctx, limit=self.top_limit)

        guild_members = self.bot_data.get_members(ctx=ctx)
        id_to_guild_member = dict()
        for member in guild_members:
            id_to_guild_member[member.id] = member

        ans = []
        for discord_id, balance in top_id_balances:
            member = id_to_guild_member[discord_id]
            nickname = MemberCommands.to_nickname(member)
            result_str = f'{nickname} - {balance}'
            ans.append(result_str)

        msg = 'Топ пользователей сервера по балансу:\n'
        msg += '\n'.join(ans)
        await ctx.send(msg)
