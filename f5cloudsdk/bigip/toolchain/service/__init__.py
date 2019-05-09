"""Python module for BIG-IP toolchain component service configuration

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.toolchain import ToolChainClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        as3 = ToolChainClient(device, 'as3')
        # configure AS3 service
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

    @staticmethod
    def _load_config_file(file):
        """Load configuration file

        Notes
        -----
        Assumes the file is valid JSON

        Parameters
        ----------
        file : str
            location to configuration file

        Returns
        -------
        dict
            the loaded file
        """

        with open(file) as m_file:
            data = json.loads(m_file.read())
        return data

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

    def is_available(self):
        """Checks toolchain component service is available

        Notes
        -----
        Retries up to 120 seconds

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
        while i < 120:
            if self._client.make_request(uri, bool_response=True):
                ret = True
                break
            i += 1
            time.sleep(1)

        return ret

    def create(self, **kwargs):
        """Creates toolchain component service

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

        config = kwargs.pop('config', '')
        config_file = kwargs.pop('config_file', '')

        if not config and not config_file:
            raise InputRequiredError('One of config|config_file must be provided')

        if config_file:
            config = self._load_config_file(config_file)

        uri = self._get_configure_endpoint()['uri']
        return self._client.make_request(uri, method='POST', body=config)

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
        