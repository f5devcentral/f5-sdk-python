""" Show the F5 Cloud Services Beacon declaration

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
from f5sdk.cs.beacon.declare import DeclareClient
from f5sdk.logger import Logger

LOGGER = Logger(__name__).get_logger()


def run_example():
    """ Show F5 Cloud Services Beacon Declaration (Applications, Monitors, etc.) """
    # create management client
    mgmt_client = ManagementClient(
        user=os.environ['F5_CS_USER'],
        password=os.environ['F5_CS_PWD']
    )

    # create declare client
    declare_client = DeclareClient(mgmt_client)

    # get subscription details
    return declare_client.create(config={'action': 'get'})


if __name__ == '__main__':
    LOGGER.info(json.dumps(run_example(), indent=4))
