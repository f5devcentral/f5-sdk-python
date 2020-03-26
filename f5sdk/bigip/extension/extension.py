"""Python module containing BIG-IP Extension clients"""

from f5sdk.logger import Logger

from .extension_metadata import MetadataClient
from .package import OperationClient as PackageClient
from .service import OperationClient as ServiceClient


class AS3Client(object):
    """AS3 client

    Attributes
    ----------
    component : str
        the extension component
    version : str
        the extension component version
    """

    def __init__(self, client, **kwargs):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
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

        self.logger = Logger(__name__).get_logger()

        self._client = client
        self._metadata_client = MetadataClient(
            'as3',
            kwargs.pop('version', None),
            use_latest_metadata=kwargs.pop('use_latest_metadata', False)
        )
        self.component = self._metadata_client.component
        self.version = self._metadata_client.version

    @property
    def package(self):
        """ Package (see PackageClient for more details) """
        return PackageClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )

    @property
    def service(self):
        """ Service (see ServiceClient for more details)  """
        return ServiceClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )


class DOClient(object):
    """DO client

    Attributes
    ----------
    component : str
        the extension component
    version : str
        the extension component version
    """

    def __init__(self, client, **kwargs):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
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

        self.logger = Logger(__name__).get_logger()

        self._client = client
        self._metadata_client = MetadataClient(
            'do',
            kwargs.pop('version', None),
            use_latest_metadata=kwargs.pop('use_latest_metadata', False)
        )
        self.component = self._metadata_client.component
        self.version = self._metadata_client.version

    @property
    def package(self):
        """ Package (see PackageClient for more details) """
        return PackageClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )

    @property
    def service(self):
        """ Service (see ServiceClient for more details)  """
        return ServiceClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )

class TSClient(object):
    """TS client

    Attributes
    ----------
    component : str
        the extension component
    version : str
        the extension component version
    """

    def __init__(self, client, **kwargs):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
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

        self.logger = Logger(__name__).get_logger()

        self._client = client
        self._metadata_client = MetadataClient(
            'ts',
            kwargs.pop('version', None),
            use_latest_metadata=kwargs.pop('use_latest_metadata', False)
        )
        self.component = self._metadata_client.component
        self.version = self._metadata_client.version

    @property
    def package(self):
        """ Package (see PackageClient for more details) """
        return PackageClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )

    @property
    def service(self):
        """ Service (see ServiceClient for more details)  """
        return ServiceClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )


class CFClient(object):
    """CF client

    Attributes
    ----------
    component : str
        the extension component
    version : str
        the extension component version
    """

    def __init__(self, client, **kwargs):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
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

        self.logger = Logger(__name__).get_logger()

        self._client = client
        self._metadata_client = MetadataClient(
            'cf',
            kwargs.pop('version', None),
            use_latest_metadata=kwargs.pop('use_latest_metadata', False)
        )
        self.component = self._metadata_client.component
        self.version = self._metadata_client.version

    @property
    def package(self):
        """ Package (see PackageClient for more details) """
        return PackageClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )

    @property
    def service(self):
        """ Service (see ServiceClient for more details)  """
        return ServiceClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )
