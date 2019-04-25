"""Specific provider module """

from boto3.session import Session

from .virtual_machines import OperationClient as VirtualMachinesClient

class ProviderClient(object):
    """A class used as a provider client for AWS

    Attributes
    ----------
    access_key : str, optional
        the access key
    secret_key : str, optional
        the secret key
    region_name : str
        the region name
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

        self.access_key = kwargs.pop('access_key', None)
        self.secret_key = kwargs.pop('secret_key', None)
        self.region_name = kwargs.pop('region_name', 'us-west-1')

        if self.access_key and self.secret_key:
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
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
        return session

    @property
    def virtual_machines(self):
        """Virtual machines client """
        return VirtualMachinesClient(self.session, self.region_name)
