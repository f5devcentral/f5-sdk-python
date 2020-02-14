""" Behave fixtures """

import json
from test_imports import fixture # pylint: disable=import-error
from f5sdk.bigip import ManagementClient
from f5sdk.bigip.extension import ExtensionClient

DEPLOYMENT_FILE = "./deployment_info.json"

@fixture
def bigip_management_client(context):
    """Return BIG-IP management client"""

    with open(DEPLOYMENT_FILE) as json_file:
        deployment_info = json.load(json_file)
        instance_info = deployment_info['instances'][0]

        context.mgmt_client = ManagementClient(instance_info['mgmt_address'],
                                               user=instance_info['admin_username'],
                                               password=instance_info['admin_password']
                                              )
    return context.mgmt_client

@fixture
def bigip_extension_client(context, **kwargs):
    """Return BIG-IP extension client"""

    component = kwargs.pop('component', None)

    context.extension_client = ExtensionClient(context.mgmt_client, component)
