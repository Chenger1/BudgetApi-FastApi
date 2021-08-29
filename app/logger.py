import logging
import sys


def get_logger(name: str = __file__, file: str = 'app.log', encoding: str = 'utf-8') -> logging.Logger:
    logger = logging.Logger(name)

    fh = logging.FileHandler(file, encoding=encoding)
    logger.addHandler(fh)

    sh = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(sh)
    return logger


log = get_logger()
