"""conftest.py for functional tests."""

import os
import json
import pytest

from f5cloudsdk.bigip import ManagementClient


@pytest.fixture(scope="session")
def management_client():
    """Return management client"""
    with open(os.path.join(os.path.dirname(__file__),
                           "../deployment/deployment_info.json")) as json_file:
        json_data = json.load(json_file)
        mgmt_client = ManagementClient(json_data['instances'][0]['mgmt_address'],
                                       user=json_data['instances'][0]['admin_username'],
                                       password=json_data['instances'][0]['admin_password'])
        return mgmt_client
