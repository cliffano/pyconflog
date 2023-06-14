"""Stream handler module for conflog.
"""
import logging

def init(config):
    """Initialise stream handler.
    """
    _format = config.get_format()
    datefmt = config.get_datefmt()
    level = config.get_level()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(_format, datefmt))
    stream_handler.setLevel(level)
    return stream_handler
