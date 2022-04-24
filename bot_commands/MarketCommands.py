from typing import Tuple
from discord.ext import commands
from bot_commands.EmbedUtils import EmbedColor, ActionType
from discord.ext.commands import Context
from bot_commands import EmbedUtils
from data.bot_data import BotData


class MarketCommands(commands.Cog):
    def __init__(self, bot_data: BotData):
        self.data = bot_data
        self.roles_id = None
        self.role_price = None

    def get_roles_id(self, ctx):
        if self.roles_id is None:
            self.roles_id = self.data.guild_id_to_data[ctx.guild.id].roles
        return self.roles_id

    def get_role_price(self, ctx):
        if self.role_price is None:
            self.role_price = self.data.guild_id_to_data[ctx.guild.id].role_price
        return self.role_price

    @commands.command()
    async def market(self, ctx):
        self.roles_id = self.get_roles_id(ctx)
        roles_to_str = ''
        for i in range(len(self.roles_id)):
            role = ctx.guild.get_role(role_id=self.roles_id[i])
            roles_to_str += f'{i+1} - ``@{role}``\n'

        embed_description = f'{roles_to_str}'
        embed = EmbedUtils.create_command_embed(ctx=ctx, colour=EmbedColor.ALL_OK, description=embed_description,
                                                title=' Роли доступные для покупки', action_type=ActionType.ASKED)
        await EmbedUtils.show_embed(ctx=ctx, embed=embed)

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




