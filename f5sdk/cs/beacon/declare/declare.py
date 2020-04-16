"""Beacon Declarative API Module"""

from f5sdk.base_clients import BaseFeatureClient


class DeclareClient(BaseFeatureClient):
    """Declarative API Client

    Attributes
    ----------

    Methods
    -------
    create()
        Refer to method documentation
    """

    def __init__(self, client, **kwargs):
        """Initialization

        Parameters
        ----------
        client : object
            the management client object
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        None

        Returns
        -------
        None

        """

        super(DeclareClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/beacon/v1/declare'
        )

    def create(self, **kwargs):
        """Create operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._create(**kwargs)
