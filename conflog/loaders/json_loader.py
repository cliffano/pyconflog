"""JSON file configuration loader for conflog."""

import json
from . import PARAMS


def load(conf_file: str) -> dict:
    """Load configuration values from a JSON file.

    Returns only the top-level keys listed in :data:`PARAMS`.

    :param conf_file: Path to the JSON configuration file.
    :type conf_file: str
    :returns: Dict of configuration parameters found in the file.
    :rtype: dict
    """
    conf = {}
    with open(conf_file, "r", encoding="utf-8") as stream:
        conf_json = json.load(stream)
        for param in PARAMS:
            if param in conf_json:
                conf[param] = conf_json[param]
    return conf
