"""JSON configuration loader.
"""
import json
from . import PARAMS

def load(conf_file: str) -> dict:
    """Get configuration values from JSON file.
    """
    conf = {}
    with open(conf_file, 'r', encoding='utf-8') as stream:
        conf_json = json.load(stream)
        for param in PARAMS:
            if param in conf_json:
                conf[param] = conf_json[param]
    return conf
