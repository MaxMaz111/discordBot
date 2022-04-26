from discord.ext import commands
from discord.ext.commands import Context

from bot_commands import EmbedUtils, CommandUtils
from bot_commands.BotException import BotException
from bot_commands.EmbedUtils import EmbedColor, ActionType
from data.bot_data import BotData
from utils import ErrorUtils


class MarketCommands(commands.Cog):
    def __init__(self,
                 bot_data: BotData):
        self.data = bot_data

    @commands.command()
    async def market(self,
                     ctx: Context):
        role_costs = self.data.get_market_role_costs(ctx=ctx)

        def role_to_str(index_role_cost):
            index, role_cost = index_role_cost
            role, cost = role_cost
            return f'{index + 1} - ``@{role}``: {cost} :coin:'

        roles_str = '\n'.join(
            map(role_to_str, enumerate(role_costs))
        )

        await EmbedUtils.show_embed(
            ctx=ctx,
            title='Роли доступные для покупки',
            description=roles_str,
            colour=EmbedColor.ALL_OK,
            action_type=ActionType.ASKED
        )

    @commands.command()
    async def buy(self,
                  ctx: Context,
                  role_index: int):
        role_index -= 1  # 0-indexation

        role_costs = self.data.get_market_role_costs(ctx=ctx)
        roles_count = len(role_costs)
        if roles_count == 0:
            raise BotException(message=f'Магазин пуст, попросите администратора добавить роли')

        if role_index not in range(roles_count):
            raise BotException(message=f'Ожидается номер роли от 1 до {roles_count}, но получен {role_index + 1}')

        role, cost = role_costs[role_index]

        author = CommandUtils.get_author(ctx=ctx)

        if role in author.roles:
            raise BotException(message=f'У вас уже есть роль {role.name}')

        balance = self.data.get_money(ctx=ctx).balance
        if balance < cost:
            raise BotException(message=f'На счете недостаточно средств')

        self.data.update_money(delta=-cost, ctx=ctx)
        await author.add_roles(role)

        await EmbedUtils.show_embed(
            ctx=ctx,
            description=f'Вы приобрели роль ``@{role}``',
            colour=EmbedColor.SUCCESS,
            action_type=ActionType.EXECUTED,
        )

    @buy.error
    async def buy_error(self,
                        ctx: Context,
                        error: Exception
                        ):
        await ErrorUtils.process_error(
            ctx=ctx,
            error=error,
            title_prefix='Не удалось купить роль',
            description=f'Укажите порядковый номер роли в списке из команды !market',
        )
