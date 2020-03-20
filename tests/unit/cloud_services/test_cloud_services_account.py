""" Test module """

from f5sdk.cloud_services.accounts import AccountClient

from ...global_test_imports import pytest, Mock
from ...shared import constants

REQUESTS = constants.MOCK['requests']


class TestAccounts(object):
    """Test Class: cloud_services.accounts module """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_accounts_show_user(mgmt_client, mocker):
        """Test: accounts.show_user()

        Assertions
        ----------
        - Return value should be mocked API response
        """

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={'foo': 'bar'})

        account_client = AccountClient(mgmt_client)
        assert account_client.show_user() == {'foo': 'bar'}
