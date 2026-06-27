"""File handler factory for conflog."""

import logging
from ..config import Config


def init(config: Config) -> logging.FileHandler:
    """Create and configure a :class:`logging.FileHandler`.

    :param config: Resolved logging configuration to read handler settings from.
    :type config: Config
    :returns: Configured file handler ready to be added to a logger.
    :rtype: logging.FileHandler
    """
    _format = config.get_format()
    datefmt = config.get_datefmt()
    level = config.get_level()
    filename = config.get_filename()
    filemode = config.get_filemode()
    file_handler = logging.FileHandler(filename, mode=filemode)
    file_handler.setFormatter(logging.Formatter(_format, datefmt))
    file_handler.setLevel(level)
    return file_handler
