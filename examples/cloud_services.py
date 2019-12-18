""" Get the F5 Cloud Services configuration

Notes
-----
Set local environment variables first
"""

# export F5_SDK_USERNAME='admin'
# export F5_SDK_PWD='admin'
# export F5_SDK_CS_SUBSCRIPTION_ID=''
# export F5_SDK_LOG_LEVEL='DEBUG'

import os

from f5sdk.cloud_services import ManagementClient
from f5sdk.cloud_services.subscriptions import SubscriptionClient
from f5sdk.logger import Logger

LOGGER = Logger(__name__).get_logger()


def get_cs_config():
    """ Get Cloud Services configuration """
    # create management client
    cs_client = ManagementClient(
        user=os.environ['F5_SDK_USERNAME'], password=os.environ['F5_SDK_PWD'])

    # create subscription client
    subscription_client = SubscriptionClient(cs_client)

    # get subscription details
    return subscription_client.show(name=os.environ['F5_SDK_CS_SUBSCRIPTION_ID'])


if __name__ == '__main__':
    LOGGER.info(get_cs_config())
