"""Python module for BIG-IP DNS

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.dns import DataCentersClient
        from f5sdk.bigip.dns import ServersClient
        from f5sdk.bigip.dns import PoolsClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        datacenters_client = DataCentersClient(device)
        servers_client = ServersClient(device)
        pools_client = PoolsClient(device)

        # create/list/update/delete various record types
        pools_client = PoolsClient(device, record_tye='a')

        # list
        datacenters_client.list()
        servers_client.list()
        pools_client.list()

        # create
        datacenters_client.create(
            config={
                'name': 'my_datacenter'
            }
        )
        servers_client.create(
            config={
                'name': 'my_server'
            }
        )
        pools_client.create(
            config={
                'name': 'my_pool'
            }
        )

        # show
        datacenters_client.show(name='my_datacenter')
        servers_client.show(name='my_server')
        pools_client.show(name='my_pool')

        # update dns datacenter
        datacenters_client.update(
            name='my_offering_id',
            config={
                'regkey': 'my_reg_key'
            }
        )
        # update server
        servers_client.update(
            name='my_server',
            config={
                'description': 'added description'
            }
        )
        # update pool
        pools_client.update(
            name='my_pool',
            config={
                'description': 'added description'
            }
        )

        # delete
        datacenters_client.delete(name='my_datacenter')
        servers_client.delete(name='my_server')
        pools_client.delete(name='my_pool')
"""

from .datacenters import DataCentersClient
from .servers import ServersClient
from .pools import PoolsClient

__all__ = [
    'DataCentersClient',
    'ServersClient',
    'PoolsClient'
]
