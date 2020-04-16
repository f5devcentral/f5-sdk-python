"""Python module containing Cloud Failover Extension Client"""

from f5sdk.logger import Logger

from .extension_metadata import MetadataClient
from .package import OperationClient as PackageClient
from .service import OperationClient as ServiceClient


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
        """ Service (see CFServiceClient for more details)  """
        return CFServiceClient(
            self._client,
            self.component,
            self.version,
            self._metadata_client,
            logger=self.logger
        )


class CFServiceClient(ServiceClient):
    """CF service client

    Attributes
    ----------
    component : str
        the extension component
    version : str
        the extension component version
    """

    def __init__(self, client, component, version, metadata_client, **kwargs):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
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

        super(CFServiceClient, self).__init__(
            client,
            component,
            version,
            metadata_client,
            logger=kwargs.pop('logger', None)
        )

    def show_inspect(self, **kwargs):
        """Performs a show inspect operation

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

        return self._show_inspect(**kwargs)

    def reset(self, **kwargs):
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
            the API response to a service reset
        """

        return self._reset(**kwargs)

    def show_trigger(self):
        """Performs a GET against the component trigger endpoint

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the API response
        """

        return self._show_trigger()

    def trigger(self, **kwargs):
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

        return self._trigger(**kwargs)
