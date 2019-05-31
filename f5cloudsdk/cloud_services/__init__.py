"""Python module for F5 Cloud Services

    Example - Basic::

        from f5cloudsdk.cloud_services import ManagementClient
        from f5cloudsdk.cloud_services.subscription import SubscriptionClient

        mgmt_client = ManagementClient(user='admin', password='admin')

        # configure subscription - DNS zones, records, etc.
        subscription_client = SubscriptionClient(mgmt_client, subscription_id='')
        subscription_client.update(config_file='./decl.json')

"""

from retry import retry

import f5cloudsdk.constants as constants
from f5cloudsdk.logger import Logger
from f5cloudsdk.utils import http_utils
from f5cloudsdk.exceptions import InputRequiredError

API_ENDPOINT = constants.F5_CLOUD_SERVICES['API_ENDPOINT']
AUTH_TOKEN_HEADER = constants.F5_CLOUD_SERVICES['AUTH_TOKEN_HEADER']

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

        self._api_endpoint = API_ENDPOINT

        # process kwargs
        self._user = kwargs.pop('user', None)
        self._password = kwargs.pop('password', None)
        self._subscription_id = kwargs.pop('subscription_id', None)

        self.access_token = None
        self.token_details = None

        if self._user and self._password:
            self._login_using_credentials()
        else:
            raise InputRequiredError('user|password required')

    @retry(tries=constants.RETRIES['DFL'], delay=constants.RETRIES['DFL_DELAY'])
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

        body = {
            'username': self._user,
            'password': self._password
        }

        response = http_utils.make_request(
            self._api_endpoint,
            '/v1/svc-auth/login',
            method='POST',
            body=body
        )
        return {'accessToken': response['access_token'], 'expirationIn': response['expires_at']}

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

        # need to add authentication token to headers
        headers = {AUTH_TOKEN_HEADER: 'Bearer %s' % self.access_token}
        headers.update(kwargs.pop('headers', {}))
        return http_utils.make_request(self._api_endpoint, uri, headers=headers, **kwargs)
