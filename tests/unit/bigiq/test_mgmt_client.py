""" Test BIG-IQ management client """

# project imports
from f5cloudsdk.bigiq import ManagementClient
# unittest imports
from ...global_test_imports import pytest, Mock

# local test imports
from ...shared import constants
# packages to mock
REQ = constants.MOCK['requests']

HOST = constants.HOST
USER = constants.USER
USER_PWD = constants.USER_PWD
TOKEN = constants.TOKEN

# define fixtures - disable pylint error when using fixture
# pylint: disable=redefined-outer-name
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


class TestMgmtClient(object):
    """Test Class: bigiq module """

    def test_mgmt_client(self, mgmt_client):
        """Test: Initialize mgmt client

        Assertions
        ----------
        - Device instance token should match 'TOKEN'
        """

        assert mgmt_client.token == TOKEN

    def test_get_info(self, mgmt_client, mocker):
        """Test: get_info function

        Assertions
        ----------
        - Device version should match 'version'
        """

        version = '7.0.0'
        response = {
            'entries': {
                'https://localhost/mgmt/tm/sys/version/0': {
                    'nestedStats': {
                        'entries': {
                            'Version': {
                                'description': version
                            }
                        }
                    }
                }
            }
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=response)

        device_info = mgmt_client.get_info()
        assert device_info['version'] == version
