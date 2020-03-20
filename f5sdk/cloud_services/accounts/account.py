"""Account Client"""

from f5sdk.base_clients import BaseFeatureClient


class AccountClient(BaseFeatureClient):
    """Cloud Services accounts client

    Attributes
    ----------

    Methods
    -------
    show_user()
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

        super(AccountClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/v1/svc-account'
        )

    def show_user(self):
        """Show information for the currently authenticated user

        Parameters
        ----------
        None

        Keyword Arguments
        -----------------
        None

        Returns
        -------
        None

        """

        return self._make_request(
            uri='%s/%s' % (self._metadata['uri'], 'user')
        )
