""" Test BIG-IQ licensing pool member management """

from f5cloudsdk.bigiq.licensing.pool import UtilityClient

from ....global_test_imports import pytest, Mock
from ....shared import constants

REQ = constants.MOCK['requests']


class TestPoolUtilityClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_list(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        for method in ['list', 'create', 'show', 'update', 'delete']:
            mock_response = {
                'items': [
                    {
                        'foo': 'bar'
                    }
                ]
            }
            mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)
            client = UtilityClient(mgmt_client)

            kwargs = {}
            if method in ['show', 'update', 'delete']:
                kwargs['name'] = 'foo'
            if method in ['create', 'update']:
                kwargs['config'] = {'foo': 'bar'}
            assert getattr(client, method)(**kwargs) == mock_response
