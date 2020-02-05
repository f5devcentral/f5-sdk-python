"""Python module containing helper utility functions """

from f5sdk.constants import COMPARISON_OPERATORS
from f5sdk.exceptions import InputRequiredError
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


def compare_versions(version1, version2, operator):
    """Compare versions

    Parameters
    ----------
    version1 : str
        first version to compare
    config_file : str
        second version to compare
    operator : str
        operator such as greaterThanOrEqual, lessThanOrEqual

    Returns
    -------
    boolean
        boolean dependent on version comparison pass/fail
    """

    compare_pass = True
    for v_1, v_2 in zip(version1.split('.'), version2.split('.')):
        if not COMPARISON_OPERATORS[operator](int(v_1), int(v_2)):
            compare_pass = False

    return compare_pass
