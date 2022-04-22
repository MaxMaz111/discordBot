import logging


def init_discord_logger(fmt: str):
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt=fmt))
    logger.addHandler(handler)
