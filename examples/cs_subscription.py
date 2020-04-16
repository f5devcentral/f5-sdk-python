""" Show the F5 Cloud Services subscription declaration

Notes
-----
Set local environment variables first
"""

# export F5_CS_USER='user@example.com'
# export F5_CS_PWD='example_password'
# export F5_SDK_LOG_LEVEL='INFO'

import os
import json

from f5sdk.cs import ManagementClient
from f5sdk.cs.accounts import AccountClient
from f5sdk.cs.subscriptions import SubscriptionClient
from f5sdk.logger import Logger

LOGGER = Logger(__name__).get_logger()


def run_example():
    """ Get Cloud Services configuration """
    # create management client
    mgmt_client = ManagementClient(
        user=os.environ['F5_CS_USER'],
        password=os.environ['F5_CS_PWD']
    )

    # create account/subscription client
    account_client = AccountClient(mgmt_client)
    subscription_client = SubscriptionClient(mgmt_client)

    # discover account/subscription ID
    account_id = account_client.show_user()['primary_account_id']
    subscription_id = subscription_client.list(
        query_parameters={
            'account_id': account_id
        }
    )['subscriptions'][0]['subscription_id']

    # get subscription details
    return subscription_client.show(name=subscription_id)


if __name__ == '__main__':
    LOGGER.info(json.dumps(run_example(), indent=4))
