"""Stream handler module for logconf.
"""
import logging

def init(config):
    """Initialise stream handler.
    """
    _format = config.get_format()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(_format))
    return stream_handler
