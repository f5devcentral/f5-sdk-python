"""Utility module for bigip test cases """

# project imports
from f5sdk.bigip import ManagementClient

# local test imports
from ...shared import constants

HOST = constants.HOST
PORT = constants.PORT


def get_mgmt_client(**kwargs):
    """Create mgmt client instance

    Parameters
    ----------
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    user : str
        the user to pass to the client
    pwd : str
        the pwd to pass to the client
    token : str
        the token to pass to the client
    private_key_file : str
        the private_key_file to pass to the client
    port : int
        the port to pass to the client
    skip_ready_check : bool
        skip device ready check

    Returns
    -------
    obj
        mgmt client instance
    """

    user = kwargs.pop('user', '')
    pwd = kwargs.pop('pwd', '')
    private_key_file = kwargs.pop('private_key_file', '')
    token = kwargs.pop('token', '')
    port = kwargs.pop('port', PORT)
    skip_ready_check = kwargs.pop('skip_ready_check', True)

    mgmt_client_kwargs = {
        'port': port,
        'skip_ready_check': skip_ready_check
    }

    # update kwargs based on auth options
    if token:
        mgmt_client_kwargs['token'] = token
    elif private_key_file:
        mgmt_client_kwargs['user'] = user
        mgmt_client_kwargs['private_key_file'] = private_key_file
        mgmt_client_kwargs['set_user_password'] = pwd
    else:
        mgmt_client_kwargs['user'] = user
        mgmt_client_kwargs['password'] = pwd

    return ManagementClient(HOST, **mgmt_client_kwargs)
