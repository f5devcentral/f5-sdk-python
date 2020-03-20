"""Module for BIG-IQ license pool member management"""

from f5sdk.base_clients import BaseFeatureClient


class MemberManagementClient(BaseFeatureClient):
    """BIG-IQ license pool member management client

    Attributes
    ----------

    Methods
    -------
    list()
        Refer to method documentation
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

        super(MemberManagementClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/mgmt/cm/device/tasks/licensing/pool/member-management'
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
