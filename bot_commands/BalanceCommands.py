from typing import Tuple

import discord
from discord.ext import commands
from discord.ext.commands import Context

from bot_commands import EmbedUtils
from bot_commands.EmbedUtils import EmbedColor, ActionType
from bot_commands.MembersCommands import MemberCommands
from data.bot_data import BotData
import bot_commands.CommandUtils as CommandUtils
from utils import LogUtils


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

        recipient_id = CommandUtils.get_mentioned_id(ctx=ctx, mentioned_id_argument=recipient_id)

        def try_give() -> Tuple[str, EmbedColor]:
            members = self.bot_data.get_members(ctx=ctx)
            member_ids = MemberCommands.to_ids(members)
            if recipient_id not in member_ids:
                return f'<@{recipient_id}> нет на сервере.\n\nНе удастся передать монетки', EmbedColor.PROBLEM_OCCURRED

            if recipient_id == sender_id:
                return f'Нельзя передать монетки самому себе', EmbedColor.PROBLEM_OCCURRED

            sender_money = self.bot_data.get_money(ctx=ctx)
            if sender_money.balance < amount:
                return f'У вас недостаточно средств', EmbedColor.PROBLEM_OCCURRED

            self.bot_data.send_money(
                ctx=ctx,
                sender_money=sender_money,
                recipient_id=recipient_id,
                amount=amount,
            )

            return f'Вы передали {amount} :coin: пользователю <@{recipient_id}>', EmbedColor.SUCCESS

        description, colour = try_give()
        await EmbedUtils.show_embed(
            ctx=ctx,
            colour=colour,
            description=description,
            action_type=ActionType.EXECUTED,
        )

    @give.error
    async def give_error(self,
                         ctx: Context,
                         error: Exception,
                         ):
        LogUtils.get_bot_logger().error(msg=str(error))

        if isinstance(error, discord.ext.commands.CommandError):
            await EmbedUtils.show_embed(
                ctx=ctx,
                colour=EmbedColor.ERROR,
                title='Не удалось передать монетки',
                description='Укажите человека, его id или линк, а затем количество монеток,'
                            f' которое вы хотите передать',
                action_type=ActionType.ASKED,
            )

    @commands.command()
    async def balance(self,
                      ctx: Context,
                      ):
        money = self.bot_data.get_money(ctx=ctx)
        money_amount = money.balance
        await EmbedUtils.show_embed(ctx=ctx,
                                    colour=EmbedColor.SUCCESS,
                                    description=f'На вашем балансе {money_amount} :coin:',
                                    action_type=ActionType.ASKED,
                                    )

    @commands.command()
    async def top_balances(self,
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

        msg = 'Топ пользователей сервера по балансу:\n'
        msg += '\n'.join(ans)
        await EmbedUtils.show_embed(ctx=ctx,
                                    colour=EmbedColor.ALL_OK,
                                    title='Топ пользователей сервера по балансу',
                                    description='\n'.join(ans),
                                    action_type=ActionType.ASKED,
                                    )
