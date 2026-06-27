"""Python logging setup via configuration files and environment variables."""

from typing import Union
import logging
from .handlers.file_handler import init as init_file_handler
from .handlers.stream_handler import init as init_stream_handler
from .config import Config


class Conflog:
    """Configures Python logging from files, environment variables, and a config dict."""

    def __init__(
        self,
        conf_files: Union[None, str, list] = None,
        conf_dict: Union[None, dict] = None,
    ):
        """Initialise Python logging with configuration from files and an optional dict.

        Configuration is loaded in order: files first, then environment variables,
        then ``conf_dict`` (which takes highest precedence).

        :param conf_files: Path or list of paths to configuration files.
            Supported formats: ``.ini``, ``.json``, ``.xml``, ``.yaml``.
        :type conf_files: str or list[str] or None
        :param conf_dict: Optional dict of configuration values that override all other
            sources.
        :type conf_dict: dict or None
        """

        if isinstance(conf_files, str):
            conf_files = [conf_files]

        self.config = Config(conf_files=conf_files, conf_dict=conf_dict)
        handlers = self.config.get_handlers()
        datefmt = self.config.get_datefmt()
        level = self.config.get_level()
        self.extras = self.config.get_extras()

        self.handlers = []
        if "stream" in handlers:
            self.handlers.append(init_stream_handler(self.config))
        if "file" in handlers:
            self.handlers.append(init_file_handler(self.config))

        logging.basicConfig(datefmt=datefmt, level=level)

    def get_logger(self, name: str) -> logging.Logger:
        """Return a named logger with all configured handlers attached.

        :param name: Logger name, typically ``__name__`` of the calling module.
        :type name: str
        :returns: Configured :class:`logging.LoggerAdapter` wrapping the named logger.
        :rtype: logging.LoggerAdapter
        """
        logger = logging.getLogger(name)
        logger.propagate = False  # prevent duplicate logging from parent propagation
        for handler in self.handlers:
            logger.addHandler(handler)

        logger = logging.LoggerAdapter(logger, self.extras)
        logger.setLevel(self.config.get_level())

        return logger

    def close_logger_handlers(self, name: str) -> None:
        """Close and remove all handlers from the named logger.

        :param name: Logger name whose handlers should be closed.
        :type name: str
        """
        logger = logging.getLogger(name)
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()

    def get_config_properties(self) -> dict:
        """Return the merged configuration properties dictionary.

        :returns: All resolved configuration key-value pairs.
        :rtype: dict
        """
        return self.config.conf
