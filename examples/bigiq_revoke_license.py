""" Revoke licensed BIG-IP (unreachable) from BIG-IQ license pool

Notes
-----
Set local environment variables first
"""

# export F5_SDK_HOST='192.0.2.10'
# export F5_SDK_USERNAME='admin'
# export F5_SDK_PWD='admin'
# export F5_SDK_BIGIP_TO_REVOKE='192.0.2.100'
# export F5_SDK_BIGIQ_LICENSE_POOL='my_pool'
# export F5_SDK_LOG_LEVEL='DEBUG'

import os

from f5cloudsdk.bigiq import ManagementClient
from f5cloudsdk.bigiq.licensing import AssignmentClient
from f5cloudsdk.bigiq.licensing import MemberManagementPoolClient
from f5cloudsdk.logger import Logger

LOGGER = Logger(__name__).get_logger()

def revoke_license(address, pool):
    """ Revoke license"""

    # create management client
    mgmt_client = ManagementClient(
        os.environ['F5_SDK_HOST'],
        user=os.environ['F5_SDK_USERNAME'],
        password=os.environ['F5_SDK_PWD'])

    # create assignment client, member management client
    assignment_client = AssignmentClient(mgmt_client)
    member_mgmt_client = MemberManagementPoolClient(mgmt_client)

    # list assignments
    assignments = assignment_client.list()

    # get address assignment - there should only be one
    assignments = assignments['items']
    assignment = [i for i in assignments if assignments['deviceAddress'] == address][0]

    if not assignment:
        raise Exception('Unable to locate assignment from BIG-IQ assignments')

    # perform revoke - unreachable device
    return member_mgmt_client.create(
        config={
            'licensePoolName': pool,
            'command': 'revoke',
            'address': assignment['deviceAddress'],
            'assignmentType': 'UNREACHABLE',
            'macAddress': assignment['macAddress']
        }
    )

if __name__ == '__main__':
    RESPONSE = revoke_license(
        os.environ['F5_SDK_BIGIP_TO_REVOKE'],
        os.environ['F5_SDK_BIGIQ_LICENSE_POOL']
    )
    LOGGER.info('Response: %s', RESPONSE)
