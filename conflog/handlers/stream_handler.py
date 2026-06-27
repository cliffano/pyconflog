"""Stream handler factory for conflog."""

import logging
from ..config import Config


def init(config: Config) -> logging.StreamHandler:
    """Create and configure a :class:`logging.StreamHandler`.

    :param config: Resolved logging configuration to read handler settings from.
    :type config: Config
    :returns: Configured stream handler ready to be added to a logger.
    :rtype: logging.StreamHandler
    """
    _format = config.get_format()
    datefmt = config.get_datefmt()
    level = config.get_level()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(_format, datefmt))
    stream_handler.setLevel(level)
    return stream_handler
