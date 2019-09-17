"""Module for BIG-IQ license pool (utility) management

    Example - Basic::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing.pool import UtilityClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = UtilityClient(device)

        # list license pools
        license_client.list()

        # create license pool
        license_client.create(
            config={
                'name': 'my_pool'
            }
        )

        # show license pool details
        license_client.show(name='my_pool_id')

        # update license pool
        license_client.update(
            name='my_pool_id',
            config={
                'name': 'my_pool'
            }
        )

        # delete license pool
        license_client.delete(name='my_pool_id')

    Example - Offerings::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing.pool import UtilityOfferingsClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        offerings_client = UtilityOfferingsClient(
            device,
            pool_name='my_pool_name'
        )

        # list license pool offerings
        offerings_client.list()

        # create (add) offering to license pool
        offerings_client.create(
            config={
                'regkey': 'my_reg_key'
            }
        )

        # show license pool offering details
        offerings_client.show(name='my_offering_id')

        # update offering in license pool
        offerings_client.update(
            name='my_offering_id',
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete offering from license pool
        offerings_client.delete(name='my_offering_id')

    Example - Offering Members::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing.pool import UtilityOfferingMembersClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        members_client = UtilityOfferingMembersClient(
            device,
            pool_name='my_pool_name',
            offering_name='my_offering_name'
        )

        # list license pool offering members
        members_client.list()

        # create (assign) member in license pool offering - managed or unmanaged
        members_client.create(
            config={
                'deviceAddress': 'x.x.x.x'
            }
        )

        # show license pool offering member details
        members_client.show(name='my_member_id')

        # update member in license pool offering
        members_client.update(
            name='my_member_id',
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete (revoke) member from license pool offering - managed or unmanaged
        members_client.delete(
            name='my_member_id',
            config={
                'id': 'my_member_id',
                'username': 'admin',
                'password': 'admin'
            }
        )

"""

from f5cloudsdk.base_clients import BaseFeatureClient

BASE_URI = '/mgmt/cm/device/licensing/pool/utility/licenses'

class UtilityClient(BaseFeatureClient):
    """BIG-IQ license pool utility client

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

        super(UtilityClient, self).__init__(
            client,
            logger_name=__name__,
            uri=BASE_URI
        )

class UtilityOfferingsClient(BaseFeatureClient):
    """BIG-IQ license pool utility offerings client

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
        pool_name : str
            the pool name against which this client should operate

        Returns
        -------
        None

        """

        self._pool_name = kwargs.pop('pool_name', None)

        super(UtilityOfferingsClient, self).__init__(
            client,
            logger_name=__name__,
            uri='%s/%s/offerings' % (BASE_URI, self._pool_name)
        )

class UtilityOfferingMembersClient(BaseFeatureClient):
    """BIG-IQ license pool utility offering members client

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
        pool_name : str
            the pool name against which this client should operate
        offering_name : str
            the offering name against which this client should operate

        Returns
        -------
        None
        """

        self._pool_name = kwargs.pop('pool_name', None)
        self._offering_name = kwargs.pop('offering_name', None)

        super(UtilityOfferingMembersClient, self).__init__(
            client,
            logger_name=__name__,
            uri='%s/%s/offerings/%s/members' % (BASE_URI, self._pool_name, self._offering_name)
        )
