from logconf import PARAMS
import yaml

def load(conf_file):
    """Get configuration values from YAML file.
    """
    conf = {}
    with open(conf_file, 'r') as stream:
        conf_yaml = yaml.safe_load(stream)
        if conf_yaml is not None:
            for param in PARAMS:
                if param in conf_yaml:
                    conf[param] = conf_yaml[param]
    return conf
