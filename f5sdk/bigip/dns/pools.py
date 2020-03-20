"""Module for BIG-IP DNS pools management"""

from f5sdk.base_clients import BaseFeatureClient

BASE_URI = '/mgmt/tm/gtm/pool'


class PoolsClient(BaseFeatureClient):
    """BIG-IP DNS pools client

    Attributes
    ----------

    Methods
    -------
    list()
        Refer to method documentation
    create()
        Refer to method documentation
    show()
        Refer to method documentation
    update()
        Refer to method documentation
    delete()
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
        super(PoolsClient, self).__init__(
            client,
            logger_name=__name__,
            uri=BASE_URI+kwargs.pop('record_type', '')
        )

    def list(self, **kwargs):
        """List operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        query_parameters : dict
            Query parameters for the request

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._list(**kwargs)

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

    def show(self, **kwargs):
        """Show operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._show(**kwargs)

    def update(self, **kwargs):
        """Update operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._update(**kwargs)

    def delete(self, **kwargs):
        """Delete operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._delete(**kwargs)
