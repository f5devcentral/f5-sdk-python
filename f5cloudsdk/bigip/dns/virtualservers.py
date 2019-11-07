"""Module for BIG-IP Virtual server management"""

from f5cloudsdk.base_clients import BaseFeatureClient

BASE_URI = '/mgmt/tm/gtm/server'


class VirtualServersClient(BaseFeatureClient):
    """BIG-IP virtual server management client

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

        super(VirtualServersClient, self).__init__(
            client,
            logger_name=__name__,
            uri=BASE_URI
        )
