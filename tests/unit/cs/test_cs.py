""" Test module """

from f5sdk.cs import ManagementClient
from f5sdk import constants as project_constants
from f5sdk.exceptions import InvalidAuthError, HTTPError

from ...global_test_imports import pytest, Mock
from ...shared import constants

REQ = constants.MOCK['requests']

USER = constants.USER
USER_PWD = constants.USER_PWD
TOKEN = constants.TOKEN
CUSTOM_API_ENDPOINT = constants.CUSTOM_API_ENDPOINT

LOGIN_RESPONSE = constants.F5_CS['LOGIN_RESPONSE']

AUTH_TOKEN_HEADER = project_constants.F5_CS['AUTH_TOKEN_HEADER']


class TestCloudServices(object):
    """Test Class: cs module """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_mgmt_client(mgmt_client):
        """Test: Initialize mgmt client

        Assertions
        ----------
        - Mgmt client access token should match 'TOKEN'
        """

        assert mgmt_client.access_token == TOKEN

    @staticmethod
    def test_mgmt_client_with_incorrect_creds(mocker):
        """Test: Initialize mgmt client with wrong credentials

        Assertions
        ----------
        - Mgmt client throws exception InvalidAuthError
        """
        mocker.patch(REQ).side_effect = HTTPError(constants.BAD_REQUEST_BODY)
        with pytest.raises(InvalidAuthError):
            ManagementClient(user=USER, password=USER_PWD)

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_request_auth_header(mgmt_client, mocker):
        """Test: make_request should insert auth header

        Assertions
        ----------
        - make_request should insert auth header: {'Authorization': 'Bearer token'}
        """

        mock = mocker.patch(REQ)

        mgmt_client.make_request('/')

        _, kwargs = mock.call_args
        assert 'Bearer' in kwargs['headers'][AUTH_TOKEN_HEADER]

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_default_api_endpoint(mgmt_client):
        """Test: Default API endpoint is used as expected

        Assertions
        ----------
        - Validates that CloudService has api_endpoint set to default value
        """
        # pylint: disable=protected-access

        assert mgmt_client._api_endpoint == project_constants.F5_CS['API_ENDPOINT']

    @staticmethod
    def test_api_endpoint_no_api_endpoint_value(mocker):
        """Test: Default API endpoint is used as expected
            when api_endpoint is provided with a None value

        Assertions
        ----------
        - Validates that CloudService has api_endpoint set to default value
        """
        # pylint: disable=protected-access

        mocker.patch(REQ).return_value.json = Mock(return_value=LOGIN_RESPONSE)

        mgmt_client = ManagementClient(user=USER, password=USER_PWD, api_endpoint=None)

        assert mgmt_client._api_endpoint == project_constants.F5_CS['API_ENDPOINT']

    @staticmethod
    def test_custom_api_endpoint(mocker):
        """Test: Custom API endpoint is used as expected
        Assertions
        ----------
        - Validates that CloudService api endpoint is set to custom value
        """
        # pylint: disable=protected-access

        mocker.patch(REQ).return_value.json = Mock(return_value=LOGIN_RESPONSE)

        mgmt_client = ManagementClient(
            user=USER, password=USER_PWD, api_endpoint=CUSTOM_API_ENDPOINT
        )

        assert mgmt_client._api_endpoint == constants.CUSTOM_API_ENDPOINT
