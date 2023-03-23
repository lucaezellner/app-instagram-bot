import logging


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    magenta = '\x1b[35m'
    # assim que seta RGB
    white = '\x1b[38;2;255;255;255m'
    reset = '\x1b[0m'

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.white + self.fmt + self.reset,
            logging.INFO: self.white + self.fmt + self.reset,
            logging.WARNING: self.blue + self.fmt + self.reset,
            logging.ERROR: self.white + self.fmt + self.reset,
            logging.CRITICAL: self.magenta + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
