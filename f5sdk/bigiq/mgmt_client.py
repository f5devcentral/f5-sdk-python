"""BIG-IQ management client
"""

from datetime import datetime, timedelta

from retry import retry

from f5sdk.logger import Logger
from f5sdk import constants
from f5sdk.utils import http_utils
from f5sdk.decorators import check_auth, add_auth_header


class ManagementClient(object):
    """A class used as a management client for BIG-IQ

    Attributes
    ----------
    host : str
        the hostname of the device
    port : str
        the port of the device

    Methods
    -------
    get_info()
        Refer to method documentation
    make_request()
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

        Returns
        -------
        None
        """

        self.logger = Logger(__name__).get_logger()

        self.host = host.split(':')[0]
        self.port = kwargs.pop('port', 443)

        self._user = kwargs.pop('user', None)
        self._password = kwargs.pop('password', None)
        self._auth_provider = kwargs.pop('auth_provider', None)

        # account for multiple authentication schemes
        if self._user and self._password:
            self._login_using_credentials()
        else:
            raise Exception('user|password required')

    @retry(tries=constants.RETRIES['DEFAULT'], delay=constants.RETRIES['DELAY_IN_SECS'])
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
            {
                'token': 'token',
                'expirationDate': '2019-01-01T01:01:01.00'
            }
        """

        self.logger.debug('Getting authentication token')

        response = http_utils.make_request(
            self.host,
            '/mgmt/shared/authn/login',
            port=self.port,
            method='POST',
            body={
                'username': self._user,
                'password': self._password,
                'loginProviderName': self._auth_provider
            },
            basic_auth={
                'user': self._user,
                'password': self._password,
                'loginProviderName': self._auth_provider
            }
        )
        token_details = response['token']

        return {
            'token': token_details['token'],
            'expirationDate': (
                datetime.now() + timedelta(seconds=token_details['timeout'])
            ).isoformat()
        }

    def _login_using_credentials(self):
        """Login to device using user + password

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.logger.info('Logging in using user + password')

        self.token = self._get_token()['token']

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

        response = self.make_request('/mgmt/tm/sys/version')

        version_info = response['entries'][
            'https://localhost/mgmt/tm/sys/version/0'
        ]['nestedStats']['entries']
        return {
            'version': version_info['Version']['description']
        }
