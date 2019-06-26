""" Test BIG-IP module """

# standard imports
import json
# project imports
from f5cloudsdk.cloud_services import ManagementClient
from f5cloudsdk.cloud_services.subscription import SubscriptionClient
from f5cloudsdk.exceptions import InputRequiredError
# unittest imports
from ...global_test_imports import pytest, Mock

# local test imports
from ...shared import constants
# packages to mock
REQ = constants.MOCK['requests']

USER = constants.USER
USER_PWD = constants.USER_PWD

LOGIN_RESPONSE = constants.F5_CLOUD_SERVICES['LOGIN_RESPONSE']


class TestSubscription(object):
    """Test Class: cloud_services.subscription module """

    @classmethod
    def setup_class(cls):
        """" Setup func """

    @classmethod
    def teardown_class(cls):
        """" Teardown func """

    def test_mgmt_client_no_sub_id(self, mocker):
        """Test: Subscription client should raise error if subscription id is not provided

        Assertions
        ----------
        - Exception InputRequiredError is raised
        """

        mocker.patch(REQ).return_value.json = Mock(return_value=LOGIN_RESPONSE)

        mgmt_client = ManagementClient(user=USER, password=USER_PWD)

        pytest.raises(InputRequiredError, SubscriptionClient, mgmt_client)

    def test_subscription_client_show(self, mocker):
        """Test: Subscription client show()

        Assertions
        ----------
        - Subscription client show() return value should be mocked response
        """

        show_response = {
            'subscription_id': 'foo',
            'account_id': 'foo'
        }
        mocker.patch(REQ).return_value.json = Mock(side_effect=[LOGIN_RESPONSE, show_response])

        mgmt_client = ManagementClient(user=USER, password=USER_PWD)
        sub_client = SubscriptionClient(mgmt_client, subscription_id='foo')

        response = sub_client.show()
        assert response == show_response

    def test_subscription_client_update(self, mocker):
        """Test: Subscription client update()

        Assertions
        ----------
        - Subscription client update() return value should be mocked response
        """

        update_response = {
            'configuration': {}
        }
        mocker.patch(REQ).return_value.json = Mock(side_effect=[LOGIN_RESPONSE, update_response])

        mgmt_client = ManagementClient(user=USER, password=USER_PWD)
        sub_client = SubscriptionClient(mgmt_client, subscription_id='foo')

        response = sub_client.update(config={'configuration': {}})
        assert response == update_response

    def test_subscription_client_update_config_file(self, mocker):
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
        sub_client = SubscriptionClient(mgmt_client, subscription_id='foo')

        response = sub_client.update(config_file='/foo.json')
        assert response == update_response
