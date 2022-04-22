import discord
from discord.ext.commands import Context

from bot_commands import EmbedUtils
from bot_commands.BotException import BotException
from bot_commands.EmbedUtils import EmbedColor, ActionType
from utils import LogUtils


async def process_error(ctx: Context,
                        error: Exception,
                        title: str,
                        description: str,
                        ):
    LogUtils.get_bot_logger().error(msg=str(error))

    if isinstance(error, discord.ext.commands.CommandError):
        error_details = error.args[0] if isinstance(error, BotException) else 'Ошибка при обработке запроса'
        await EmbedUtils.show_embed(
            ctx=ctx,
            colour=EmbedColor.ERROR,
            title=f'{title}: {error_details}',
            description=description,
            action_type=ActionType.ASKED,
        )
