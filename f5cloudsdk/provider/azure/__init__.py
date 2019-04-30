"""Specific provider module """

from azure.common.credentials import ServicePrincipalCredentials

from .virtual_machines import OperationClient as VirtualMachinesClient

class ProviderClient(object):
    """A class used as a provider client for Azure

    Attributes
    ----------
    credentials : object
        the credentials for the provider
    """

    def __init__(self, **kwargs):
        """Class initialization

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        subscription_id : str
            the subscription key
        client_id : str
            the service principal client id
        tenant_id : str
            the service principal tenant id
        secret : str
            the service principal secret

        Returns
        -------
        None
        """

        self._subscription_id = kwargs.pop('subscription_id', None)
        self._client_id = kwargs.pop('client_id', None)
        self._tenant_id = kwargs.pop('tenant_id', None)
        self._secret = kwargs.pop('secret', None)

        # optional, since this might be available via metadata
        if not self._subscription_id:
            raise Exception('Valid subscription id must be provided')

        if self._client_id and self._tenant_id and self._secret:
            self.credentials = self._get_credentials()
        else:
            raise Exception('Valid credentials must be provided')

    def _get_credentials(self):
        """Get credentials object

        Parameters
        ----------
        None

        Returns
        -------
        object
            instantiated credentials object
        """
        credentials = ServicePrincipalCredentials(
            client_id=self._client_id,
            tenant=self._tenant_id,
            secret=self._secret
        )
        return credentials

    def is_logged_in(self):
        """Checks if is logged in

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if there is an instantiated credentials object
        """

        return bool(self.credentials)

    @property
    def virtual_machines(self):
        """Virtual machines client """
        return VirtualMachinesClient(self.credentials, self._subscription_id)
