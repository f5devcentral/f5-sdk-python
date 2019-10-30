"""Python module for a specific provider """

from boto3.session import Session

from ..abstract import AbstractProviderClient
from .virtual_machines import OperationClient as VirtualMachinesClient


class ProviderClient(AbstractProviderClient):
    """A class used as a provider client for AWS

    Attributes
    ----------
    session : object
        the session for the provider
    """

    def __init__(self, **kwargs):
        """Class initialization

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        access_key : str, optional
            the access key
        secret_key : str, optional
            the secret key
        region_name : str
            the region name

        Returns
        -------
        None
        """

        self._access_key = kwargs.pop('access_key', None)
        self._secret_key = kwargs.pop('secret_key', None)
        self._region_name = kwargs.pop('region_name', 'us-west-1')

        if self._access_key and self._secret_key:
            self.session = self._get_session()
        else:
            raise Exception('Valid credentials must be provided')

    def _get_session(self):
        """Get session object

        Parameters
        ----------
        None

        Returns
        -------
        object
            instantiated session object
        """
        session = Session(
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key
        )
        return session

    def is_logged_in(self):
        """Checks if is logged in

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if there is an instantiated session object
        """

        return bool(self.session)

    @property
    def virtual_machines(self):
        """Virtual machines client """
        return VirtualMachinesClient(self.session, self._region_name)
