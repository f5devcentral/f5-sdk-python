"""Module for BIG-IQ license assignment

    Example - Basic::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing import AssignmentClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = AssignmentClient(device)

        # list license assignments
        license_client.list()
"""

from f5cloudsdk.base_clients import BaseFeatureClient

class AssignmentClient(BaseFeatureClient):
    """BIG-IQ license assignment client

    Attributes
    ----------

    Methods
    -------

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

    def create(self, **kwargs):
        """ Unsupported method """

        raise self._exceptions['UnsupportedMethod']
