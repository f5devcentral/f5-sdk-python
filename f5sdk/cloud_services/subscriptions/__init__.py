"""Module for Cloud Services subscriptions

    Example - Update Subscription::

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

from .subscription import SubscriptionClient

__all__ = [
    'SubscriptionClient'
]
