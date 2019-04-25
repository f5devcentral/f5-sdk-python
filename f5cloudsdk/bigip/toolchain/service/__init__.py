"""Module for BIG-IP toolchain component service configuration """

class OperationClient(object):
    """A class used as a toolchain service operation client for BIG-IP

    Attributes
    ----------
    component : str
        the component in the toolchain
    version : str
        the component version in the toolchain
    toolchain_metadata : dict
        the toolchain metadata

    Methods
    -------
    create()
        Refer to method documentation
    """

    def __init__(self, client, component, version, toolchain_metadata):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
        component : str
            the component in the toolchain
        version : str
            the component version in the toolchain
        toolchain_metadata : dict
            the toolchain metadata

        Returns
        -------
        None
        """

        self._client = client
        self.component = component
        self.version = version
        self.toolchain_metadata = toolchain_metadata

    def create(self, **kwargs):
        """Creates toolchain component service

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
