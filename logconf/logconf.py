"""This module provides a function to get a logger
with the specified name and configuration from conf_files.
"""
import logging
from config import Config

PARAMS = [
    'datefmt',
    'filename',
    'format',
    'level'
]

def get_logger(name, conf_files=None):
    """Get a logger with the specified name
    and configuration from conf_files.
    """

    config = Config(conf_files=conf_files)
    logging.basicConfig(
        datefmt=config.get_datefmt(),
        filename=config.get_filename(),
        filemode=config.get_filemode(),
        format=config.get_format(),
        level=config.get_level()
    )
    logger = logging.getLogger(name)
    return logger
