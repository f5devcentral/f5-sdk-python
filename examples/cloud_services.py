""" Get the F5 Cloud Services configuration

Notes
-----
Set local environment variables first
"""

# export F5_CS_EMAIL='user@example.com'
# export F5_CS_PWD='example_password'
# export F5_CS_SUBSCRIPTION_ID=''
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
        user=os.environ['F5_CS_EMAIL'], password=os.environ['F5_SDK_PWD'],
        api_endpoint=os.environ.get('F5_CS_API_ENDPOINT', None))  # optional
    # create subscription client
    subscription_client = SubscriptionClient(cs_client)

    # get subscription details
    return subscription_client.show(name=os.environ['F5_CS_SUBSCRIPTION_ID'])


if __name__ == '__main__':
    LOGGER.info(get_cs_config())
