""" Test fixtures """

from f5sdk.bigiq import ManagementClient

from ...global_test_imports import pytest, Mock
from ...shared import constants

REQ = constants.MOCK['requests']

HOST = constants.HOST
USER = constants.USER
USER_PWD = constants.USER_PWD
TOKEN = constants.TOKEN


@pytest.fixture
def mgmt_client(mocker):
    """ Test fixture: create mgmt client """
    token_response = {
        'token': {
            'token': TOKEN,
            'timeout': 300,
            'selfLink': 'https://localhost/mgmt/shared/authz/tokens/mytoken'
        }
    }
    mocker.patch(REQ).return_value.json = Mock(return_value=token_response)
    return ManagementClient(HOST, user=USER, password=USER_PWD)
