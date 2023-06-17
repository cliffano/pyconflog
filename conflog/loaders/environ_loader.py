"""Environment variables configuration loader.
"""
import os
from . import PARAMS

def load() -> dict:
    """Get configuration values from environment variables.
    Configuration values are prefixed with CONFLOG_.
    """
    conf = {}
    for param in PARAMS:
        env_var = 'CONFLOG_' + param.upper()
        if env_var in os.environ:
            conf[param] = os.environ[env_var]
    return conf
