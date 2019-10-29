"""Module for Cloud Services subscriptions subscription client"""

from f5cloudsdk.base_clients import BaseFeatureClient


class SubscriptionClient(BaseFeatureClient):
    """A class used as a subscription client for Cloud Services

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

        super(SubscriptionClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/v1/svc-subscription/subscriptions'
        )
