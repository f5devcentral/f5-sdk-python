"""Python module for F5 Cloud Services

    Example - Basic::

        from f5sdk.cloud_services import ManagementClient
        from f5sdk.cloud_services.subscriptions import SubscriptionClient

        mgmt_client = ManagementClient(user='admin', password='admin')

        subscription_client = SubscriptionClient(mgmt_client)

        # configure subscription - DNS zones, records, etc.
        subscription_client.update(
            name='subscription_id',
            config_file='./decl.json'
        )
"""

from .mgmt_client import ManagementClient

__all__ = [
    'ManagementClient'
]
