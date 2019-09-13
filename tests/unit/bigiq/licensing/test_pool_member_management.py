""" Test BIG-IQ licensing pool member management """

from f5cloudsdk.bigiq.licensing import PoolMemberManagementClient

from ....global_test_imports import pytest, Mock
from ....shared import constants

REQ = constants.MOCK['requests']


class TestPoolMemberManagementClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_list(self, mgmt_client, mocker):
        """Test: list function

        Assertions
        ----------
        - List response should match mocked return value
        """

        mock_response = {
            'items': []
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        client = PoolMemberManagementClient(mgmt_client)
        assert client.list() == mock_response

    @pytest.mark.usefixtures("mgmt_client")
    def test_create(self, mgmt_client, mocker):
        """Test: list function

        Assertions
        ----------
        - List response should match mocked return value
        """

        mock_response = {
            'items': []
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        client = PoolMemberManagementClient(mgmt_client)
        assert client.create(config={'foo': 'bar'}) == mock_response
