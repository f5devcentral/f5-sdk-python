"""Module for BIG-IQ license pool (utility) management"""

from f5cloudsdk.base_clients import BaseFeatureClient

BASE_URI = '/mgmt/cm/device/licensing/pool/utility/licenses'


class UtilityClient(BaseFeatureClient):
    """BIG-IQ license pool utility client

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
