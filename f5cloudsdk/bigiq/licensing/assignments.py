"""Module for BIG-IQ license assignment"""

from f5cloudsdk.base_clients import BaseFeatureClient


class AssignmentClient(BaseFeatureClient):
    """BIG-IQ license assignment client

    Attributes
    ----------

    Methods
    -------
    list()
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

        super(AssignmentClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/mgmt/cm/device/licensing/assignments'
        )

    def create(self, **kwargs):
        """ Method not allowed (action:skip_documentation) """

        raise self._exceptions['MethodNotAllowed']

    def show(self, **kwargs):
        """ Method not allowed (action:skip_documentation) """

        raise self._exceptions['MethodNotAllowed']

    def update(self, **kwargs):
        """ Method not allowed (action:skip_documentation) """

        raise self._exceptions['MethodNotAllowed']

    def delete(self, **kwargs):
        """ Method not allowed (action:skip_documentation) """

        raise self._exceptions['MethodNotAllowed']
