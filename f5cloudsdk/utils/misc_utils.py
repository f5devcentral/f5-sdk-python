"""Python module containing helper utility functions """

from f5cloudsdk.exceptions import InputRequiredError
from . import file_utils

def resolve_config(config, config_file, **kwargs):
    """Resolve config options: config|config_file

    Parameters
    ----------
    config : str, dict
        configuration (resolved)
    config_file : str
        configuration file (to resolve)
    required : bool
        when false, input is not required and none object may be returned

    Returns
    -------
    dict
        the loaded config
    """

    if not config and not config_file:
        if kwargs.pop('required', True):
            raise InputRequiredError('One of config|config_file must be provided')
        return None

    if config_file:
        config = file_utils.load_file(config_file)
    return config
