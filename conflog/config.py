"""Logging configuration container and accessor."""

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
"""dict: Mapping of lower-case level name strings to :mod:`logging` level integers."""

DEFAULT_HANDLERS = "stream"
"""str: Default handler types, comma-separated."""

DEFAULT_DATEFMT = "%d-%b-%y %H:%M:%S"
"""str: Default date format string."""

DEFAULT_FILENAME = "conflog.log"
"""str: Default log file name."""

DEFAULT_FILEMODE = "w"
"""str: Default file open mode for the file handler."""

DEFAULT_FORMAT = "%(asctime)s --> %(name)s - %(levelname)s - %(message)s"
"""str: Default log record format string."""

DEFAULT_LEVEL = "info"
"""str: Default log level name."""

DEFAULT_EXTRAS_SEPARATOR = ","
"""str: Default separator between extra key-value pairs."""

DEFAULT_EXTRAS_KEY_VALUE_SEPARATOR = "="
"""str: Default separator between a key and its value within an extras pair."""

DEFAULT_EXTRAS = {}
"""dict: Default extras dictionary (empty)."""


class Config:
    """Resolved logging configuration built by merging files, environment variables, and a dict."""

    def __init__(
        self, conf_files: Union[None, list] = None, conf_dict: Union[None, dict] = None
    ):
        """Load and merge configuration from files, environment variables, and an optional dict.

        Sources are applied in order of increasing precedence:

        1. Configuration files (in the order supplied).
        2. Environment variables prefixed with ``CONFLOG_``.
        3. ``conf_dict`` (highest precedence, overwrites everything).

        :param conf_files: List of configuration file paths to load.
            Supported extensions: ``.ini``, ``.json``, ``.xml``, ``.yaml``.
        :type conf_files: list[str] or None
        :param conf_dict: Optional dict of configuration values that override all other
            sources.
        :type conf_dict: dict or None
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
        """Return the list of handler type names to use.

        Reads the ``handlers`` config key, which is a comma-separated string of
        handler type names. Supported values are ``stream`` and ``file``.

        :returns: List of handler type name strings.
            Defaults to ``['stream']`` when not configured.
        :rtype: list[str]
        """
        return self.conf.get("handlers", DEFAULT_HANDLERS).split(",")

    def get_datefmt(self) -> str:
        """Return the date format string for log records.

        :returns: strftime-compatible date format string.
            Defaults to ``'%d-%b-%y %H:%M:%S'`` when not configured.
        :rtype: str
        """
        return self.conf.get("datefmt", DEFAULT_DATEFMT)

    def get_filename(self) -> str:
        """Return the log file path for the file handler.

        :returns: Log file path string.
            Defaults to ``'conflog.log'`` when not configured.
        :rtype: str
        """
        return self.conf.get("filename", DEFAULT_FILENAME)

    def get_filemode(self) -> str:
        """Return the file open mode for the file handler.

        :returns: File open mode string (e.g. ``'w'``, ``'a'``).
            Defaults to ``'w'`` when not configured.
        :rtype: str
        """
        return self.conf.get("filemode", DEFAULT_FILEMODE)

    def get_format(self) -> str:
        """Return the log record format string.

        :returns: :func:`logging.Formatter`-compatible format string.
            Defaults to ``'%(asctime)s --> %(name)s - %(levelname)s - %(message)s'``
            when not configured.
        :rtype: str
        """
        return self.conf.get("format", DEFAULT_FORMAT)

    def get_level(self) -> int:
        """Return the numeric log level.

        :returns: :mod:`logging` level integer corresponding to the configured level name.
            Defaults to :data:`logging.INFO` when not configured.
        :rtype: int
        """
        level = self.conf.get("level", DEFAULT_LEVEL)
        return LEVELS[level.lower()]

    def get_extras_separator(self) -> str:
        """Return the separator used between extra key-value pairs in string form.

        :returns: Separator character or string.
            Defaults to ``','`` when not configured.
        :rtype: str
        """
        return self.conf.get("extras_separator", DEFAULT_EXTRAS_SEPARATOR)

    def get_extras_key_value_separator(self) -> str:
        """Return the separator used between a key and its value within an extras pair.

        :returns: Key-value separator character or string.
            Defaults to ``'='`` when not configured.
        :rtype: str
        """
        return self.conf.get(
            "extras_key_value_separator", DEFAULT_EXTRAS_KEY_VALUE_SEPARATOR
        )

    def get_extras(self) -> dict:
        """Return the extras dictionary to be injected into every log record.

        For JSON and YAML sources, extras may be supplied as a mapping directly.
        For all other sources (INI, XML, environment variables), extras must be a
        string of the form ``key1=value1,key2=value2`` (separators are configurable
        via :meth:`get_extras_separator` and :meth:`get_extras_key_value_separator`).

        :returns: Dict of extra fields added to each log record.
            Defaults to an empty dict when not configured.
        :rtype: dict
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
