"""This module provides the Logconf class,
which allows the management of Python logging
via configuration files.
"""
import logging
from logconf.config import Config

class Logconf():
    """A class for managing Python logging logger and handlers.
    """

    def __init__(self, conf_files=None):
        """Initialise Python logging with configuration from conf_files.
        """

        config = Config(conf_files=conf_files)
        handlers = config.get_handlers()
        datefmt = config.get_datefmt()
        _format = config.get_format()
        level = config.get_level()

        self.handlers = []
        if 'stream' in handlers:
            self.handlers.append(self._init_stream_handler(config))
        if 'file' in handlers:
            self.handlers.append(self._init_file_handler(config))

        logging.basicConfig(
            datefmt=datefmt,
            level=level
        )

    def _init_stream_handler(self, config):
        """Initialise stream handler.
        """
        _format = config.get_format()
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(_format))
        return stream_handler

    def _init_file_handler(self, config):
        """Initialise file handler.
        """
        _format = config.get_format()
        filename = config.get_filename()
        filemode = config.get_filemode()
        file_handler = logging.FileHandler(filename, mode=filemode)
        file_handler.setFormatter(logging.Formatter(_format))
        return file_handler

    def get_logger(self, name):
        """Get the logger based on the given name
        and add the handlers to the logger.
        """
        logger = logging.getLogger(name)
        for handler in self.handlers:
            logger.addHandler(handler)
        return logger

    def close_handlers(self, name):
        """Close logger handlers
        and clear the handlers from logger.
        """
        logger = self.get_logger(name)
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()
