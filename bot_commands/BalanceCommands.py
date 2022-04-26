from discord.ext import commands
from discord.ext.commands import Context

import bot_commands.CommandUtils as CommandUtils
from bot_commands import EmbedUtils
from bot_commands.BotException import BotException
from bot_commands.EmbedUtils import EmbedColor, ActionType
from bot_commands.MembersCommands import MemberCommands
from data.bot_data import BotData
from utils import ErrorUtils


class BalanceCommands(commands.Cog):
    def __init__(self,
                 data: BotData,
                 top_limit: int,
                 ):
        self.bot_data = data
        self.top_limit = top_limit

    @commands.command()
    async def give(self,
                   ctx: Context,
                   recipient_id: str,
                   amount: int,
                   ):
        sender = CommandUtils.get_author(ctx)
        sender_id = int(sender.id)

        recipient_id = CommandUtils.get_target_id(ctx=ctx, mentioned_id_argument=recipient_id)

        members = self.bot_data.get_members(ctx=ctx)
        member_ids = MemberCommands.to_ids(members)

        if recipient_id not in member_ids:
            raise BotException(message=f'<@{recipient_id}> нет на сервере.\n\nНе удастся передать монетки')

        if recipient_id == sender_id:
            raise BotException(message=f'Нельзя передать монетки самому себе')

        sender_money = self.bot_data.get_money(ctx=ctx)
        if sender_money.balance < amount:
            raise BotException(message=f'У вас недостаточно средств')

        self.bot_data.send_money(
            ctx=ctx,
            sender_money=sender_money,
            recipient_id=recipient_id,
            amount=amount,
        )

        await EmbedUtils.show_embed(
            ctx=ctx,
            colour=EmbedColor.SUCCESS,
            description=f'Вы передали {amount} :coin: пользователю <@{recipient_id}>',
            action_type=ActionType.EXECUTED,
        )

    @give.error
    async def give_error(self,
                         ctx: Context,
                         error: Exception,
                         ):
        await ErrorUtils.process_error(
            ctx=ctx,
            error=error,
            title_prefix='Не удалось передать монетки',
            description='Укажите человека, его id или линк, а затем количество монеток,'
                        f' которое вы хотите передать',
        )

    @commands.command()
    async def balance(self,
                      ctx: Context,
                      discord_id: str = None,
                      ):
        discord_id = CommandUtils.get_target_id(ctx=ctx, mentioned_id_argument=discord_id)

        money = self.bot_data.get_money(discord_id=discord_id, ctx=ctx)
        money_amount = money.balance
        owner_str = f'вашем балансе' if discord_id == CommandUtils.get_author(ctx=ctx).id else f'балансе <@{discord_id}>'
        await EmbedUtils.show_embed(ctx=ctx,
                                    colour=EmbedColor.SUCCESS,
                                    description=f'На {owner_str} {money_amount} :coin:',
                                    action_type=ActionType.ASKED,
                                    )

    @commands.command()
    async def top(self,
                  ctx: Context,
                  ):
        top_id_balances = self.bot_data.top_users_by_money(ctx=ctx, limit=self.top_limit)

        guild_members = self.bot_data.get_members(ctx=ctx)
        id_to_guild_member = dict()
        for member in guild_members:
            id_to_guild_member[member.id] = member

        ans = []
        for discord_id, balance in top_id_balances:
            member = id_to_guild_member[discord_id]
            nickname = CommandUtils.to_nickname(member)
            result_str = f'{nickname} - {balance} :coin:'
            ans.append(result_str)

        await EmbedUtils.show_embed(ctx=ctx,
                                    colour=EmbedColor.ALL_OK,
                                    title='Топ пользователей сервера по балансу',
                                    description='\n'.join(ans),
                                    action_type=ActionType.ASKED,
                                    )


