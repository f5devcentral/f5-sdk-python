"""Insights Client"""

from f5sdk.base_clients import BaseFeatureClient


class InsightsClient(BaseFeatureClient):
    """Beacon Insights Client

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

        super(InsightsClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/beacon/v1/insights'
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
        """Create/Update operation

        Note: Beacon insights REST API uses the just one method for create and update operation.
              Therefore here the update method calls the create method from the base client

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

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._show(**kwargs)

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
