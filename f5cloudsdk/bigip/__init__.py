"""Python module for BIG-IP

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        # get BIG-IP info (version, etc.)
        device.get_info()

    Example - Token Authentication::

        device = ManagementClient('192.0.2.10', token='my_token')
"""

import json
import socket
from datetime import datetime, timedelta
from retry import retry
import requests
from requests.auth import HTTPBasicAuth

import f5cloudsdk.constants as constants
from f5cloudsdk.logger import Logger
from .decorators import check_auth

DFL_PORT = 443
DFL_PORT_1NIC = 8443

class ManagementClient(object):
    """A class used as a management client for BIG-IP

    Attributes
    ----------
    host : str
        the hostname of the device
    port : str
        the port of the device
    token : str
        the token of the device
    token_details : dict
        the token details of the device
    logger : object
        instantiated logger object

    Methods
    -------
    get_info()
        Refer to method documentation
    make_request()
        Refer to method documentation
    make_request_ssh()
        Refer to method documentation
    """

    def __init__(self, host, **kwargs):
        """Class initialization

        Parameters
        ----------
        host : str
            the hostname of the device
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        port : int
            the port to assign to the port attribute
        user : str
            the username to assign to the user attribute
        password : str
            the password to assign to the password attribute
        private_key : str
            the private_key to assign to the private_key attribute
        token : str
            the token to assign to the token attribute

        Returns
        -------
        None
        """

        self.host = host.split(':')[0] # disallow providing port here
        self.port = kwargs.pop('port', None) or self._discover_port()
        self._user = kwargs.pop('user', '')
        self._password = kwargs.pop('password', '')
        self._private_key = kwargs.pop('private_key', '')
        self.token = kwargs.pop('token', None)
        self.token_details = {}

        self.logger = Logger(__name__).get_logger()

        if self._user and self._password:
            # run _login_using_credentials() to get token
            self._login_using_credentials()
        elif self._private_key:
            # create temporary user and run _login_using_credentials() to get token
            self._login_using_key()
        elif self.token:
            # token provided directly
            pass
        else:
            raise Exception('user/password credentials, private key or token required')

    def _discover_port(self):
        """Discover management port (best effort)

        Try 443 -> 8443, set port to 443 if neither responds.

        Timeout set to 1 second, if connect or connect refused assume it is the right port.

        Parameters
        ----------
        None

        Keyword Arguments
        -----------------
        None

        Returns
        -------
        int
            the discovered management port
        """
        # local helper function
        def _test_socket(port):
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.settimeout(1) # 1 second - avoid increasing this
            try:
                _socket.connect((self.host, port))
                return True
            except socket.timeout:
                return False
            except OSError:
                # this exception is used primarily to catch connection refused error
                # ConnectionRefusedError in python 3.x however to support 2.x use generic OSError
                return True

        if _test_socket(DFL_PORT):
            return DFL_PORT
        if _test_socket(DFL_PORT_1NIC):
            return DFL_PORT_1NIC
        return DFL_PORT

    def _make_request(self, uri, **kwargs):
        """Makes request to device (HTTP/S)

        Parameters
        ----------
        uri : str
            the URI where the request should be made
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        method : str
            the HTTP method to use
        headers : str
            the HTTP headers to use
        body : str
            the HTTP body to use
        body_content_type : str
            the HTTP body content type to use
        override_auth : object
            requests authentication object to use (instead of token)
        bool_response : bool
            return boolean based on HTTP success/failure

        Returns
        -------
        dict
            a dictionary containing the JSON response
        """

        uri = uri
        method = kwargs.pop('method', 'GET').lower()
        headers = {constants.F5_AUTH_TOKEN_HEADER: self.token, 'User-Agent': constants.USER_AGENT}
        # add any user-supplied headers, allow the user to override default headers
        headers.update(kwargs.pop('headers', {}))
        # check for body, normalize
        body = kwargs.pop('body', None)
        body_content_type = kwargs.pop('body_content_type', 'json') # json (default), raw
        if body and body_content_type == 'json':
            headers.update({'Content-Type': 'application/json'})
            body = json.dumps(body)

        auth = kwargs.pop('override_auth', None)
        if auth:
            headers.pop(constants.F5_AUTH_TOKEN_HEADER)

        bool_response = kwargs.pop('bool_response', False)

        # note: certain requests contain very large payloads, do *not* log body
        self.logger.debug('Making HTTP request: %s %s' % (method.upper(), uri))

        # construct url
        url = 'https://%s:%s%s' % (self.host, self.port, uri)
        # make request
        response = requests.request(
            method,
            url,
            headers=headers,
            data=body,
            auth=auth,
            timeout=60,
            verify=False
        )

        # boolean response, if requested
        if bool_response:
            return response.ok

        # raise exception on non-success status code
        response.raise_for_status()
        return response.json()

    @retry(tries=120, delay=1)
    def _get_token(self):
        """Gets authentication token

        Retries if unsuccessful, up to maximum allotment

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing authentication token, expiration date and expiration in seconds:
            {'token': 'token', 'expirationDate': '2019-01-01T01:01:01.00', 'expirationIn': 3600}
        """

        self.logger.debug('Getting authentication token')

        expiration_date = (datetime.now() + timedelta(hours=1)).isoformat()
        timeout = 3600 # set timeout to 1 hour

        uri = '/mgmt/shared/authn/login'
        body = {
            'username': self._user,
            'password': self._password,
            'loginProviderName': 'tmos' # need to support other providers
        }
        # get token
        response = self._make_request(
            uri,
            method='POST',
            body=body,
            override_auth=HTTPBasicAuth(self._user, self._password)
        )
        token = response['token']['token']

        # now extend token lifetime
        token_uri = '/mgmt/shared/authz/tokens/%s' % (token)
        self._make_request(
            token_uri,
            method='PATCH',
            body={'timeout': timeout},
            override_auth=HTTPBasicAuth(self._user, self._password)
        )

        return {'token': token, 'expirationDate': expiration_date, 'expirationIn': timeout}

    def _login_using_credentials(self):
        """Logs in to device using user/password

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.logger.info('Logging in using user/password')
        token = self._get_token()
        self.token = token['token']
        self.token_details = token

    def _login_using_key(self):
        """Logs in to device using private key

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.logger.info('Logging in using private key')

    def get_info(self):
        """Gets device info

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containg version: {'version': 'x.x.x'}
        """
        uri = '/mgmt/tm/sys/version'
        response = self.make_request(uri)

        v_0 = 'https://localhost/mgmt/tm/sys/version/0'
        version = response['entries'][v_0]['nestedStats']['entries']['Version']['description']
        return {'version': version}

    @check_auth
    def make_request(self, uri, **kwargs):
        """Makes request to device (HTTP/S)

        Parameters
        ----------
        uri : str
            the URI where the request should be made
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        method : str
            the HTTP method to use
        headers : str
            the HTTP headers to use
        body : str
            the HTTP body to use
        body_content_type : str
            the HTTP body content type to use
        bool_response : bool
            return boolean based on HTTP success/failure

        Returns
        -------
        dict
            a dictionary containing the JSON response
        """

        return self._make_request(uri, **kwargs)
