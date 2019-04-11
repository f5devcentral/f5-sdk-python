"""Helper utility functions """

import requests

def download_to_file(url, file_name):
    """Downloads an artifact to a local file

    Notes
    -----
    Uses a stream to avoid loading into memory

    Parameters
    ----------
    url: str
        the URL where the artifact should be downloaded from
    file_name: str
        the local file name where the artifact should be downloaded

    Returns
    -------
    None
    """

    response = requests.get(url, stream=True)
    with open(file_name, 'wb+') as file_object:
        for chunk in response.iter_content(chunk_size=1024):
            # filter out keep-alive new lines
            if chunk:
                file_object.write(chunk)
