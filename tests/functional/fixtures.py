""" Behave fixtures """

import os
import json
from test_imports import fixture  # pylint: disable=import-error

from f5sdk.bigip import ManagementClient
from f5sdk.bigip.extension import AS3Client, DOClient, TSClient, CFClient

from f5sdk.cs import ManagementClient as CSManagementClient
from f5sdk.cs.beacon.insights import InsightsClient
from f5sdk.cs.beacon.declare import DeclareClient

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


@fixture
def cs_management_client(context):
    """Return Cloud Services mgmt client"""
    context.cs_mgmt_client = CSManagementClient(user=os.environ['F5_CS_USER'],
                                                password=os.environ['F5_CS_PWD'])

    return context.cs_mgmt_client


@fixture
def cs_beacon_insights_client(context):
    """Return Cloud Services Beacon Insights client"""
    context.beacon_insights_client = InsightsClient(context.cs_mgmt_client)

    return context.beacon_insights_client


@fixture
def cs_beacon_declare_client(context):
    """Return Cloud Services Beacon Declare client"""
    context.beacon_declare_client = DeclareClient(context.cs_mgmt_client)

    return context.beacon_declare_client
