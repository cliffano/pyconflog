"""File handler module for logconf.
"""
import logging

def init(config):
    """Initialise file handler with specified configuration.
    """
    _format = config.get_format()
    filename = config.get_filename()
    filemode = config.get_filemode()
    file_handler = logging.FileHandler(filename, mode=filemode)
    file_handler.setFormatter(logging.Formatter(_format))
    return file_handler