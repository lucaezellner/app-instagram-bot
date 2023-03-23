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


def add_logging_level(level_name, level_num, method_name=None):
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError('{} already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError('{} already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError('{} already defined in logger class'.format(method_name))
    
    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)
            
    def log_to_root(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)
