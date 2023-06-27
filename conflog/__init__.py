"""
conflog
=======
Python logging setup via environment variables and configuration files.

This library provides a way to configure logging for Python applications.
It is intended to be used with configuration files in various formats,
including JSON, INI, XML, and YAML, along with the ability to overwrite
a configuration via environment variables.
"""

from typing import Union
import logging
from .handlers.file_handler import init as init_file_handler
from .handlers.stream_handler import init as init_stream_handler
from .config import Config

class Conflog():
    """A class for managing Python logging logger and handlers.
    """

    def __init__(self, conf_files: Union[None, str, list]=None, conf_dict: Union[None, dict]=None):
        """Initialise Python logging with configuration from
        configuration files and configuration dictionary.
        """

        if isinstance(conf_files, str):
            conf_files = [conf_files]

        self.config = Config(conf_files=conf_files, conf_dict=conf_dict)
        handlers = self.config.get_handlers()
        datefmt = self.config.get_datefmt()
        level = self.config.get_level()
        self.extras = self.config.get_extras()

        self.handlers = []
        if 'stream' in handlers:
            self.handlers.append(init_stream_handler(self.config))
        if 'file' in handlers:
            self.handlers.append(init_file_handler(self.config))

        logging.basicConfig(
            datefmt=datefmt,
            level=level
        )

    def get_logger(self, name: str) -> logging.Logger:
        """Get the logger based on the given name
        and add the handlers to the logger.
        """
        logger = logging.getLogger(name)
        logger.propagate = False # prevent duplicate logging from parent propagation
        for handler in self.handlers:
            logger.addHandler(handler)

        logger = logging.LoggerAdapter(logger, self.extras)
        logger.setLevel(self.config.get_level())

        return logger

    def close_logger_handlers(self, name: str) -> None:
        """Close logger handlers
        and clear the handlers from logger.
        """
        logger = logging.getLogger(name)
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()

    def get_config_properties(self) -> dict:
        """Get the configuration properties dictionary.
        """
        return self.config.conf
