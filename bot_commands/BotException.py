from discord.ext.commands import CommandError


class BotException(CommandError):
    def __init__(self,
                 message: str = None,
                 *args,
                 ):
        super().__init__(message=message, *args)
