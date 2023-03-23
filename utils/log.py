import logging
from utils.log_formatter import CustomFormatter, SecondaryFormatter


def get_logger():
    logger = logging.getLogger("instagram-bot")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter("%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
                                    "%d-%m-%Y %H:%M:%S"))

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(ch)
    return logger


def change_log_formatter(logger):
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(SecondaryFormatter("%(asctime)s - %(levelname)s FROM INSTABOT - %(message)s (%(filename)s:%(lineno)d)",
                                       "%d-%m-%Y %H:%M:%S"))

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(ch)
    return logger
