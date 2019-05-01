"""Utility module for bigip test cases """

# SDK imports
from f5cloudsdk.bigip import ManagementClient

def get_mgmt_client(**kwargs):
    """ Helper function to create mgmt client """

    user = kwargs.pop('user', '')
    pwd = kwargs.pop('pwd', '')
    token = kwargs.pop('token', '')
    if token:
        return ManagementClient('192.0.2.1', token=token)
    return ManagementClient('192.0.2.1', user=user, password=pwd)
