"""Python module for BIG-IP DNS

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.dns import DataCentersClient
        from f5cloudsdk.bigip.dns import VirtualServersClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        datacenters_client = DataCentersClient(device)
        virtualservers_client = VirtualServersClient(device)

        # list
        datacenters_client.list()
        virtualservers_client.list()

        # create
        datacenters_client.create(
            config={
                'name': 'my_datacenter'
            }
        )
        virtualservers_client.create(
            config={
                'name': 'my_virtual_server'
            }
        )


        # show
        datacenters_client.show(name='my_datacenter')
        virtualservers_client.show(name='my_virtual_server')

        # update dns datacenter
        datacenters_client.update(
            name='my_offering_id',
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete
        datacenters_client.delete(name='my_datacenter')
        virtualservers_client.delete(name='my_virtual_server')
"""

from .datacenters import DataCentersClient
from .virtualservers import VirtualServersClient

__all__ = [
    'DataCentersClient',
    'VirtualServersClient'
]
