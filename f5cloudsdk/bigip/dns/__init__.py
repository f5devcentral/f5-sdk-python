"""Python module for BIG-IP DNS

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.dns import DataCentersClient
        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        datacenters_client = DataCentersClient(device)

        # list datacenters
        dns_datacenters_client.list()

    Example - Data Centers::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.dns import DataCentersClient
        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        datacenters_client = DataCentersClient(device)

        # list datacenters
        dns_datacenters_client.list()

        # create datacenter
        datacenters_client.create(
            config={
                'name': 'my_datacenter'
            }
        )

        # show datacenter
        datacenters_client.show(name='my_datacenter')

        # update dns datacenter
        datacenters_client.update(
            name='my_offering_id',
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete datacenter
        datacenters_client.delete(name='my_datacenter')
"""

from .datacenters import DataCentersClient

__all__ = [
    'DataCentersClient'
]
