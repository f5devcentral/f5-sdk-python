""" Test BIG-IP module """

## unittest imports ##
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError: # python 2.x support
    from mock import Mock, MagicMock, patch

## project imports ##
import socket
from f5cloudsdk import exceptions

## local test imports ##
from ...shared import utils
from . import utils as BigIpUtils

DFL_MGMT_PORT = 443

USER = 'admin'
USER_PWD = 'admin'
TOKEN = 'mytoken'

class TestBigIp(unittest.TestCase):
    """Test Class: bigip module """

    @patch('requests.request')
    def test_mgmt_client(self, mock_request):
        """Test: Initialize mgmt client

        Assertions
        ----------
        - Mocked request should be called
        - Device instance token should match 'TOKEN'
        """

        response = {
            'token': {
                'token': TOKEN,
                'selfLink': 'https://localhost/mgmt/shared/authz/tokens/mytoken'
            }
        }
        mock_request.side_effect = utils.create_mock_response(response)

        device = BigIpUtils.get_mgmt_client(user=USER, pwd=USER_PWD)
        assert mock_request.called
        assert device.token == TOKEN

    @patch('socket.socket')
    def test_port_discovery(self, mock_socket):
        """Test: Port discovery during mgmt client init

        Assertions
        ----------
        - Mocked socket should be called
        - Device port should match 'DFL_MGMT_PORT'
        - Device port should match 'DFL_MGMT_PORT' when OSError is raised
        """

        # basic - port should be set to default
        mock_socket.side_effect = utils.create_mock_socket()

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)
        assert mock_socket.called
        assert device.port == DFL_MGMT_PORT

        # raise OSError (connect refused case) - port should be set to default
        mock_socket.side_effect = utils.create_mock_socket(connect_raise=OSError)

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)
        assert device.port == DFL_MGMT_PORT

    @patch('socket.socket')
    def test_port_discovery_timeout(self, mock_socket):
        """Test: Port discovery during mgmt client init - when timeout occurrs

        Verify result when timeout for all DFL_ ports occurs

        Assertions
        ----------
        - Mocked socket should be called
        - DFL_MGMT_PORT should be returned
        """

        mock_socket.side_effect = utils.create_mock_socket(connect_raise=socket.timeout)

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)
        assert device.port == DFL_MGMT_PORT

    @patch('requests.request')
    def test_get_info(self, mock_requests):
        """Test: get_info

        Assertions
        ----------
        - Mocked request should be called
        - Device version should match 'version'
        """

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

    @patch('requests.request')
    def test_make_request_no_token(self, mock_requests):
        """Test: make_request with no device token

        Assertions
        ----------
        - AuthRequiredError exception should be raised
        """

        mock_requests.side_effect = utils.create_mock_response({})

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        device.token = None
        self.assertRaises(exceptions.AuthRequiredError, device.make_request, '/')

    @patch('requests.request')
    def test_make_request_bool(self, mock_requests):
        """Test: make_request with bool_response=True

        Assertions
        ----------
        - Mocked request should be called
        - make_request should return boolean (True)
        """

        mock_requests.side_effect = utils.create_mock_response({})

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        response = device.make_request('/', bool_response=True)
        assert mock_requests.called
        assert response
