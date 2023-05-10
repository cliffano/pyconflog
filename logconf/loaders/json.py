from logconf import PARAMS
import json

def load(conf_file):
    """Get configuration values from JSON file.
    """
    conf = {}
    with open(conf_file, 'r') as stream:
        conf_json = json.load(stream)
        for param in PARAMS:
            if param in conf_json:
                conf[param] = conf_json[param]
    return conf
