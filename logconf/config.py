"""A module for managing logging configurations.
"""
import logging
from loaders import environ_loader, ini_loader, json_loader, xml_loader, yaml_loader

LEVELS = {
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

DEFAULT_DATEFMT = '%d-%b-%y %H:%M:%S'
DEFAULT_FILENAME = 'logconf.log'
DEFAULT_FILEMODE = 'w'
DEFAULT_FORMAT = '%(asctime)s --> %(name)s - %(levelname)s - %(message)s'
DEFAULT_LEVEL = 'info'

class Config():
    """A class for managing logging configurations.
    """

    def __init__(self, conf_files=None):
        """Initialise config by loading and merging
        the configuration options from files and environment
        variables.
        """

        self.conf = {}

        # Load configurations from files
        for conf_file in conf_files:

            curr_conf = {}

            if conf_file.endswith('.ini'):
                curr_conf = ini_loader.load(conf_file)
            elif conf_file.endswith('.json'):
                curr_conf = json_loader.load(conf_file)
            elif conf_file.endswith('.xml'):
                curr_conf = xml_loader.load(conf_file)
            elif conf_file.endswith('.yaml'):
                curr_conf = yaml_loader.load(conf_file)

            self.conf = {**curr_conf, **self.conf}

        # Load configurations from environment variables
        self.conf = {**environ_loader.load(), **self.conf}

    def get_datefmt(self):
        """Get date format.
        If date format is not specified, default to '%d-%b-%y %H:%M:%S'.
        """
        return self.conf.get('datefmt', DEFAULT_DATEFMT)

    def get_filename(self):
        """Get log filename.
        If log filename is not specified, default to 'logconf.log'.
        """
        return self.conf.get('filename', DEFAULT_FILENAME)

    def get_filemode(self):
        """Get file mode.
        If file mode is not specified, default to 'w'.
        """
        return self.conf.get('filemode', DEFAULT_FILEMODE)

    def get_format(self):
        """Get log format.
        If log format is not specified, default to
        '%(asctime)s --> %(name)s - %(levelname)s - %(message)s'.
        """
        return self.conf.get('format', DEFAULT_FORMAT)

    def get_level(self):
        """Get log level.
        If log level is not specified, default to 'info'.
        """
        level = self.conf.get('level', DEFAULT_LEVEL)
        return LEVELS[level]
