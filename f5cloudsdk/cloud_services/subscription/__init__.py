"""Python module for Cloud Services

    Example - Basic::

        from f5cloudsdk.cloud_services import ManagementClient
        from f5cloudsdk.cloud_services.subscription import SubscriptionClient

        mgmt_client = ManagementClient(user='admin', password='admin')

        # configure subscription - DNS zones, records, etc.
        subscription_client = SubscriptionClient(mgmt_client, subscription_id='')
        subscription_client.update(config_file='./decl.json')

    Example - Show::

        subscription_client.show()

    Example - Create + Activate (Not Implemented)::

        # Note: SubscriptionClient() should not include subscription_id if creating
        subscription_client.create()
        subscription_client.activate()

    Example - Retire (Not Implemented)::

        subscription_client.retire()

"""

from f5cloudsdk.logger import Logger
from f5cloudsdk.exceptions import InputRequiredError
from f5cloudsdk.utils import utils

SUBSCRIPTION_URI = '/v1/svc-subscription/subscriptions/%s'

class SubscriptionClient(object):
    """A class used as a subscription client for Cloud Services

    Attributes
    ----------
    logger : object
        instantiated logger object

    Methods
    -------
    show()
        Refer to method documentation
    update()
        Refer to method documentation
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
        subscription_id : str
            the subscription ID for the service

        Returns
        -------
        None
        """

        self.logger = Logger(__name__).get_logger()

        self._client = client

        # process kwargs
        self._subscription_id = kwargs.pop('subscription_id', None)

        # require subscription_id - this is a kwarg as the subscription ID could be
        # auto-discovered based on logic like user -> account ID -> subscription
        if not self._subscription_id:
            raise InputRequiredError('subscription_id required')

    def show(self):
        """Gets (shows) the subscription details

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the subscription details
        """

        uri = SUBSCRIPTION_URI % (self._subscription_id)
        return self._client.make_request(uri)

    def update(self, **kwargs):
        """Updates (PUT) the subscription

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
            the response to a subscription update
        """

        config = kwargs.pop('config', None)
        config_file = kwargs.pop('config_file', None)

        config = utils.resolve_config(config, config_file)

        uri = SUBSCRIPTION_URI % (self._subscription_id)
        return self._client.make_request(uri, method='PUT', body=config)
