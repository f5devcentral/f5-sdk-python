""" Test module """


import json

from f5sdk.cs.subscriptions import SubscriptionClient

from ...global_test_imports import pytest, Mock
from ...shared import constants
from .. import utils

REQUESTS = constants.MOCK['requests']


class TestSubscription(object):
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
            SubscriptionClient(mgmt_client),
            mocker=mocker,
            methods=['list', 'create', 'show', 'update', 'delete']
        )

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_subscription_client_update_config_file(mgmt_client, mocker):
        """Test: Subscription client update() - with config_file

        Assertions
        ----------
        - Subscription client update() return value should be mocked response
        """

        mocker.patch('f5sdk.utils.file_utils.open', mocker.mock_open(read_data=json.dumps({})))
        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        subscription_client = SubscriptionClient(mgmt_client)
        assert subscription_client.update(name='foo', config_file='/foo.json') == {}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_subscription_client_list_query_parameters(mgmt_client, mocker):
        """Test: list() method with query parameters

        Assertions
        ----------
        - Return value should be mock API response
        """

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={})

        subscription_client = SubscriptionClient(mgmt_client)
        assert subscription_client.list(query_parameters={'account_id': ''}) == {}
