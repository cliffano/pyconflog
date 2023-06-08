"""Stream handler module for conflog.
"""
import logging

def init(config):
    """Initialise stream handler.
    """
    _format = config.get_format()
    datefmt = config.get_datefmt()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(_format, datefmt))
    return stream_handler
