"""Module for BIG-IQ license pool member management

    Example - Basic::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing import PoolMemberManagementClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = PoolMemberManagementClient(device)

        # perform assignment - unreachable device
        license_client.create(
            config={
                'licensePoolName': 'my_pool',
                'command': 'assign',
                'address': 'x.x.x.x',
                'assignmentType': 'UNREACHABLE',
                'macAddress': 'FA:16:3E:1B:6D:32',
                'hypervisor': 'azure'
            }
        )

        # perform revoke - unreachable device
        license_client.create(
            config={
                'licensePoolName': 'my_pool',
                'command': 'revoke',
                'address': 'x.x.x.x',
                'assignmentType': 'UNREACHABLE',
                'macAddress': 'FA:16:3E:1B:6D:32'
            }
        )

        # list existing assign/revoke tasks
        license_client.list()
"""

from f5cloudsdk.base_clients import BaseFeatureClient

class PoolMemberManagementClient(BaseFeatureClient):
    """BIG-IQ pool member management client

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, client, **kwargs):
        """Initialization

        Parameters
        ----------
        client : object
            the management client object
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        None

        Returns
        -------
        None

        """

        super(PoolMemberManagementClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/mgmt/cm/device/tasks/licensing/pool/member-management'
        )
