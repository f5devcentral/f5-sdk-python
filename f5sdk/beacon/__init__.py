"""Python module for F5 Beacon

    Example - Basic::

        from f5sdk.cs import ManagementClient
        from f5sdk.beacon.insights import InsightClient

        beacon_mgmt_client = ManagementClient(user='admin', password='admin')

"""

from .mgmt_client import ManagementClient

__all__ = [
    'ManagementClient'
]
