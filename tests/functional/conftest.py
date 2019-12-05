"""conftest.py for functional tests."""

import os
import json
import pytest

from f5cloudsdk.bigip import ManagementClient


@pytest.fixture(scope="session")
def management_client():
    """Return management client"""
    with open(os.path.join(os.path.dirname(__file__), \
                "../deployment/deployment_info.json")) as json_file:
        json_data = json.load(json_file)
        for data in json_data['instances']:
            os.environ['mgmt_address'] = data['mgmt_address']
            os.environ['admin_username'] = data['admin_username']
            os.environ['admin_password'] = data['admin_password']
    # Connect to BIG-IP
    mgmt_client = ManagementClient(
        os.environ.get('mgmt_address'),
        user=os.environ.get('admin_username'),
        password=os.environ.get('admin_password'))
    return mgmt_client
