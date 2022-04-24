from typing import Tuple
from discord.ext import commands
from bot_commands.EmbedUtils import EmbedColor, ActionType
from discord.ext.commands import Context
from bot_commands import EmbedUtils
from data.bot_data import BotData


class MarketCommands(commands.Cog):
    def __init__(self,
                 bot_data: BotData):
        self.data = bot_data

    @commands.command()
    async def market(self,
                     ctx: Context):
        role_to_cost = self.data.get_market_role_to_cost(ctx=ctx)

        def role_to_str(index_role_cost):
            index, role_cost = index_role_cost
            role, cost = role_cost
            return f'{index + 1} - ``@{role}``: {cost} :coin:'

        roles_str = '\n'.join(
            map(role_to_str, enumerate(role_to_cost.items()))
        )

        await EmbedUtils.show_embed(
            ctx=ctx,
            title='Роли доступные для покупки',
            description=roles_str,
            colour=EmbedColor.ALL_OK,
            action_type=ActionType.ASKED
        )

    @commands.command()
    async def buy(self, ctx, n: int):
        self.roles_id = self.get_roles_id(ctx)
        author = ctx.message.author
        self.role_price = self.get_role_price(ctx=ctx)

        async def try_buy() -> Tuple[str, EmbedColor]:
            if n < 0 or n > len(self.roles_id):
                return f'Не удается купить роль, укажите ее номер верно', EmbedColor.ERROR

            money = self.data.get_money(ctx=ctx).balance

            if money < self.role_price:
                return f'Не удалось купить роль. На счете недостаточно средств', EmbedColor.ERROR

            if self.roles_id[n-1] in list(map(lambda x: x.id, author.roles)):
                return f'Не удалось купить роль. Вы уже приобрели', EmbedColor.ERROR
            self.data.update_money(delta=-self.role_price, user=author, ctx=ctx)
            role = ctx.guild.get_role(self.roles_id[n-1])
            await author.add_roles(role)

            return f'Вы приобрели роль ``@{role}``', EmbedColor.SUCCESS

        description, colour = await try_buy()
        await EmbedUtils.show_embed(
            ctx=ctx,
            colour=colour,
            description=description,
            action_type=ActionType.EXECUTED
        )

    @buy.error
    async def buy_error(self,
                        ctx: Context,
                        error: Exception
                        ):
        print(error.args)
        await EmbedUtils.show_embed(
            ctx=ctx,
            title='Не удалось купить роль',
            colour=EmbedColor.ERROR,
            description=f'Укажите числом номмер роли из маркета, которую хотите купить.',
            action_type=ActionType.ASKED
        )




