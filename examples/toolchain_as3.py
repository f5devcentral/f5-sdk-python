""" Update BIG-IP L4-L7 configuration using AS3

Notes
-----
Set local environment variables first
"""

# export F5_SDK_HOST='192.0.2.10'
# export F5_SDK_USERNAME='admin'
# export F5_SDK_PWD='admin'
# export F5_SDK_AS3_DECL='./my_declaration.json'
# export F5_SDK_LOG_LEVEL='DEBUG'

import os

from f5cloudsdk.bigip import ManagementClient
from f5cloudsdk.bigip.toolchain import ToolChainClient
from f5cloudsdk.logger import Logger

LOGGER = Logger(__name__).get_logger()

def update_as3_config():
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

    # create toolchain client
    as3_client = ToolChainClient(mgmt_client, 'as3')

    # Get installed package version info
    version_info = as3_client.package.is_installed()
    LOGGER.info(version_info['installed'])
    LOGGER.info(version_info['installed_version'])
    LOGGER.info(version_info['latest_version'])

    # install package
    if not as3_client.package.is_installed()['is_installed']:
        as3_client.package.install()

    # ensure service is available
    as3_client.service.is_available()

    # configure AS3
    return as3_client.service.create(config_file=os.environ['F5_SDK_AS3_DECL'])

if __name__ == '__main__':
    LOGGER.info(update_as3_config())
