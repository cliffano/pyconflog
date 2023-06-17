"""INI configuration loader.
"""
import configparser
import io
from . import PARAMS

def load(conf_file: str) -> dict:
    """Get configuration values from JSON file.
    """
    conf = {}
    with open(conf_file, 'r', encoding='utf-8') as stream:
        conf_string = io.StringIO(stream.read())
        conf_ini = configparser.ConfigParser()
        conf_ini.read_file(conf_string)
        for param in PARAMS:
            if param in conf_ini['conflog']:
                conf[param] = conf_ini['conflog'][param]
    return conf
