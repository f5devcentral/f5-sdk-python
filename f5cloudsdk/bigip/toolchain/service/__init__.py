"""Python module for BIG-IP toolchain component service configuration

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.toolchain import ToolChainClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        as3 = ToolChainClient(device, 'as3')
        # configure AS3
        as3.service.create(config_file='./decl.json')

    Example - Show::

        as3.service.show()

    Example - Delete::

        as3.service.delete()

    Example - Is Available::

        as3.service.is_available()
"""

import os
import json
import time
import requests
from retry import retry

from f5cloudsdk import constants
from f5cloudsdk.utils import misc_utils
from f5cloudsdk.exceptions import InputRequiredError

class OperationClient(object):
    """A class used as a toolchain service operation client for BIG-IP

    Attributes
    ----------
    component : str
        the component in the toolchain
    version : str
        the component version in the toolchain

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
            the component in the toolchain
        version : str
            the component version in the toolchain
        metadata_client : object
            the toolchain metadata client

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
        Certain toolchain components support async task behavior,
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
        """Checks toolchain component service is available

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
        """Creates (or updates) toolchain component service

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
        """Gets (shows) the toolchain component service

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
        """Deletes toolchain component service

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
            raise Exception('Delete is not supported for this toolchain component')

        uri = self._get_configure_endpoint()['uri']
        return self._client.make_request(uri, method='DELETE')
        