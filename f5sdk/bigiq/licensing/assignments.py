"""Module for BIG-IQ license assignment"""

from f5sdk.base_clients import BaseFeatureClient


class AssignmentClient(BaseFeatureClient):
    """BIG-IQ license assignment client

    Attributes
    ----------

    Methods
    -------
    list()
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

        super(AssignmentClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/mgmt/cm/device/licensing/assignments'
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
