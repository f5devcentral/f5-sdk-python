"""Module for BIG-IP

    Example - Basic::

        from f5sdk.bigip import ManagementClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        # get BIG-IP info (version, etc.)
        device.get_info()

    Example - Token Authentication::

        device = ManagementClient('192.0.2.10', token='my_token')

    Example - Key-Based Authentication::

        device = ManagementClient('192.0.2.10',
                                user='admin',
                                private_key_file='~/my_key',
                                set_user_password='admin')

"""

from .mgmt_client import ManagementClient

__all__ = [
    'ManagementClient'
]
