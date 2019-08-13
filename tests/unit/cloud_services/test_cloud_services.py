""" Test BIG-IP module """

# project imports
from f5cloudsdk.cloud_services import ManagementClient
from f5cloudsdk import constants as project_constants
# unittest imports
from ...global_test_imports import Mock

# local test imports
from ...shared import constants
# packages to mock
REQ = constants.MOCK['requests']

USER = constants.USER
USER_PWD = constants.USER_PWD
TOKEN = constants.TOKEN
CUSTOM_API_ENDPOINT = constants.CUSTOM_API_ENDPOINT

LOGIN_RESPONSE = constants.F5_CLOUD_SERVICES['LOGIN_RESPONSE']

AUTH_TOKEN_HEADER = project_constants.F5_CLOUD_SERVICES['AUTH_TOKEN_HEADER']


class TestCloudServices(object):
    """Test Class: cloud_services module """

    @classmethod
    def setup_class(cls):
        """" Setup func """

    @classmethod
    def teardown_class(cls):
        """" Teardown func """

    def test_mgmt_client(self, mocker):
        """Test: Initialize mgmt client

        Assertions
        ----------
        - Mgmt client access token should match 'TOKEN'
        """

        mocker.patch(REQ).return_value.json = Mock(return_value=LOGIN_RESPONSE)

        mgmt_client = ManagementClient(user=USER, password=USER_PWD)

        assert mgmt_client.access_token == TOKEN

    def test_make_request_auth_header(self, mocker):
        """Test: make_request should insert auth header

        Assertions
        ----------
        - make_request should insert auth header: {'Authorization': 'Bearer token'}
        """

        mock = mocker.patch(REQ)

        mgmt_client = ManagementClient(user=USER, password=USER_PWD)

        mgmt_client.make_request('/')

        _, kwargs = mock.call_args
        assert 'Bearer' in kwargs['headers'][AUTH_TOKEN_HEADER]

    def test_default_api_endpoint(self, mocker):
        """Test: Default API endpoint is used as expected

        Assertions
        ----------
        - Validates that CloudService has api_endpoint set to default value
        """
        show_response = {
            'subscription_id': 'foo',
            'account_id': 'foo'
        }

        mocker.patch(REQ).return_value.json = Mock(side_effect=[LOGIN_RESPONSE, show_response])

        mgmt_client = ManagementClient(user=USER, password=USER_PWD)

        assert mgmt_client._api_endpoint == project_constants.F5_CLOUD_SERVICES['API_ENDPOINT']

    def test_custom_api_endpoint(self, mocker):
        """Test: Custom API endpoint is used as expected
        Assertions
        ----------
        - Validates that CloudService api endpoint is set to custom value
        """
        show_response = {
            'subscription_id': 'foo',
            'account_id': 'foo'
        }

        mocker.patch(REQ).return_value.json = Mock(side_effect=[LOGIN_RESPONSE, show_response])

        mgmt_client = ManagementClient(user=USER, password=USER_PWD, api_endpoint=CUSTOM_API_ENDPOINT)
        assert mgmt_client._api_endpoint == constants.CUSTOM_API_ENDPOINT
