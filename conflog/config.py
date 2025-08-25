"""A module for managing logging configurations.
"""

from typing import Union
import logging
from .loaders import environ_loader, ini_loader, json_loader, xml_loader, yaml_loader

LEVELS = {
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

DEFAULT_HANDLERS = "stream"
DEFAULT_DATEFMT = "%d-%b-%y %H:%M:%S"
DEFAULT_FILENAME = "conflog.log"
DEFAULT_FILEMODE = "w"
DEFAULT_FORMAT = "%(asctime)s --> %(name)s - %(levelname)s - %(message)s"
DEFAULT_LEVEL = "info"
DEFAULT_EXTRAS_SEPARATOR = ","
DEFAULT_EXTRAS_KEY_VALUE_SEPARATOR = "="
DEFAULT_EXTRAS = {}


class Config:
    """A class for managing logging configurations."""

    def __init__(
        self, conf_files: Union[None, list] = None, conf_dict: Union[None, list] = None
    ):
        """Initialise config by loading and merging
        the configuration options from files and environment
        variables, with optional configuration dictionary overwriting
        everything being specified.
        """

        self.conf = {}

        # Load configurations from files
        for conf_file in conf_files or []:

            curr_conf = {}

            if conf_file.endswith(".ini"):
                curr_conf = ini_loader.load(conf_file)
            elif conf_file.endswith(".json"):
                curr_conf = json_loader.load(conf_file)
            elif conf_file.endswith(".xml"):
                curr_conf = xml_loader.load(conf_file)
            elif conf_file.endswith(".yaml"):
                curr_conf = yaml_loader.load(conf_file)

            self.conf = {**self.conf, **curr_conf}

        # Load configurations from environment variables
        # Environment variables configuration overwrites all configuration
        # files supplied
        self.conf = {**self.conf, **environ_loader.load()}

        # Overwrite everything if configuration dictionary is supplied
        if conf_dict:
            self.conf = {**self.conf, **conf_dict}

    def get_handlers(self) -> str:
        """Get handlers.
        Handlers is a comma separated value of the handler
        types to be used.
        If handlers is not specified, default to 'stream'.
        Currently supported handlers are 'stream' and 'file'.
        """
        return self.conf.get("handlers", DEFAULT_HANDLERS).split(",")

    def get_datefmt(self) -> str:
        """Get date format.
        If date format is not specified, default to '%d-%b-%y %H:%M:%S'.
        """
        return self.conf.get("datefmt", DEFAULT_DATEFMT)

    def get_filename(self) -> str:
        """Get log filename.
        If log filename is not specified, default to 'conflog.log'.
        """
        return self.conf.get("filename", DEFAULT_FILENAME)

    def get_filemode(self) -> str:
        """Get file mode.
        If file mode is not specified, default to 'w'.
        """
        return self.conf.get("filemode", DEFAULT_FILEMODE)

    def get_format(self) -> str:
        """Get log format.
        If log format is not specified, default to
        '%(asctime)s --> %(name)s - %(levelname)s - %(message)s'.
        """
        return self.conf.get("format", DEFAULT_FORMAT)

    def get_level(self) -> int:
        """Get log level.
        If log level is not specified, default to 'info'.
        """
        level = self.conf.get("level", DEFAULT_LEVEL)
        return LEVELS[level.lower()]

    def get_extras_separator(self) -> str:
        """Get extras separator.
        If extras separator is not specified, default to ','.
        """
        return self.conf.get("extras_separator", DEFAULT_EXTRAS_SEPARATOR)

    def get_extras_key_value_separator(self) -> str:
        """Get extras key-value separator.
        If extras key-value separator is not specified, default to '='.
        """
        return self.conf.get(
            "extras_key_value_separator", DEFAULT_EXTRAS_KEY_VALUE_SEPARATOR
        )

    def get_extras(self) -> dict:
        """Get extras.
        Extras is a dictionary of extra message parameters
        to be added to the log.
        If extras is not specified, default to an empty dictionary.
        For JSON and YAML configuration formats, extras can be passed as a map or as a string.
        For other configuration formats, extras should be passed as a string.
        A string representation of extras should be in the format "key1=value1,key2=value2".
        """
        extras = self.conf.get("extras", DEFAULT_EXTRAS)
        extras_separator = self.get_extras_separator()
        extras_key_value_separator = self.get_extras_key_value_separator()
        if isinstance(extras, str):
            _extras = {}
            for pair in extras.split(extras_separator):
                key, value = pair.split(extras_key_value_separator)
                _extras[key] = value
            extras = _extras
        return extras
