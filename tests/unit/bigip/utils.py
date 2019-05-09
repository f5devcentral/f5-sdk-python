"""Utility module for bigip test cases """

## project imports ##
from f5cloudsdk.bigip import ManagementClient

def get_mgmt_client(**kwargs):
    """Create mgmt client instance

    Parameters
    ----------
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    user : str
        the user to pass to client
    pwd : str
        the pwd to pass to client
    token : str
        the token to pass to client
    port : int
        the port to pass to client

    Returns
    -------
    obj
        mgmt client instance
    """

    user = kwargs.pop('user', '')
    pwd = kwargs.pop('pwd', '')
    token = kwargs.pop('token', '')
    port = kwargs.pop('port', 443)

    if token:
        return ManagementClient('192.0.2.1', port=port, token=token)
    return ManagementClient('192.0.2.1', port=port, user=user, password=pwd)
