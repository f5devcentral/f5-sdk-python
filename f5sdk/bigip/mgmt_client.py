"""BIG-IP management client"""

import os
import socket
import warnings
from datetime import datetime, timedelta
from retry import retry
import paramiko

import f5sdk.constants as constants
from f5sdk.logger import Logger
from f5sdk.utils import http_utils
from f5sdk.exceptions import SSHCommandStdError, DeviceReadyError, InvalidAuthError, HTTPError
from f5sdk.decorators import check_auth, add_auth_header

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
        skip_ready_check : bool
            skips the device ready check if set to true

        Returns
        -------
        None
        """

        self.logger = Logger(__name__).get_logger()

        self.host = host.split(':')[0]  # disallow providing port here
        self.port = int(kwargs.pop('port', None) or self._discover_port())
        self._user = kwargs.pop('user', None)
        self._password = kwargs.pop('password', None)
        self._private_key_file = kwargs.pop('private_key_file', None)
        self._set_user_password = kwargs.pop('set_user_password', None)
        self.token = kwargs.pop('token', None)

        self.token_details = {}

        # check device is ready
        if not kwargs.pop('skip_ready_check', False):
            self._is_ready()

        # handle multiple authentication mechanisms
        if self._user and self._password:
            self._login_using_credentials()
        elif self._user and self._private_key_file:
            self._set_password_using_key()
            self._login_using_credentials()
        elif self.token:
            pass
        else:
            raise Exception('user|password, user|private_key_file or token required')

    def _test_socket(self, port):
        """Test TCP connection can be established

        Parameters
        ----------
        None

        Returns
        -------
        bool
            a boolean true/false
        """
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(1)

        check = False
        try:
            _socket.connect((self.host, port))
            check = True
        except (socket.timeout, OSError) as err:
            self.logger.debug('connection timeout: %s', err)
        finally:
            _socket.close()
        return check

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

        if self._test_socket(DFL_PORT):
            return DFL_PORT
        if self._test_socket(DFL_PORT_1NIC):
            return DFL_PORT_1NIC
        return DFL_PORT

    @retry(tries=constants.RETRIES['LONG'], delay=constants.RETRIES['DELAY_IN_SECS'])
    def _is_ready(self):
        """Checks that the device is ready

        Notes
        -----
        Retries up to 5 minutes

        Parameters
        ----------
        None

        Returns
        -------
        bool
            boolean true if device is ready
        """

        self.logger.debug('Performing ready check using port %s' % self.port)

        if self._test_socket(self.port):
            return True

        raise DeviceReadyError('Unable to complete device ready check')

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
        with warnings.catch_warnings(record=True) as _:
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

    @retry(tries=constants.RETRIES['DEFAULT'], delay=constants.RETRIES['DELAY_IN_SECS'])
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
            tmsh = 'tmsh'  # add tmsh to command

        # set password
        self._make_ssh_request(constants.BIGIP_CMDS['AUTH_MODIFY'] % (tmsh, self._user, password))
        self._password = password

    @retry(exceptions=HTTPError,
           tries=constants.RETRIES['DEFAULT'],
           delay=constants.RETRIES['DELAY_IN_SECS'])
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
        timeout = 3600  # set timeout to 1 hour

        uri = '/mgmt/shared/authn/login'
        body = {
            'username': self._user,
            'password': self._password,
            'loginProviderName': 'tmos'
        }

        # get token
        try:
            response = http_utils.make_request(
                self.host,
                uri,
                port=self.port,
                method='POST',
                body=body,
                basic_auth={'user': self._user, 'password': self._password}
            )
        except HTTPError as error:
            if constants.HTTP_STATUS_CODE['FAILED_AUTHENTICATION'] in str(error):
                _exception = InvalidAuthError(error)
                _exception.__cause__ = None
                raise _exception
            raise error

        token = response['token']['token']
        # now extend token lifetime
        token_uri = '/mgmt/shared/authz/tokens/%s' % token

        http_utils.make_request(
            self.host,
            token_uri,
            port=self.port,
            method='PATCH',
            body={'timeout': timeout},
            basic_auth={'user': self._user, 'password': self._password}
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

        self.logger.debug('Logging in using user + password')

        token = self._get_token()
        self.token = token['token']
        self.token_details = token

    @check_auth
    @add_auth_header
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
        advanced_return : bool
            return additional information, like HTTP status code to caller

        Returns
        -------
        dict
            a dictionary containing the JSON response
        """

        return http_utils.make_request(self.host, uri, port=self.port, **kwargs)

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

    def get_info(self):
        """Gets device info

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the device information

            ::

                {
                    'version': 'x.x.x.x'
                }

        """

        uri = '/mgmt/tm/sys/version'
        response = self.make_request(uri)

        version = response['entries'][
            'https://localhost/mgmt/tm/sys/version/0'
        ]['nestedStats']['entries']['Version']['description']
        return {'version': version}
