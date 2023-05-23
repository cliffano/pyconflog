"""This module provides a function to get a logger
with the specified name and configuration from conf_files.
"""
import logging
from logconf.config import Config

def get_logger(name, conf_files=None):
    """Get a logger with the specified name
    and configuration from conf_files.
    """
    config = Config(conf_files=conf_files)

    datefmt = config.get_datefmt()
    filename = config.get_filename()
    filemode = config.get_filemode()
    _format = config.get_format()
    level = config.get_level()

    file_handler = logging.FileHandler(filename, mode=filemode)
    stream_handler = logging.StreamHandler()

    logging.basicConfig(
        datefmt=datefmt,
        format=_format,
        level=level,
        handlers=[stream_handler, file_handler]
    )

    return logging.getLogger(name)
