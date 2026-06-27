"""YAML file configuration loader for conflog."""

import yaml
from . import PARAMS


def load(conf_file: str) -> dict:
    """Load configuration values from a YAML file.

    Returns only the top-level keys listed in :data:`PARAMS`. An empty YAML
    document returns an empty dict without error.

    :param conf_file: Path to the YAML configuration file.
    :type conf_file: str
    :returns: Dict of configuration parameters found in the file.
    :rtype: dict
    """
    conf = {}
    with open(conf_file, "r", encoding="utf-8") as stream:
        conf_yaml = yaml.safe_load(stream)
        if conf_yaml is not None:
            for param in PARAMS:
                if param in conf_yaml:
                    conf[param] = conf_yaml[param]
    return conf
