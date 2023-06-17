"""File handler module for conflog.
"""
import logging
from ..config import Config

def init(config: Config) -> logging.FileHandler:
    """Initialise file handler with specified configuration.
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
