"""Environment variable configuration loader for conflog."""

import os
from . import PARAMS


def load() -> dict:
    """Load configuration values from environment variables.

    Each parameter in :data:`PARAMS` is looked up as ``CONFLOG_<PARAM>``
    (upper-cased). Only variables that are set are included in the result.

    :returns: Dict of configuration parameters found in the environment.
    :rtype: dict
    """
    conf = {}
    for param in PARAMS:
        env_var = "CONFLOG_" + param.upper()
        if env_var in os.environ:
            conf[param] = os.environ[env_var]
    return conf
