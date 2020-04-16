"""Base client"""

# pylint: disable=too-few-public-methods

from retry import retry

from f5sdk.logger import Logger
from f5sdk import constants
from f5sdk.utils import misc_utils
from f5sdk.utils import http_utils

from f5sdk.exceptions import InputRequiredError


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
            'InputRequiredError': InputRequiredError
        }

    @retry(tries=constants.RETRIES['LONG'], delay=constants.RETRIES['DELAY_IN_SECS'])
    def _wait_for_task(self, task_url):
        """Wait for task to complete - async 'accepted' task

        Notes
        -----
        Certain operations use an async task pattern, where a 202 response on the initial
        POST is returned along with a self link to query.  The operation is complete when
        one of the following is true (depends on the REST API)
        - The self link returns 200 (as opposed to 202)
        - The response object contains the following: { 'status': 'FINISHED' }

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

        # check for async task pattern success/failure
        if status_code != constants.HTTP_STATUS_CODE['OK']:
            raise Exception('Successful status code not returned: %s' % status_code)
        if 'status' in response and response['status'].upper() not in ['FINISHED', 'COMPLETED']:
            raise Exception('Successful status message not returned: %s' % response['status'])

        return response

    def _make_request(self, **kwargs):
        """Make request (HTTP)

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        uri : str
            request URI
        method : str
            request method
        config : dict, list
            request body
        query_parameters : dict
            request query parameters

        Notes
        -----
        Codifies async task pattern handling
        """

        uri = kwargs.pop('uri', self._metadata['uri'])
        method = kwargs.pop('method', 'GET')
        config = kwargs.pop('config', None)
        query_parameters = kwargs.pop('query_parameters', {})

        response, status_code = self._client.make_request(
            uri,
            method=method,
            body=config,
            query_parameters=query_parameters,
            advanced_return=True
        )

        # Account for any async task pattern
        # Note: F5CS does not return an "accepted" status code
        # so we will directly check for "taskReference" property (for now)
        if status_code == constants.HTTP_STATUS_CODE['ACCEPTED']:
            return self._wait_for_task(response['selfLink'])
        if status_code == constants.HTTP_STATUS_CODE['OK'] and response.get('taskReference'):
            return self._wait_for_task(response['taskReference'])

        # default - simply return response
        return response

    @staticmethod
    def _get_resource_name(**kwargs):
        """Get resource name"""

        resource_name = kwargs.pop('name', None)

        if not resource_name:
            raise InputRequiredError('Resource name must be provided')

        return resource_name

    def _list(self, **kwargs):
        """List operation - private method"""

        return self._make_request(**kwargs)

    def _create(self, **kwargs):
        """Create operation - private method"""

        config = misc_utils.resolve_config(
            kwargs.pop('config', None),
            kwargs.pop('config_file', None)
        )

        return self._make_request(method='POST', config=config)

    def _show(self, **kwargs):
        """Show operation - private method"""

        resource_name = self._get_resource_name(**kwargs)

        return self._make_request(
            uri='%s/%s' % (self._metadata['uri'], resource_name)
        )

    def _update(self, **kwargs):
        """Update operation - private method"""

        resource_name = self._get_resource_name(**kwargs)
        config = misc_utils.resolve_config(
            kwargs.pop('config', None),
            kwargs.pop('config_file', None)
        )

        return self._make_request(
            uri='%s/%s' % (self._metadata['uri'], resource_name),
            method='PUT',
            config=config
        )

    def _delete(self, **kwargs):
        """Delete operation - private method"""

        resource_name = self._get_resource_name(**kwargs)
        config = misc_utils.resolve_config(
            kwargs.pop('config', None),
            kwargs.pop('config_file', None),
            required=False
        )

        return self._make_request(
            uri='%s/%s' % (self._metadata['uri'], resource_name),
            method='DELETE',
            config=config
        )
