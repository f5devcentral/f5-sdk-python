"""Base client"""

from retry import retry

from f5cloudsdk.logger import Logger
from f5cloudsdk import constants
from f5cloudsdk.utils import misc_utils
from f5cloudsdk.utils import http_utils

from f5cloudsdk.exceptions import MethodNotAllowed

class BaseFeatureClient(object):
    """A base feature client class

    Attributes
    ----------

    Methods
    -------
    """

    def __init__(self, client, **kwargs):
        """Class initialization

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        logger_name : str
            the logger name to use in log messages
        uri : str
            the REST URI against which this client operates

        Returns
        -------
        None
        """

        self.logger = Logger(kwargs.pop('logger_name', __name__)).get_logger()

        self._client = client
        self._metadata = {
            'uri': kwargs.pop('uri', None)
        }

        self._exceptions = {
            'MethodNotAllowed': MethodNotAllowed
        }

    @retry(tries=constants.RETRIES['LONG'], delay=constants.RETRIES['DELAY_IN_SECS'])
    def _wait_for_task(self, task_url):
        """Wait for task to complete - async 'accepted' task

        Notes
        -----
        Certain operations use an async task pattern, where a 202 response on the initial
        POST is returned along with a self link to query.  The self link will return 202
        until the task is complete, at which time it will return 200.

        Parameters
        ----------
        task_url : str
            the HTTP url with a task ID to query

        Returns
        -------
        dict
            the serialized REST response (once the task completes)
        """

        response, status_code = self._client.make_request(
            http_utils.parse_url(task_url)['path'],
            advanced_return=True
        )

        # check for async task pattern success/failure using multiple means
        # - success code (200)
        # - response object: { 'status': 'FINISHED' }
        if status_code != constants.HTTP_STATUS_CODE['OK']:
            raise Exception('Successful status code not returned: %s' % status_code)
        if 'status' in response and response['status'] not in ['FINISHED']:
            raise Exception('Successful status message not returned: %s' % response['status'])

        return response

    def _list(self):
        """List operation - private method"""

        return self._client.make_request(self._metadata['uri'])

    def _create(self, **kwargs):
        """Create operation - private method"""

        config = kwargs.pop('config', None)
        config_file = kwargs.pop('config_file', None)
        config = misc_utils.resolve_config(config, config_file)

        response, status_code = self._client.make_request(
            self._metadata['uri'],
            method='POST',
            body=config,
            advanced_return=True
        )

        # account for async task pattern
        if status_code == constants.HTTP_STATUS_CODE['ACCEPTED']:
            return self._wait_for_task(response['selfLink'])

        # default - simply return response
        return response

    def list(self):
        """List operation

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._list()

    def create(self, **kwargs):
        """Create operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._create(**kwargs)
