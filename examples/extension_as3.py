""" Update BIG-IP L4-L7 configuration using AS3

Notes
-----
Set local environment variables first
"""

# export F5_SDK_HOST='192.0.2.10'
# export F5_SDK_USERNAME='admin'
# export F5_SDK_PWD='admin'
# export F5_SDK_AS3_DECL='./my_declaration.json'
# export F5_SDK_LOG_LEVEL='INFO'

import os

from f5sdk.bigip import ManagementClient
from f5sdk.bigip.extension import AS3Client
from f5sdk.logger import Logger

LOGGER = Logger(__name__).get_logger()


def run_example():
    """ Update AS3 configuration

    Notes
    -----
    Includes package installation, service check while
    maintaining idempotency
    """
    # create management client
    mgmt_client = ManagementClient(
        os.environ['F5_SDK_HOST'],
        user=os.environ['F5_SDK_USERNAME'],
        password=os.environ['F5_SDK_PWD'])

    # create extension client
    as3_client = AS3Client(mgmt_client)

    # Get installed package version info
    version_info = as3_client.package.is_installed()
    LOGGER.info(version_info['installed'])
    LOGGER.info(version_info['installed_version'])
    LOGGER.info(version_info['latest_version'])

    # install package
    if not version_info['installed']:
        as3_client.package.install()

    # ensure service is available
    as3_client.service.is_available()

    # configure AS3
    return as3_client.service.create(config_file=os.environ['F5_SDK_AS3_DECL'])


if __name__ == '__main__':
    LOGGER.info(run_example())
