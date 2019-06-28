"""Utility module for bigip test cases """

# project imports
from f5cloudsdk.bigip import ManagementClient

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

    if token:
        return ManagementClient(HOST, port=port, token=token)
    if private_key_file:
        return ManagementClient(HOST,
                                port=port,
                                user=user,
                                private_key_file=private_key_file,
                                set_user_password=pwd)
    return ManagementClient(HOST, port=port, user=user, password=pwd)
