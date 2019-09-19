""" Test module """


import json

from f5cloudsdk.cloud_services import ManagementClient
from f5cloudsdk.cloud_services.subscriptions import SubscriptionClient

from ...global_test_imports import pytest, Mock
from ...shared import constants
from .. import utils

REQ = constants.MOCK['requests']

USER = constants.USER
USER_PWD = constants.USER_PWD
LOGIN_RESPONSE = constants.F5_CLOUD_SERVICES['LOGIN_RESPONSE']


class TestSubscription(object):
    """Test Class: cloud_services.subscriptions module """

    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = SubscriptionClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker,
            methods=['list', 'create', 'show', 'update', 'delete']
        )

    @pytest.mark.usefixtures("mgmt_client")
    def test_subscription_client_update_config_file(self, mgmt_client, mocker):
        """Test: Subscription client update() - with config_file

        Assertions
        ----------
        - Subscription client update() return value should be mocked response
        """

        update_response = {
            'configuration': {}
        }
        mocker.patch(REQ).return_value.json = Mock(side_effect=[LOGIN_RESPONSE, update_response])
        mocker.patch('f5cloudsdk.utils.file_utils.open', mocker.mock_open(read_data=json.dumps({})))

        mgmt_client = ManagementClient(user=USER, password=USER_PWD)
        sub_client = SubscriptionClient(mgmt_client)

        assert sub_client.update(name='foo', config_file='/foo.json') == update_response
