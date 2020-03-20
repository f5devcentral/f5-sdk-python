""" Test BIG-IQ licensing pool member management """

from f5sdk.bigiq.licensing.pools import MemberManagementClient

from ....global_test_imports import pytest, Mock, PropertyMock
from ....shared import constants
from ... import utils

REQ = constants.MOCK['requests']


class TestPoolMemberManagementClient(object):
    """Test"""

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = MemberManagementClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker,
            methods=['list', 'create']
        )


    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_create_async(mgmt_client, mocker):
        """Test: create function - async response

        Assertions
        ----------
        - Create response should match mocked return value (2nd response)
        """

        mock_responses = [
            {
                'status': 'RUNNING',
                'selfLink': 'https://localhost/foo/bar'
            },
            {
                'status': 'FINISHED'
            }
        ]
        mock_request = mocker.patch(REQ).return_value
        mock_request.json = Mock(side_effect=mock_responses)
        type(mock_request).status_code = PropertyMock(side_effect=[202, 200])

        client = MemberManagementClient(mgmt_client)
        response = client.create(config={'foo': 'bar'})
        assert response == mock_responses[1]
