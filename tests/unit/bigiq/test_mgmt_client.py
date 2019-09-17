""" Test BIG-IQ management client """

from ...global_test_imports import pytest, Mock
from ...shared import constants

REQ = constants.MOCK['requests']
TOKEN = constants.TOKEN


class TestMgmtClient(object):
    """Test Class: bigiq module """

    @pytest.mark.usefixtures("mgmt_client")
    def test_mgmt_client(self, mgmt_client):
        """Test: Initialize mgmt client

        Assertions
        ----------
        - Device instance token should match 'TOKEN'
        """

        assert mgmt_client.token == TOKEN

    @pytest.mark.usefixtures("mgmt_client")
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
