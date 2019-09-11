"""Python module for F5 Cloud Services

    Example - Basic::

        from f5cloudsdk.cloud_services import ManagementClient
        from f5cloudsdk.cloud_services.subscription import SubscriptionClient

        mgmt_client = ManagementClient(user='admin', password='admin')

        # configure subscription - DNS zones, records, etc.
        subscription_client = SubscriptionClient(mgmt_client, subscription_id='')
        subscription_client.update(config_file='./decl.json')

"""

from .mgmt_client import ManagementClient

__all__ = ['ManagementClient']
