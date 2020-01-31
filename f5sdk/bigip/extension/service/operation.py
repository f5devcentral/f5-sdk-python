"""Module for BIG-IP extension component service configuration"""

import time
import requests
from retry import retry

from f5sdk import constants
from f5sdk.utils import misc_utils


class OperationClient(object):
    """A class used as a extension service operation client for BIG-IP

    Attributes
    ----------
    component : str
        the extension component
    version : str
        the extension component version

    Methods
    -------
    create()
        Refer to method documentation
    show()
        Refer to method documentation
    delete()
        Refer to method documentation
    is_available()
        Refer to method documentation
    """

    def __init__(self, client, component, version, metadata_client):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
        component : str
            the extension component
        version : str
            the extension component version
        metadata_client : object
            the extension metadata client

        Returns
        -------
        None
        """

        self._client = client
        self._metadata_client = metadata_client
        self.component = component
        self.version = version

    def _get_configure_endpoint(self):
        """Get configuration endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the configuration endpoint details
        """

        return self._metadata_client.get_endpoints()['configure']

    @retry(tries=constants.RETRIES['LONG'], delay=constants.RETRIES['DELAY_IN_SECS'])
    def _wait_for_task(self, task_url):
        """Wait for task to complete - async 'accepted' task

        Notes
        -----
        Certain extension components support async task behavior,
        where a 202 response on the initial POST is returned along
        with a self link to query.  The self link will return 202 until
        the task is complete, at which time it will return 200.

        Parameters
        ----------
        task_url : str
            HTTP url to task ID to query

        Returns
        -------
        dict
            the response to a service create (from task ID endpoint)
        """

        uri = requests.utils.urlparse(task_url).path
        response, status_code = self._client.make_request(uri, advanced_return=True)

        if status_code != constants.HTTP_STATUS_CODE['OK']:
            raise Exception('_wait_for_task timed out with status code: %s' % status_code)

        return response

    def is_available(self):
        """Checks extension component service is available

        Notes
        -----
        Retries up to 60 seconds

        Parameters
        ----------
        None

        Returns
        -------
        bool
            a boolean based on service availability
        """

        uri = self._get_configure_endpoint()['uri']

        ret = False
        i = 0
        while i < constants.RETRIES['DEFAULT']:
            if self._client.make_request(uri, bool_response=True):
                ret = True
                break
            i += 1
            time.sleep(constants.RETRIES['DELAY_IN_SECS'])

        return ret

    def create(self, **kwargs):
        """Creates (or updates) extension component service

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        config : dict
            a dictionary containing configuration
        config_file : str
            a local file containing configuration to load

        Returns
        -------
        dict
            the response to a service create
        """

        config = kwargs.pop('config', None)
        config_file = kwargs.pop('config_file', None)

        config = misc_utils.resolve_config(config, config_file)

        uri = self._get_configure_endpoint()['uri']
        response, status_code = self._client.make_request(
            uri, method='POST', body=config, advanced_return=True)

        # check for async task pattern response
        if status_code == constants.HTTP_STATUS_CODE['ACCEPTED']:
            return self._wait_for_task(response['selfLink'])
        # return response data
        return response

    def show(self):
        """Gets (shows) the extension component service

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the response to a service get
        """

        uri = self._get_configure_endpoint()['uri']
        return self._client.make_request(uri)

    def delete(self):
        """Deletes extension component service

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the response to a service deletion
        """

        methods = self._get_configure_endpoint()['methods']

        if 'DELETE' not in methods:
            raise Exception('Delete is not supported for this extension component')

        uri = self._get_configure_endpoint()['uri']
        return self._client.make_request(uri, method='DELETE')
