"""Python module for BIG-IP toolchain configuration

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.toolchain import ToolChainClient
        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        as3 = ToolChainClient(device, 'as3')
        # install AS3 package
        as3.package.install()
        # create AS3 service
        as3.service.create(config_file='./decl.json')

    Example - Specify Component Version::

        as3 = ToolChainClient(device, 'as3', version='3.9.0')
"""

import os
import json

from .package import OperationClient as PackageClient
from .service import OperationClient as ServiceClient

TOOLCHAIN_METADATA = 'toolchain_metadata.json'

class MetadataClient(object):
    """A class used as a metadata client

    Attributes
    ----------
    component : str
        the component in the toolchain
    version : str
        the component version in the toolchain
    toolchain_metadata : dict
        the toolchain metadata

    Methods
    -------
    get_download_url()
        Refer to method documentation
    get_package_name()
        Refer to method documentation
    get_endpoints()
        Refer to method documentation
    """

    def __init__(self, component, version):
        """Class initialization

        Parameters
        ----------
        component : str
            the component in the toolchain
        version : str
            the component version in the toolchain

        Returns
        -------
        None
        """

        self.toolchain_metadata = self._load_metadata()
        self.component = self._validate_component(component)
        self.version = self._validate_component_version(
            self.component,
            version or self._get_latest_version()
            )

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
        component : str
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
        component : str
            a toolchain component to check
        version : str
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

    def _get_component_metadata(self):
        """Gets the metadata for a specific component from the toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the metadata
        """

        return self.toolchain_metadata['components'][self.component]

    def _get_version_metadata(self):
        """Gets the metadata for a specific component version from the toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the metadata
        """

        return self.toolchain_metadata['components'][self.component]['versions'][self.version]

    def get_download_url(self):
        """Gets the component versions download url from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the download url
        """

        return self._get_version_metadata()['downloadUrl']

    def get_package_name(self):
        """Gets the component versions package name from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the package name
        """

        return self._get_version_metadata()['packageName']

    def get_endpoints(self):
        """Gets the component endpoints from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the endpoints
        """

        return self._get_component_metadata()['endpoints']

class ToolChainClient(object):
    """A class used as a toolchain client for BIG-IP

    Attributes
    ----------
    component : str
        the component in the toolchain
    version : str
        the component version in the toolchain
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
        self._metadata_client = MetadataClient(component, kwargs.pop('version', None))
        self.component = self._metadata_client.component
        self.version = self._metadata_client.version

    @property
    def package(self):
        """ Package (see PackageClient for more details) """
        return PackageClient(self._client, self.component, self.version, self._metadata_client)

    @property
    def service(self):
        """ Service (see ServiceClient for more details)  """
        return ServiceClient(self._client, self.component, self.version, self._metadata_client)
