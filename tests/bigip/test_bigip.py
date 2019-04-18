""" Test BIG-IP module """
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError:
    # python 2.x support
    from mock import Mock, MagicMock, patch

from f5cloudsdk.bigip import ManagementClient

USER = 'admin'
USER_PWD = 'admin'
TOKEN = 'mytoken'

class MockRequestsResponse:
    """ Mock requests response object """
    def __init__(self, body):
        self.body = body

    def raise_for_status(self):
        """ Mock raise_for_status function """
        return True

    def json(self):
        """ Mock json function """
        return self.body

class TestBigIp(unittest.TestCase):
    """ Test case """

    def get_mgmt_client(self, **kwargs):
        """ Helper function to create mgmt client """
        use_token = kwargs.pop('use_token', False)
        if use_token:
            return ManagementClient('192.0.2.1', token=TOKEN)
        return ManagementClient('192.0.2.1', user=USER, password=USER_PWD)

    @patch('requests.patch')
    @patch('requests.post')
    def test_bigip_mgmt_client_basic(self, mock_post, mock_patch):
        """ Test BIG-IP mgmt client (basic) """
        def mock_post_response(*args, **kwargs):
            """ Mock post response """
            response = {
                'token': {
                    'token': TOKEN,
                    'selfLink': 'https://localhost/mgmt/shared/authz/tokens/mytoken'
                }
            }
            return MockRequestsResponse(response)
        mock_post.side_effect = mock_post_response

        device = self.get_mgmt_client()
        assert mock_post.called
        assert mock_patch.called
        assert device.user == USER
        assert device.password == USER_PWD
        assert device.token == TOKEN

    @patch('requests.request')
    def test_bigip_mgmt_client_get_info(self, mock_requests):
        """ Test BIG-IP mgmt client (get_info) """
        version = '14.1.0.0'
        def mock_requests_response(*args, **kwargs):
            """ Mock requests response """
            response = {
                'entries': {
                    'https://localhost/mgmt/tm/sys/version/0': {
                        'nestedStats': {
                            'entries': {
                                'Version': {
                                    'description': version
                                }
                            }
                        }
                    }
                }
            }
            return MockRequestsResponse(response)
        mock_requests.side_effect = mock_requests_response

        device = self.get_mgmt_client(use_token=True)
        device_info = device.get_info()
        assert mock_requests.called
        assert device_info['version'] == version
