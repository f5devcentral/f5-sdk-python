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
    show_info()
        Refer to method documentation
    """

    def __init__(self, client, component, version, metadata_client, **kwargs):
        """Class initialization

        Parameters
        ----------
        client : instance
            the management client instance
        component : str
            the extension component
        version : str
            the extension component version
        metadata_client : instance
            the extension metadata client instance
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        logger : instance
            the logger instance to use

        Returns
        -------
        None
        """

        self.logger = kwargs.pop('logger', None)

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

    def _get_info_endpoint(self):
        """Get info endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the info endpoint details
        """

        return self._metadata_client.get_endpoints()['info']

    def _get_inspect_endpoint(self):
        """Get inspect endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the inspect endpoint details
        """

        return self._metadata_client.get_endpoints()['inspect']

    def _get_trigger_endpoint(self):
        """Get trigger endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the trigger endpoint details
        """

        return self._metadata_client.get_endpoints()['trigger']

    def _get_reset_endpoint(self):
        """Get reset endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the reset endpoint details
        """

        return self._metadata_client.get_endpoints()['reset']

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

    def reset(self, **kwargs):
        """Reset the state file states in CF extension component.

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Returns
        -------
        dict
            the API response to a service reset
        """

        declaration = kwargs.pop('content', None)

        config = kwargs.pop('config', None)
        config_file = kwargs.pop('config_file', None)

        # check if declaration is a json file. If so, parse it accordingly and get the content
        if declaration and declaration.split('.').pop() == 'json':
            declaration = misc_utils.resolve_config(None, declaration)

        # set default if no declaration is provided
        content = declaration if declaration is not None else {"resetStateFile": True}

        uri = self._get_reset_endpoint()['uri']
        response, status_code = self._client.make_request(
            uri, method='POST', body=content, advanced_return=True)

        # check for async task pattern response
        if status_code == constants.HTTP_STATUS_CODE['ACCEPTED']:
            return self._wait_for_task(response['selfLink'])
        # return response data
        return response

    def trigger(self, **kwargs):
        """Trigger a failover for CF component extension

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Returns
        -------
        dict
            the API response to a service trigger
        """

        declaration = kwargs.pop('content', None)

        # check if declaration is a json file. If so, parse it accordingly and get the content
        if declaration and declaration.split('.').pop() == 'json':
            declaration = misc_utils.resolve_config(None, declaration)

        # set default if no declaration is provided
        content = declaration if declaration is not None else '{}'

        uri = self._get_trigger_endpoint()['uri']
        response, status_code = self._client.make_request(
            uri, method='POST', body=content, advanced_return=True)

        # check for async task pattern response
        if status_code == constants.HTTP_STATUS_CODE['ACCEPTED']:
            return self._wait_for_task(response['selfLink'])
        # return response data
        return response

    def show_info(self):
        """Show component extension info

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the API response to a service info get
        """

        return self._client.make_request(self._get_info_endpoint()['uri'])

    def show_inspect(self):
        """Show component extension inspect

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the API response to a service inspect get
        """

        return self._client.make_request(self._get_inspect_endpoint()['uri'])

    def show_trigger(self):
        """Show CF component extension trigger failover status

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the API response to a service trigger get
        """

        return self._client.make_request(self._get_trigger_endpoint()['uri'])
