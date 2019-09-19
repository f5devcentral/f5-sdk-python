""" Test fixtures """

from f5cloudsdk.cloud_services import ManagementClient

from ...global_test_imports import pytest, Mock
from ...shared import constants

REQ = constants.MOCK['requests']

HOST = constants.HOST
USER = constants.USER
USER_PWD = constants.USER_PWD

LOGIN_RESPONSE = constants.F5_CLOUD_SERVICES['LOGIN_RESPONSE']


@pytest.fixture
def mgmt_client(mocker):
    """ Test fixture: create mgmt client """
    mocker.patch(REQ).return_value.json = Mock(return_value=LOGIN_RESPONSE)

    return ManagementClient(user=USER, password=USER_PWD)
