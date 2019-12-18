"""Module for BIG-IQ license pool clients

    Example - Member Management::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing.pools import MemberManagementClient

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

    Example - RegKey Pools::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing.pools import RegKeyClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = RegKeyClient(device)

        # list license pools
        license_client.list()

        # create license pool
        license_client.create(
            config={
                'name': 'my_pool'
            }
        )

        # show license pool details
        license_client.show(name='my_pool_id')

        # update license pool
        license_client.update(
            name='my_pool_id',
            config={
                'name': 'my_pool'
            }
        )

        # delete license pool
        license_client.delete(name='my_pool_id')

    Example - RegKey Pool Offerings::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing.pools import RegKeyOfferingsClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        offerings_client = RegKeyOfferingsClient(
            device,
            pool_name='my_pool_name'
        )

        # list license pool offerings
        offerings_client.list()

        # create (add) offering to license pool
        offerings_client.create(
            config={
                'regkey': 'my_reg_key'
            }
        )

        # show license pool offering details
        offerings_client.show(name='my_offering_id')

        # update offering in license pool
        offerings_client.update(
            name='my_offering_id',
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete offering from license pool
        offerings_client.delete(name='my_offering_id')

    Example - RegKey Pool Offering Members::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing.pools import RegKeyOfferingMembersClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        members_client = RegKeyOfferingMembersClient(
            device,
            pool_name='my_pool_name',
            offering_name='my_offering_name'
        )

        # list license pool offering members
        members_client.list()

        # create (assign) member in license pool offering - managed or unmanaged
        members_client.create(
            config={
                'deviceAddress': 'x.x.x.x'
            }
        )

        # show license pool offering member details
        members_client.show(name='my_member_id')

        # update member in license pool offering
        members_client.update(
            name='my_member_id',
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete (revoke) member from license pool offering - managed or unmanaged
        members_client.delete(
            name='my_member_id',
            config={
                'id': 'my_member_id',
                'username': 'admin',
                'password': 'admin'
            }
        )

    Example - Utility Pools::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing.pools import UtilityClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = UtilityClient(device)

        # list license pools
        license_client.list()

        # create license pool
        license_client.create(
            config={
                'name': 'my_pool'
            }
        )

        # show license pool details
        license_client.show(name='my_pool_id')

        # update license pool
        license_client.update(
            name='my_pool_id',
            config={
                'name': 'my_pool'
            }
        )

        # delete license pool
        license_client.delete(name='my_pool_id')

    Example - Utility Pool Offerings::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing.pools import UtilityOfferingsClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        offerings_client = UtilityOfferingsClient(
            device,
            pool_name='my_pool_name'
        )

        # list license pool offerings
        offerings_client.list()

        # create (add) offering to license pool
        offerings_client.create(
            config={
                'regkey': 'my_reg_key'
            }
        )

        # show license pool offering details
        offerings_client.show(name='my_offering_id')

        # update offering in license pool
        offerings_client.update(
            name='my_offering_id',
            config={
                'regkey': 'my_reg_key'
            }
        )

        # delete offering from license pool
        offerings_client.delete(name='my_offering_id')

    Example - Utility Pool Offering Members::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing.pools import UtilityOfferingMembersClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        members_client = UtilityOfferingMembersClient(
            device,
            pool_name='my_pool_name',
            offering_name='my_offering_name'
        )

        # list license pool offering members
        members_client.list()

        # create (assign) member in license pool offering - managed or unmanaged
        members_client.create(
            config={
                'deviceAddress': 'x.x.x.x'
            }
        )

        # show license pool offering member details
        members_client.show(name='my_member_id')

        # update member in license pool offering
        members_client.update(
            name='my_member_id',
            config={
                'deviceAddress': 'x.x.x.x'
            }
        )

        # delete (revoke) member from license pool offering - managed or unmanaged
        members_client.delete(
            name='my_member_id',
            config={
                'id': 'my_member_id',
                'username': 'admin',
                'password': 'admin'
            }
        )
"""

from .member_management import MemberManagementClient
from .reg_key import RegKeyClient, RegKeyOfferingsClient, RegKeyOfferingMembersClient
from .utility import UtilityClient, UtilityOfferingsClient, UtilityOfferingMembersClient

__all__ = [
    'MemberManagementClient',
    'RegKeyClient',
    'RegKeyOfferingsClient',
    'RegKeyOfferingMembersClient',
    'UtilityClient',
    'UtilityOfferingsClient',
    'UtilityOfferingMembersClient'
]
