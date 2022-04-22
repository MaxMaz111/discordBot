import logging

logger_format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'

BOT_LOGGER_NAME = 'bot-economic'


def init_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt=logger_format))
    logger.addHandler(handler)


def get_bot_logger():
    return logging.getLogger(BOT_LOGGER_NAME)