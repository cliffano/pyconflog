"""INI file configuration loader for conflog."""

import configparser
import io
from . import PARAMS


def load(conf_file: str) -> dict:
    """Load configuration values from an INI file.

    Reads the ``[conflog]`` section and returns only the keys listed in
    :data:`PARAMS`.

    :param conf_file: Path to the INI configuration file.
    :type conf_file: str
    :returns: Dict of configuration parameters found in the file.
    :rtype: dict
    """
    conf = {}
    with open(conf_file, "r", encoding="utf-8") as stream:
        conf_string = io.StringIO(stream.read())
        conf_ini = configparser.ConfigParser()
        conf_ini.read_file(conf_string)
        for param in PARAMS:
            if param in conf_ini["conflog"]:
                conf[param] = conf_ini["conflog"][param]
    return conf
