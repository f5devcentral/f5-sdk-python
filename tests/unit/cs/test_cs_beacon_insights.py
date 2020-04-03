""" Test module """


import json

from f5sdk.cs.beacon.insights import InsightsClient

from ...global_test_imports import pytest, Mock
from ...shared import constants
from .. import utils

REQUESTS = constants.MOCK['requests']


class TestBeaconInsights(object):
    """Test Class: cs.subscriptions module """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        utils.validate_crud_operations(
            InsightsClient(mgmt_client),
            mocker=mocker,
            methods=['list', 'create', 'show', 'delete']
        )

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_insights_client_list_query_parameters(mgmt_client, mocker):
        """Test: list() method with query parameters

        Assertions
        ----------
        - Return value should be mock API response
        """

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        insights_client = InsightsClient(mgmt_client)
        assert insights_client.list(query_parameters={'pageSize': '5'}) == {}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_insights_client_create_config_file(mgmt_client, mocker):
        """Test: Beacon Insights client create() - with config_file

        Assertions
        ----------
        - Beacon Insights client create() return value should be mocked response
        """

        mocker.patch('f5sdk.utils.file_utils.open', mocker.mock_open(read_data=json.dumps({})))
        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        insights_client = InsightsClient(mgmt_client)
        assert insights_client.create(config_file='/foo.json') == {}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_insights_client_update_config_file(mgmt_client, mocker):
        """Test: Beacon Insights client update() - with config_file

        Assertions
        ----------
        - Beacon Insights client create() return value should be mocked response
        """

        mocker.patch('f5sdk.utils.file_utils.open', mocker.mock_open(read_data=json.dumps({})))
        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        insights_client = InsightsClient(mgmt_client)
        assert insights_client.create(config_file='/foo.json') == {}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_insights_client_delete_with_title(mgmt_client, mocker):
        """Test: Beacon Insights client update() - with config_file

        Assertions
        ----------
        - Beacon Insights client create() return value should be mocked response
        """

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        insights_client = InsightsClient(mgmt_client)
        assert insights_client.delete(name='blah') == {}
