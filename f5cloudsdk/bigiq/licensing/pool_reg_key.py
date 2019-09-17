"""Module for BIG-IQ license pool (reg key) management

    Example - Basic::

        DEV: IMPORTANT URI(S)
        # list licenses
        /mgmt/cm/device/licensing/pool/regkey/licenses
        # list license offerings
        /mgmt/cm/device/licensing/pool/regkey/licenses/{id}/offerings
        # list license offering members
        /mgmt/cm/device/licensing/pool/regkey/licenses/{id}/offerings/{regkey}/members

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing import PoolRegKeyClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = PoolRegKeyClient(device, pool_name='my_pool', offering_name='my_offering')

        # list license pools
        license_client.list()

        # create license pool
        license_client.create(
            config={
                'name': 'my_pool'
            }
        )

        # show license pool details
        license_client.show(name='my_pool')

        # update license pool
        license_client.update(
            config={
                'name': 'my_pool'
            }
        )

        # delete license pool
        license_client.delete(name='my_pool')

    Example - Offerings::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing import PoolRegKeyClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = PoolRegKeyClient(device, pool_name='my_pool_name')

        # list license pool offerings
        license_client.offerings.list()

        # create (add) offering to license pool
        license_client.offerings.create(
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete offering from license pool
        license_client.offerings.delete(name='my_offering')

    Example - Offering Members::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing import PoolRegKeyClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = PoolRegKeyClient(
            device,
            pool_name='my_pool_name',
            offering_name='my_offering_name'
        )

        # list license pool offering members
        license_client.offerings.members.list(name='my_reg_key)

        # create (assign) member in offering - managed or unmanaged
        license_client.offerings.members.create(
            config={
                'deviceAddress': 'x.x.x.x'
            }
        )

        # delete member from offering - managed or unmanaged
        license_client.offerings.members.delete(
            member_id='1234',
            config={
                'id': '1234',
                'username': 'admin',
                'password': 'admin'
            }
        )

"""

from f5cloudsdk.base_clients import BaseFeatureClient

class PoolRegKeyClient(BaseFeatureClient):
    """BIG-IQ pool reg key client

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

        self._pool_name = kwargs.pop('pool_name', None)

        super(PoolRegKeyClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/mgmt/cm/device/licensing/pool/regkey/licenses'
        )

    @property
    def offerings(self):
        """ Offerings (see OfferingsClient for more details) """
        return OfferingsClient(
            self._client,
            uri='%s/%s/offerings' % (self._metadata['uri'], self._pool_name)
        )

class OfferingsClient(BaseFeatureClient):
    """BIG-IQ pool reg key offering client

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
        uri : str
            the REST URI against which this client operates

        Returns
        -------
        None

        """

        super(OfferingsClient, self).__init__(
            client,
            logger_name=__name__,
            uri=kwargs.pop('uri', None)
        )
