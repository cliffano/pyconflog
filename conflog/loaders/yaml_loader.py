"""YAML configuration loader.
"""
import yaml
from . import PARAMS

def load(conf_file: str) -> dict:
    """Get configuration values from YAML file.
    """
    conf = {}
    with open(conf_file, 'r', encoding='utf-8') as stream:
        conf_yaml = yaml.safe_load(stream)
        if conf_yaml is not None:
            for param in PARAMS:
                if param in conf_yaml:
                    conf[param] = conf_yaml[param]
    return conf
