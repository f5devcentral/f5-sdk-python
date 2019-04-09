""" Denotes directory is a package """

import requests

def download_to_file(url, file_name):
    """ Download artifact to file (using a stream) """
    response = requests.get(url, stream=True)
    with open(file_name, 'wb+') as file_object:
        for chunk in response.iter_content(chunk_size=1024):
            # filter out keep-alive new lines
            if chunk:
                file_object.write(chunk)
