"""Python module for BIG-IP

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        # get BIG-IP info (version, etc.)
        device.get_info()

    Example - Token Authentication::

        device = ManagementClient('192.0.2.10', token='my_token')

    Example - Key-Based Authentication::

        device = ManagementClient('192.0.2.10',
                                user='admin',
                                private_key_file='~/my_key',
                                set_user_password='admin')

"""

import os
import json
import socket
import warnings
from datetime import datetime, timedelta
from retry import retry
import paramiko
import requests
from requests.auth import HTTPBasicAuth

import f5cloudsdk.constants as constants
from f5cloudsdk.logger import Logger
from f5cloudsdk.exceptions import SSHCommandStdError
from .decorators import check_auth

DFL_PORT = 443
DFL_PORT_1NIC = 8443

SSH_EXCEPTIONS = (
    paramiko.ssh_exception.SSHException,
    paramiko.ssh_exception.AuthenticationException,
    paramiko.ssh_exception.BadHostKeyException
)

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
    make_ssh_request()
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
            the username for device authentication
        password : str
            the password for device authentication
        private_key_file : str
            the file containing the private key for device authentication
        set_user_password : str
            sets the user password to this value - used along with private_key_file
        token : str
            the token to assign to the token attribute

        Returns
        -------
        None
        """

        self.host = host.split(':')[0] # disallow providing port here
        self.port = kwargs.pop('port', None) or self._discover_port()
        self._user = kwargs.pop('user', None)
        self._password = kwargs.pop('password', None)
        self._private_key_file = kwargs.pop('private_key_file', None)
        self._set_user_password = kwargs.pop('set_user_password', None)
        self.token = kwargs.pop('token', None)

        self.token_details = {}

        self.logger = Logger(__name__).get_logger()

        if self._user and self._password:
            # run _login_using_credentials()
            self._login_using_credentials()
        elif self._user and self._private_key_file:
            # set password
            self._set_password_using_key()
            # ok, now run login_using_credentials()
            self._login_using_credentials()
        elif self.token:
            # token provided directly
            pass
        else:
            raise Exception('user|password, user|private_key_file or token required')

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
        """See public method for documentation: make_request """

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
            timeout=constants.HTTP_TIMEOUT['DFL'],
            verify=constants.HTTP_VERIFY
        )

        # boolean response, if requested
        if bool_response:
            return response.ok

        # helpful debug
        self.logger.debug('HTTP response: %s %s' % (response.status_code, response.reason))

        # raise exception on non-success status code
        response.raise_for_status()
        return response.json()

    def _make_ssh_request(self, command):
        """See public method for documentation: make_ssh_request """

        # note: command *might* contain sensitive information
        # logger should scrub those: i.e. secret foo -> secret ***
        self.logger.debug('Making SSH request: %s' % (command))

        # create client kwargs
        client_kwargs = {
            'username': self._user
        }
        if self._password:
            client_kwargs['password'] = self._password
        elif self._private_key_file:
            private_key_file = os.path.expanduser(self._private_key_file)
            client_kwargs['pkey'] = paramiko.RSAKey.from_private_key_file(private_key_file)
        else:
            raise Exception('password or private key file required')

        # workaround for deprecation warning described here, until fixed
        # https://github.com/paramiko/paramiko/issues/1369
        # workaround: temporarily catch warnings on client.connect
        with warnings.catch_warnings(record=True) as _w:
            # create client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
            try:
                client.connect(self.host, **client_kwargs)
            except SSH_EXCEPTIONS as _e:
                self.logger.error(_e)
                raise _e

        # collect result
        result = client.exec_command(command)

        # command output (tuple): stdin, stdout, stder
        stdout = result[1].read().decode('utf-8')
        stderr = result[2].read().decode('utf-8')
        client.close()

        if stderr:
            raise SSHCommandStdError('Error: %s' % stderr)

        return stdout.rstrip('\n\r')

    @retry(tries=constants.RETRIES['DFL'], delay=constants.RETRIES['DFL_DELAY'])
    def _set_password_using_key(self):
        """Sets password on device using user + private key

        Updates user's password using set_user_password

        Retries if unsuccessful, up to maximum allotment

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # get password to set
        password = self._set_user_password
        if not password:
            raise Exception('set_user_password required')

        # get user shell - tmsh or bash
        tmsh = ''
        # note: if the shell is in fact bash the first command will fail, so catch
        # the exception and try with 'tmsh' explicitly added to the command
        auth_list_cmd = constants.BIGIP_CMDS['AUTH_LIST']
        try:
            user_info = self._make_ssh_request(auth_list_cmd % (tmsh, self._user))
        except SSHCommandStdError:
            user_info = self._make_ssh_request(auth_list_cmd % ('tmsh', self._user))
        if 'shell bash' in user_info:
            tmsh = 'tmsh' # add tmsh to command

        # set password
        self._make_ssh_request(constants.BIGIP_CMDS['AUTH_MODIFY'] % (tmsh, self._user, password))
        self._password = password

    @retry(tries=constants.RETRIES['DFL'], delay=constants.RETRIES['DFL_DELAY'])
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
        """Logs in to device using user + password

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.logger.info('Logging in using user + password')
        token = self._get_token()
        self.token = token['token']
        self.token_details = token

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

    @check_auth
    def make_ssh_request(self, command):
        """Makes request to device (SSH)

        Parameters
        ----------
        command : str
            the command to execute on the device

        Returns
        -------
        str
            the command response
        """

        return self._make_ssh_request(command)
