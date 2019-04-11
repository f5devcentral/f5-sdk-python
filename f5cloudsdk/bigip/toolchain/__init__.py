""" Module for BIG-IP toolchain configuration

    Examples
    --------
    Example: Basic
    --------------
    from f5cloudsdk.bigip import ManagementClient
    from f5cloudsdk.bigip.toolchain import ToolChainClient
    device = ManagementClient('192.0.2.10', user='admin', password='admin')

    as3 = ToolChainClient(device, 'as3')
    # install AS3 package
    as3.package.install()
    # create AS3 service
    as3.service.create('./my_local_decl')

    Example: Specify Component Version
    --------------
    as3 = ToolChainClient(device, 'as3', version='3.9.0')
"""

import os
import json

from .package import Operation as packageClient
from .service import Operation as serviceClient

TOOLCHAIN_METADATA = 'toolchain_metadata.json'

class ToolChainClient():
    """A class used as a toolchain client for BIG-IP

    Attributes
    ----------
    component : str
        the component in the toolchain
    version : str
        the component version in the toolchain
    toolchain_metadata : dict
        the toolchain metadata
    """

    def __init__(self, client, component, **kwargs):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
        component : str
            the component in the toolchain
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        version : str
            a string specifying the component version to use

        Returns
        -------
        None
        """

        self._client = client
        self.toolchain_metadata = self._load_metadata()
        self.component = self._validate_component(component)
        self.version = self._validate_component_version(
            self.component,
            kwargs.pop('version', self._get_latest_version())
        )

    @property
    def package(self):
        """ Package (see packageClient for more details) """
        return packageClient(self._client, self.component, self.version, self.toolchain_metadata)

    @property
    def service(self):
        """ Service (see serviceClient for more details)  """
        return serviceClient(self._client, self.component, self.version, self.toolchain_metadata)

    @staticmethod
    def _load_metadata():
        """Load toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containg the JSON metadata
        """

        with open(os.path.join(os.path.dirname(__file__), TOOLCHAIN_METADATA)) as m_file:
            metadata = json.loads(m_file.read())
        return metadata

    def _get_latest_version(self):
        """Gets the latest component version from the toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the latest version
        """

        c_v_metadata = self.toolchain_metadata['components'][self.component]['versions']
        latest = {k: v for (k, v) in c_v_metadata.items() if v['latest']}
        return list(latest.keys())[0] # we should only have one

    def _validate_component(self, component):
        """Validates the toolchain component exists in metadata

        Parameters
        ----------
        component: str
            a toolchain component to check

        Returns
        -------
        str
            the toolchain component provided if it exists (see Raises)

        Raises
        ------
        Exception
            if the toolchain component does not exist in metadata
        """

        components = list(self.toolchain_metadata['components'].keys())
        if not [i for i in components if i == component]:
            raise Exception('Valid component must be provided: %s' % (components))
        return component

    def _validate_component_version(self, component, version):
        """Validates the toolchain component version exists in metadata

        Parameters
        ----------
        component: str
            a toolchain component to check
        version: str
            a toolchain component version to check

        Returns
        -------
        str
            the toolchain component version provided if it exists (see Raises)

        Raises
        ------
        Exception
            if the toolchain component version does not exist in metadata
        """

        versions = list(self.toolchain_metadata['components'][component]['versions'].keys())
        if not [i for i in versions if i == version]:
            raise Exception('Valid component version must be provided: %s' % (versions))
        return version
