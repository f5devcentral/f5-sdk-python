"""Module for BIG-IQ license pool (reg key) management"""

from f5sdk.base_clients import BaseFeatureClient

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

    def show(self, **kwargs):
        """Show operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._show(**kwargs)

    def update(self, **kwargs):
        """Update operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._update(**kwargs)

    def delete(self, **kwargs):
        """Delete operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._delete(**kwargs)

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

    def show(self, **kwargs):
        """Show operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._show(**kwargs)

    def update(self, **kwargs):
        """Update operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._update(**kwargs)

    def delete(self, **kwargs):
        """Delete operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._delete(**kwargs)

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

    def show(self, **kwargs):
        """Show operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._show(**kwargs)

    def update(self, **kwargs):
        """Update operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._update(**kwargs)

    def delete(self, **kwargs):
        """Delete operation

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        name : str
            name (id) of the object to operate against
        config : dict
            object containing configuration
        config_file : str
            reference to a local file containing configuration

        Returns
        -------
        dict
            the serialized REST response
        """

        return self._delete(**kwargs)
