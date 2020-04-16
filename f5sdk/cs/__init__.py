"""Python module for F5 Cloud Services

    Example - Basic::

        from f5sdk.cs import ManagementClient
        from f5sdk.cs.accounts import AccountClient
        from f5sdk.cs.subscriptions import SubscriptionClient

        mgmt_client = ManagementClient(user='admin', password='admin')
        account_client = AccountClient(mgmt_client)
        subscription_client = SubscriptionClient(mgmt_client)

        # discover account/subscription ID
        account_id = account_client.show_user()['primary_account_id']
        subscription_id = subscription_client.list(
            query_parameters={
                'account_id': account_id
            }
        )['subscriptions'][0]['subscription_id']

        # configure subscription - GSLB, etc.
        subscription_client.update(
            name=subscription_id,
            config_file='./decl.json'
        )
"""

from .mgmt_client import ManagementClient

__all__ = [
    'ManagementClient'
]
