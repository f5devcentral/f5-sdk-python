"""Management client"""

from retry import retry

import f5sdk.constants as constants
from f5sdk.logger import Logger
from f5sdk.utils import http_utils
from f5sdk.exceptions import InputRequiredError, InvalidAuthError, HTTPError

API_ENDPOINT = constants.F5_CS['API_ENDPOINT']
AUTH_TOKEN_HEADER = constants.F5_CS['AUTH_TOKEN_HEADER']


class ManagementClient(object):
    """A class used as a management client for F5 Cloud Services

    Attributes
    ----------
    access_token : str
        the access token for the service
    token_details : dict
        the token details for the service
    logger : object
        instantiated logger object

    Methods
    -------
    make_request()
        Refer to method documentation
    """

    def __init__(self, **kwargs):
        """Class initialization

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        user : str
            the username for service authentication
        password : str
            the password for service authentication

        Returns
        -------
        None
        """

        self.logger = Logger(__name__).get_logger()

        # process kwargs
        self._api_endpoint = kwargs.pop('api_endpoint', None)
        if self._api_endpoint is None:
            self._api_endpoint = API_ENDPOINT

        self._user = kwargs.pop('user', None)
        self._password = kwargs.pop('password', None)
        self._subscription_id = kwargs.pop('subscription_id', None)

        self.access_token = None
        self.token_details = None

        if self._user and self._password:
            self._login_using_credentials()
        else:
            raise InputRequiredError('user|password required')

    @retry(exceptions=HTTPError,
           tries=constants.RETRIES['DEFAULT'],
           delay=constants.RETRIES['DELAY_IN_SECS'])
    def _get_token(self):
        """Gets access token

        Retries if unsuccessful, up to maximum allotment

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing access token and expiration in seconds:
            {'accessToken': 'token', 'expirationIn': 3600}
        """


        try:
            response = http_utils.make_request(
                self._api_endpoint,
                '/v1/svc-auth/login',
                method='POST',
                body={
                    'username': self._user,
                    'password': self._password
                }
            )
        except HTTPError as error:
            if constants.HTTP_STATUS_CODE['BAD_REQUEST_BODY'] in str(error) or \
                constants.HTTP_STATUS_CODE['FAILED_AUTHENTICATION'] in str(error):
                _exception = InvalidAuthError(error)
                _exception.__cause__ = None
                raise _exception
            raise error
        return {
            'accessToken': response['access_token'],
            'expirationIn': response['expires_at']
        }

    def _login_using_credentials(self):
        """Logs in to service using user + password

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.logger.info('Logging in using user + password')
        self.token_details = self._get_token()
        self.access_token = self.token_details['accessToken']

    def make_request(self, uri, **kwargs):
        """Makes request to service (HTTP/S)

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

        # merge default authentication headers with any user supplied ones
        dfl_headers = {
            AUTH_TOKEN_HEADER: 'Bearer %s' % self.access_token
        }
        dfl_headers.update(kwargs.pop('headers', {}))

        return http_utils.make_request(
            self._api_endpoint,
            uri,
            headers=dfl_headers,
            **kwargs
        )
