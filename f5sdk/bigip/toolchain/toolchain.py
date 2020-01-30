"""Python module for BIG-IP toolchain component configuration, including AS3, DO and TS

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.toolchain import ToolChainClient
        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        as3 = ToolChainClient(device, 'as3')
        # install AS3 package
        as3.package.install()
        # check service is available
        as3.service.is_available()
        # configure AS3
        as3.service.create(config_file='./decl.json')

    Example - Specify Component Type::

        do = ToolChainClient(device, 'do')
        ts = ToolChainClient(device, 'ts')

    Example - Specify Component Version::

        as3 = ToolChainClient(device, 'as3', version='3.9.0')
"""

from .toolchain_metadata import MetadataClient
from .package import OperationClient as PackageClient
from .service import OperationClient as ServiceClient


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
        use_latest_metadata : bool
            use latest metadata (will be retrieved from remote CDN)

        Returns
        -------
        None
        """

        self._client = client
        self._metadata_client = MetadataClient(
            component,
            kwargs.pop('version', None),
            use_latest_metadata=kwargs.pop('use_latest_metadata', True)
        )
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
