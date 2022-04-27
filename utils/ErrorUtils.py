from typing import Optional

from discord.ext.commands import Context, CommandOnCooldown

from bot_commands import EmbedUtils
from bot_commands.BotException import BotException
from bot_commands.EmbedUtils import EmbedColor, ActionType
from utils import LogUtils


def get_error_details(error: Exception):
    if isinstance(error, BotException):
        return error.args[0]

    if isinstance(error, CommandOnCooldown):
        error_prefix = 'You are on cooldown. Try again in '
        error_message = error.args[0]
        total_seconds_str = error_message[len(error_prefix):-1]

        total_seconds = int(float(total_seconds_str))

        seconds_in_minute = 60

        minutes_in_hour = 60
        seconds_in_hour = minutes_in_hour * seconds_in_minute

        hours_in_day = 24
        seconds_in_days = hours_in_day * seconds_in_hour

        total_days = total_seconds // seconds_in_days
        total_seconds %= seconds_in_days

        total_hours = total_seconds // seconds_in_hour
        total_seconds %= seconds_in_hour

        total_minutes = total_seconds // seconds_in_minute
        total_seconds %= seconds_in_minute

        return f'До следующего запроса осталось {total_days} дней {total_hours} часов ' \
               f'{total_minutes} минут {total_seconds} секунд'

    return 'Ошибка при обработке запроса'


async def process_error(ctx: Context,
                        error: Exception,
                        title_prefix: str,
                        with_details: Optional[bool] = True,
                        description: Optional[str] = '',
                        ):
    LogUtils.get_bot_logger().error(msg=str(error))

    error_details = get_error_details(error)
    title = title_prefix + (f': {error_details}' if with_details else '')
    await EmbedUtils.show_embed(
        ctx=ctx,
        colour=EmbedColor.ERROR,
        title=title,
        description=description,
        action_type=ActionType.ASKED,
    )
