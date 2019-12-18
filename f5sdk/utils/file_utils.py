"""Python module containing helper file utility functions """

import json


def load_file(file, **kwargs):
    """Load file (read + additional actions)

    Parameters
    ----------
    file : str
        location to configuration file
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    file_type : str
        the file type: json (default), raw

    Returns
    -------
    dict
        the loaded file
    """
    file_type = kwargs.pop('file_type', 'json')

    with open(file) as _f:
        data = _f.read()

    # do stuff based on explicit file type
    if file_type == 'json':
        data = json.loads(data)
    return data
