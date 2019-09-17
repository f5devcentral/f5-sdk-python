"""Module for BIG-IQ license pool member management

    Example - Basic::

        from f5cloudsdk.bigiq import ManagementClient
        from f5cloudsdk.bigiq.licensing.pool import MemberManagementClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = MemberManagementClient(device)

        # list existing assign/revoke tasks
        license_client.list()

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
"""

from f5cloudsdk.base_clients import BaseFeatureClient

class MemberManagementClient(BaseFeatureClient):
    """BIG-IQ license pool member management client

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

        super(MemberManagementClient, self).__init__(
            client,
            logger_name=__name__,
            uri='/mgmt/cm/device/tasks/licensing/pool/member-management'
        )

    def show(self, **kwargs):
        """ Method not allowed (action:skip_documentation) """

        raise self._exceptions['MethodNotAllowed']

    def update(self, **kwargs):
        """ Method not allowed (action:skip_documentation) """

        raise self._exceptions['MethodNotAllowed']

    def delete(self, **kwargs):
        """ Method not allowed (action:skip_documentation) """

        raise self._exceptions['MethodNotAllowed']
