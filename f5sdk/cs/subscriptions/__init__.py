"""Module for Cloud Services subscriptions

    Example - Update Subscription::

        from f5sdk.cs.subscriptions import SubscriptionClient

        subscription_client = SubscriptionClient(mgmt_client)

        # configure subscription - DNS zones, records, etc.
        subscription_client.update(
            name='subscription_id',
            config_file='./decl.json'
        )

    Example - List Subscriptions::

        from f5sdk.cs.subscriptions import SubscriptionClient

        subscription_client = SubscriptionClient(mgmt_client)

        # configure subscription - DNS zones, records, etc.
        subscription_client.list(
            query_parameters={
                'account_id': ''
            }
        )
"""

from .subscription import SubscriptionClient

__all__ = [
    'SubscriptionClient'
]
