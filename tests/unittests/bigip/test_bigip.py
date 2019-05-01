""" Test BIG-IP module """
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError:
    # python 2.x support
    from mock import Mock, MagicMock, patch

# SDK imports

# test imports
from ...shared import utils
from . import utils as BigIpUtils

USER = 'admin'
USER_PWD = 'admin'
TOKEN = 'mytoken'

class TestBigIp(unittest.TestCase):
    """ Test case """

    @patch('requests.patch')
    @patch('requests.post')
    def test_bigip_mgmt_client_basic(self, mock_post, mock_patch):
        """ Test BIG-IP mgmt client (basic) """
        response = {
            'token': {
                'token': TOKEN,
                'selfLink': 'https://localhost/mgmt/shared/authz/tokens/mytoken'
            }
        }
        mock_post.side_effect = utils.create_mock_response(response)

        device = BigIpUtils.get_mgmt_client(user=USER, pwd=USER_PWD)
        assert mock_post.called
        assert mock_patch.called
        assert device.user == USER
        assert device.password == USER_PWD
        assert device.token == TOKEN

    @patch('requests.request')
    def test_bigip_mgmt_client_get_info(self, mock_requests):
        """ Test BIG-IP mgmt client (get_info) """
        version = '14.1.0.0'
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
        mock_requests.side_effect = utils.create_mock_response(response)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        device_info = device.get_info()
        assert mock_requests.called
        assert device_info['version'] == version
