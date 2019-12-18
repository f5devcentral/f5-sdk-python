""" Test fixtures """

from f5sdk.bigip import ManagementClient

from ...global_test_imports import pytest, Mock
from ...shared import constants

REQ = constants.MOCK['requests']

HOST = constants.HOST
USER = constants.USER
USER_PWD = constants.USER_PWD
TOKEN = constants.TOKEN
PORT = constants.PORT


@pytest.fixture
def mgmt_client(mocker):
    """ Test fixture: create mgmt client """
    token_response = {
        'token': {
            'token': TOKEN,
            'selfLink': 'https://localhost/mgmt/shared/authz/tokens/mytoken'
        }
    }
    mocker.patch(REQ).return_value.json = Mock(return_value=token_response)

    kwargs = {
        'user': USER,
        'password': USER_PWD,
        'port': PORT,
        'skip_ready_check': True
    }
    return ManagementClient(HOST, **kwargs)
