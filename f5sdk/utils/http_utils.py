"""Python module containing helper http utility functions """

import json
import os
import warnings
import requests
import urllib3

from f5sdk import constants
from f5sdk.logger import Logger

from f5sdk.exceptions import HTTPError

logger = Logger(__name__).get_logger()  # pylint: disable=invalid-name


def download_to_file(url, file_name):
    """Downloads an artifact to a local file

    Notes
    -----
    Uses a stream to avoid loading into memory

    Parameters
    ----------
    url : str
        the URL where the artifact should be downloaded from
    file_name : str
        the local file name where the artifact should be downloaded

    Returns
    -------
    None
    """

    response = requests.request(
        'GET',
        url,
        stream=True
    )
    with open(file_name, 'wb+') as file_object:
        for chunk in response.iter_content(chunk_size=1024):
            # filter out keep-alive new lines
            if chunk:
                file_object.write(chunk)


# pylint: disable=too-many-locals
def make_request(host, uri, **kwargs):
    """Makes request to device (HTTP/S)

    Parameters
    ----------
    uri : str
        the URI where the request should be made
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    port : int
        the port to use
    method : str
        the HTTP method to use
    query_parameters : dict
        the HTTP query parameters to use
    headers : str
        the HTTP headers to use (may override defaults)
    body : str
        the HTTP body to use
    body_content_type : str
        the HTTP body content type to use
    bool_response : bool
        return boolean based on HTTP success/failure
    basic_auth : dict
        use basic auth: {'user': 'foo', 'password': 'bar'}
    advanced_return : bool
        return additional information, like HTTP status code to caller

    Returns
    -------
    dict
        a dictionary containing the JSON response
    """

    headers = {
        'User-Agent': constants.USER_AGENT
    }

    port = kwargs.pop('port', 443)
    method = kwargs.pop('method', 'GET').lower()
    headers.update(kwargs.pop('headers', {}))
    query_parameters = kwargs.pop('query_parameters', {})

    # check for body, normalize
    body = kwargs.pop('body', None)
    body_content_type = kwargs.pop('body_content_type', 'json')  # json (default), raw
    if body and body_content_type == 'json':
        headers.update({'Content-Type': 'application/json'})
        body = json.dumps(body)

    # check for auth options
    auth = None
    basic_auth = kwargs.pop('basic_auth', None)
    if basic_auth:
        auth = requests.auth.HTTPBasicAuth(basic_auth['user'], basic_auth['password'])

    # note: certain requests *may* contain large payloads, do *not* log body
    logger.debug('Making HTTP request: %s %s' % (method.upper(), uri))

    url = 'https://%s:%s%s' % (host, port, uri)

    # make request
    with warnings.catch_warnings(record=True) as caught_warnings:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        response = requests.request(method,
                                    url,
                                    headers=headers,
                                    params=query_parameters,
                                    data=body,
                                    auth=auth,
                                    timeout=constants.HTTP_TIMEOUT['DFL'],
                                    verify=constants.HTTP_VERIFY)
        if caught_warnings and \
                caught_warnings[0].category == urllib3.exceptions.InsecureRequestWarning:
            if constants.ENV_VARS.get('DISABLE_SSL_WARNINGS') not in os.environ.keys() or (
                    constants.ENV_VARS.get('DISABLE_SSL_WARNINGS') in os.environ.keys() and
                    os.environ[constants.ENV_VARS.get('DISABLE_SSL_WARNINGS')].lower() == 'false'):
                logger.warning('SSL Insecure request, '
                               'recommend adding a valid certificate to the device')
    # return boolean response, if requested
    if kwargs.pop('bool_response', False):
        return response.ok

    status_code = response.status_code
    status_reason = response.reason

    # determine response body using the following logic
    # 1) if the content-length header exists and is 0: set to empty dict
    # 2) response is valid JSON: decode JSON to native python object (dict, list)
    headers = response.headers
    if (status_code == 204) or \
            ('content-length' in headers.keys() and headers['content-length'] == '0'):
        response_body = None
    else:
        try:
            response_body = response.json()
        except ValueError:
            response_body = {"body": response.content}


    # helpful debug
    logger.debug('HTTP response: %s %s' % (status_code, status_reason))
    logger.trace('HTTP response body: %s' % response_body)

    # raise exception on 4xx and 5xx status code(s)
    if str(status_code)[:1] in ['4', '5']:
        raise HTTPError('Bad request for URL: %s code: %s reason: %s body: %s' % (
            url, status_code, status_reason, response_body
        ))

    # optionally return tuple containing status code, response, (future)
    if kwargs.pop('advanced_return', False):
        return (response_body, status_code)

    # finally, simply return response data
    return response_body


def parse_url(url):
    """Parse URL


    Parameters
    ----------
    url : str
        the URL that should be parsed

    Returns
    -------
    dict
        object containing the parsed URL contents

        ::

            {
                'protocol': 'https',
                'host': 'test.local',
                'path': '/foo/bar',
                'query': ''
            }

    """

    parsed_url = requests.utils.urlparse(url)

    return {
        'protocol': parsed_url.scheme,
        'host': parsed_url.netloc,
        'path': parsed_url.path,
        'query': parsed_url.query
    }
