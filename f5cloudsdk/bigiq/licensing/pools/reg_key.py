"""Module for BIG-IQ license pool (reg key) management"""

from f5cloudsdk.base_clients import BaseFeatureClient

BASE_URI = '/mgmt/cm/device/licensing/pool/regkey/licenses'


class RegKeyClient(BaseFeatureClient):
    """BIG-IQ license pool reg key client

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

        super(RegKeyClient, self).__init__(
            client,
            logger_name=__name__,
            uri=BASE_URI
        )


class RegKeyOfferingsClient(BaseFeatureClient):
    """BIG-IQ license pool reg key offerings client

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

        super(RegKeyOfferingsClient, self).__init__(
            client,
            logger_name=__name__,
            uri='%s/%s/offerings' % (BASE_URI, self._pool_name)
        )


class RegKeyOfferingMembersClient(BaseFeatureClient):
    """BIG-IQ license pool reg key offering members client

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

        super(RegKeyOfferingMembersClient, self).__init__(
            client,
            logger_name=__name__,
            uri='%s/%s/offerings/%s/members' % (BASE_URI, self._pool_name, self._offering_name)
        )
