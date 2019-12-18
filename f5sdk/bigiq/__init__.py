"""Module for BIG-IQ

    Example - Basic::

        from f5sdk.bigiq import ManagementClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        # get device info (version, etc.)
        device.get_info()
"""

from .mgmt_client import ManagementClient

__all__ = [
    'ManagementClient'
]
