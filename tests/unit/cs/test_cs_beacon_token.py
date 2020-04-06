""" Test module """


import json

from f5sdk.cs.beacon.token import TokenClient

from ...global_test_imports import pytest, Mock
from ...shared import constants
from .. import utils

REQUESTS = constants.MOCK['requests']


class TestBeaconToken(object):
    """Test Class: cs.beacon.token module """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        utils.validate_crud_operations(
            TokenClient(mgmt_client),
            mocker=mocker,
            methods=['list', 'create', 'show', 'delete']
        )

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_token_client_list_query_parameters(mgmt_client, mocker):
        """Test: list() method with query parameters

        Assertions
        ----------
        - Return value should be mock API response
        """

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        token_client = TokenClient(mgmt_client)
        assert token_client.list(query_parameters={'pageSize': '5'}) == {}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_token_client_create_config_file(mgmt_client, mocker):
        """Test: Beacon Token client create() - with config_file

        Assertions
        ----------
        - Beacon Token client create() return value should be mocked response
        """

        mocker.patch('f5sdk.utils.file_utils.open', mocker.mock_open(read_data=json.dumps({})))
        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        token_client = TokenClient(mgmt_client)
        assert token_client.create(config_file='/foo.json') == {}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_token_client_delete_with_name(mgmt_client, mocker):
        """Test: Beacon Token client update() - with config_file

        Assertions
        ----------
        - Beacon Token client create() return value should be mocked response
        """

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        token_client = TokenClient(mgmt_client)
        assert token_client.delete(name='blah') == {}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_token_client_show_with_name(mgmt_client, mocker):
        """Test: Beacon Token client show()

        Assertions
        ----------
        - Beacon Token client show() return value should be mocked response
        """

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={'foo': 'bar'})

        token_client = TokenClient(mgmt_client)
        assert token_client.delete(name='blah') == {'foo': 'bar'}
