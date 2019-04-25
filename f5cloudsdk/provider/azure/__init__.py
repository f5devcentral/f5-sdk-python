"""Specific provider module """

from azure.common.credentials import ServicePrincipalCredentials

from .virtual_machines import OperationClient as VirtualMachinesClient

class ProviderClient(object):
    """A class used as a provider client for Azure

    Attributes
    ----------
    client_id : str, optional
        the service principal client id
    tenant_id : str, optional
        the service principal tenant id
    secret : str, optional
        the service principal secret
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

        self.subscription_id = kwargs.pop('subscription_id', None)
        self.client_id = kwargs.pop('client_id', None)
        self.tenant_id = kwargs.pop('tenant_id', None)
        self.secret = kwargs.pop('secret', None)

        # optional, since this might be available via metadata
        if not self.subscription_id:
            raise Exception('Valid subscription id must be provided')

        if self.client_id and self.tenant_id and self.secret:
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
            client_id=self.client_id,
            tenant=self.tenant_id,
            secret=self.secret
        )
        return credentials

    @property
    def virtual_machines(self):
        """Virtual machines client """
        return VirtualMachinesClient(self.credentials, self.subscription_id)
