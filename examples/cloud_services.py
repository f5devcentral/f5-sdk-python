""" Configure Cloud Services

Notes
-----
Set local environment variables first
"""

# export F5_SDK_USERNAME='admin'
# export F5_SDK_PWD='admin'
# export F5_SDK_CS_SUBSCRIPTION_ID=''
# export F5_SDK_CS_DECL='./my_declaration.json'
# export F5_SDK_LOG_LEVEL='DEBUG'

import os

from f5cloudsdk.cloud_services import ManagementClient
from f5cloudsdk.cloud_services.subscription import SubscriptionClient
from f5cloudsdk.logger import Logger

LOGGER = Logger(__name__).get_logger()

def update_cs_config():
    """ Update Cloud Services configuration """
    # create management client
    cs_client = ManagementClient(
        user=os.environ['F5_SDK_USERNAME'], password=os.environ['F5_SDK_PWD'])

    # create subscription client
    subscription_client = SubscriptionClient(
        cs_client, subscription_id=os.environ['F5_SDK_CS_SUBSCRIPTION_ID'])

    # configure subscription
    return subscription_client.update(config_file=os.environ['F5_SDK_CS_DECL'])

if __name__ == '__main__':
    LOGGER.info(update_cs_config())
