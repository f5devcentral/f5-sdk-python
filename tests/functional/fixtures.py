""" Behave fixtures """

import json
from test_imports import fixture # pylint: disable=import-error
from f5sdk.bigip import ManagementClient
from f5sdk.bigip.extension import AS3Client, DOClient, TSClient, CFClient

DEPLOYMENT_FILE = "./deployment_info.json"

@fixture
def bigip_management_client(context):
    """Return BIG-IP management client"""

    with open(DEPLOYMENT_FILE) as json_file:
        deployment_info = json.load(json_file)

        # get instance info on active (primary) device
        instance_info = [i for i in deployment_info['instances'] if i['primary']][0]

        context.mgmt_client = ManagementClient(instance_info['mgmt_address'],
                                               user=instance_info['admin_username'],
                                               password=instance_info['admin_password']
                                              )

        context.deployment_info = deployment_info

    return context.mgmt_client

@fixture
def bigip_extension_client(context, **kwargs):
    """Return BIG-IP extension client"""

    component = kwargs.pop('component', None)

    # extension client factory
    if component == 'as3':
        context.extension_client = AS3Client(context.mgmt_client)
    elif component == 'do':
        context.extension_client = DOClient(context.mgmt_client)
    elif component == 'ts':
        context.extension_client = TSClient(context.mgmt_client)
    elif component == 'cf':
        context.extension_client = CFClient(context.mgmt_client)
    else:
        raise Exception('Unknown component: {}'.format(component))

    return context.extension_client
