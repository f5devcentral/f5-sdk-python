"""Python module for BIG-IQ

    Example - Basic::

        from f5cloudsdk.bigiq import ManagementClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        # get device info - version, etc.
        device.get_info()

    Example - Licensing (Utility Pool)::

        IMPORTANT URI(S) (remove before merge):
        # list licenses
        /mgmt/cm/device/licensing/pool/utility/licenses
        # list license offerings
        /mgmt/cm/device/licensing/pool/utility/licenses/{id}/offerings
        # list license offering members
        /mgmt/cm/device/licensing/pool/utility/licenses/{id}/offerings/{regkey}/members

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing import PoolUtilityClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = PoolUtilityClient(device)

        # list pools
        license_client.list()

        # show pool
        license_client.show(name='my_pool')

        # create pool
        license_client.create(
            config={
                'name': 'my_pool',
                'baseRegKey': 'xxxx',
                'method': 'AUTOMATIC'
            }
        )

        # delete pool
        license_client.delete(name='my_pool')

        # list pool offerings
        license_client.offerings.list(name='my_pool')

        # add offering to pool
        license_client.offerings.create(
            name='my_pool',
            offering='my_offering',
            config={
                'regkey': 'xxxx'
            }
        )

        # delete offering from pool
        license_client.offerings.delete(
            name='my_pool', offering='my_offering', regkey='my_reg_key')

        # list pool offering members
        license_client.offerings.list_members(name='my_pool', offering='my_offering')

        # assign member to offering - managed or unmanaged
        license_client.offerings.create_member(
            name='my_pool',
            offering='my_offering',
            config={
                'deviceAddress': 'x.x.x.x'
            }
        )

        # delete member from offering - managed or unmanaged
        license_client.offerings.delete_member(
            name='my_pool',
            offering='my_offering',
            member_id='1234',
            config={
                'id': '1234',
                'username': 'admin',
                'password': 'admin'
            }
        )
"""

from .mgmt_client import ManagementClient

__all__ = ['ManagementClient']
