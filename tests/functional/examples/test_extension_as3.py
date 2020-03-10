""" Functional Test Examples File """

import os
import json
import pytest

from f5sdk.bigip import ManagementClient
from f5sdk.exceptions import FileLoadError
from examples.extension_as3 import update_as3_config


@pytest.fixture
def instance_info():
    """ Get instances info from deployment_info.json """
    with open('./deployment_info.json') as json_file:
        deployment_info = json.load(json_file)
        deployment_info = [i for i in deployment_info['instances'] if i['primary']][0]

    return deployment_info


# pylint: disable=redefined-outer-name
def test_extension_as3_example_file(instance_info):
    """ Test update_as3_config() method """
    if not os.path.exists(os.path.join(os.getcwd(), './examples/extension_as3.py')):
        raise FileLoadError('Test example file extension_as3.py not exists')

    os.environ['F5_SDK_HOST'] = instance_info['mgmt_address']
    os.environ['F5_SDK_USERNAME'] = instance_info['admin_username']
    os.environ['F5_SDK_PWD'] = instance_info['admin_password']
    os.environ['F5_SDK_AS3_DECL'] = os.path.join(os.path.dirname(__file__), 'as3_declaration.json')

    # run AS3 example
    update_as3_config()

    # create management client
    mgmt_client = ManagementClient(
        os.environ['F5_SDK_HOST'],
        user=os.environ['F5_SDK_USERNAME'],
        password=os.environ['F5_SDK_PWD'])

    # validate AS3 example created a virtual server
    virtual_servers = mgmt_client.make_request('/mgmt/tm/ltm/virtual')['items']
    match = [i for i in virtual_servers
             if i['destination'].split('/')[-1].split(':')[0] == '10.0.1.20'
            ]
    assert len(match) == 1, virtual_servers
