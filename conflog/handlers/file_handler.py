"""File handler module for conflog.
"""
import logging

def init(config):
    """Initialise file handler with specified configuration.
    """
    _format = config.get_format()
    datefmt = config.get_datefmt()
    filename = config.get_filename()
    filemode = config.get_filemode()
    file_handler = logging.FileHandler(filename, mode=filemode)
    file_handler.setFormatter(logging.Formatter(_format, datefmt))
    return file_handler
