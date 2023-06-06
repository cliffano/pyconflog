"""This module provides the Logconf class,
which allows the management of Python logging
via configuration files.
"""
import logging
from .handlers.file_handler import init as init_file_handler
from .handlers.stream_handler import init as init_stream_handler
from .config import Config

class Logconf():
    """A class for managing Python logging logger and handlers.
    """

    def __init__(self, conf_files=None):
        """Initialise Python logging with configuration from conf_files.
        """

        config = Config(conf_files=conf_files)
        handlers = config.get_handlers()
        datefmt = config.get_datefmt()
        level = config.get_level()

        self.handlers = []
        if 'stream' in handlers:
            self.handlers.append(init_stream_handler(config))
        if 'file' in handlers:
            self.handlers.append(init_file_handler(config))

        logging.basicConfig(
            datefmt=datefmt,
            level=level
        )

    def get_logger(self, name):
        """Get the logger based on the given name
        and add the handlers to the logger.
        """
        logger = logging.getLogger(name)
        for handler in self.handlers:
            logger.addHandler(handler)
        return logger

    def close_logger_handlers(self, name):
        """Close logger handlers
        and clear the handlers from logger.
        """
        logger = logging.getLogger(name)
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()
