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
    is_available()
        Refer to method documentation
    show_info()
        Refer to method documentation
    create()
        Refer to method documentation
    show()
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

        response, status_code = self._client.make_request(
            requests.utils.urlparse(task_url).path,
            advanced_return=True
        )

        if status_code != constants.HTTP_STATUS_CODE['OK']:
            raise Exception('Wait for async task timed out with status code: %s' % status_code)

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

        response, status_code = self._client.make_request(
            self._get_configure_endpoint()['uri'],
            method='POST',
            body=misc_utils.resolve_config(config, config_file),
            advanced_return=True
        )

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

        return self._client.make_request(self._get_configure_endpoint()['uri'])

    def _delete(self):
        """Performs a delete against the component configuration endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the API response
        """

        return self._client.make_request(
            self._get_configure_endpoint()['uri'],
            method='DELETE'
        )

    def _show_inspect(self, **kwargs):
        """Performs a GET against the component inspect endpoint

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        query_parameters : dict
            optional query parameters to include

        Returns
        -------
        dict
            the API response
        """

        query_parameters = kwargs.pop('query_parameters', None)

        url = ''
        if query_parameters:
            for key in query_parameters:
                url += ''.join(key + '=' + str(query_parameters[key]) + '&')
            url = '?' + url[:-1]

        return self._client.make_request(self._get_inspect_endpoint()['uri'] + url)

    def _show_trigger(self):
        """Performs a GET against the component trigger endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the API response
        """

        return self._client.make_request(self._get_trigger_endpoint()['uri'])

    def _trigger(self, **kwargs):
        """Performs a POST against the component trigger endpoint

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
            the API response
        """

        config = kwargs.pop('config', None)
        config_file = kwargs.pop('config_file', None)

        # set default if no declaration is provided
        if config is None and config_file is None:
            config = self._get_trigger_endpoint()["defaultPostBody"]
        else:
            config = misc_utils.resolve_config(config, config_file)

        response, status_code = self._client.make_request(
            self._get_trigger_endpoint()['uri'],
            method='POST',
            body=config,
            advanced_return=True
        )

        # check for async task pattern response
        if status_code == constants.HTTP_STATUS_CODE['ACCEPTED']:
            return self._wait_for_task(response['selfLink'])
        # return response data
        return response

    def _reset(self, **kwargs):
        """Performs a POST against the component reset endpoint

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
            the API response
        """

        config = kwargs.pop('config', None)
        config_file = kwargs.pop('config_file', None)

        # set default if no declaration is provided
        if config is None and config_file is None:
            config = self._get_reset_endpoint()["defaultPostBody"]
        else:
            config = misc_utils.resolve_config(config, config_file)

        response, status_code = self._client.make_request(
            self._get_reset_endpoint()['uri'],
            method='POST',
            body=config,
            advanced_return=True
        )

        # check for async task pattern response
        if status_code == constants.HTTP_STATUS_CODE['ACCEPTED']:
            return self._wait_for_task(response['selfLink'])
        # return response data
        return response
