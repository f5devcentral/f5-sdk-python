""" Test BIG-IP module """

## unittest imports ##
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch, call
except ImportError: # python 2.x support
    from mock import Mock, MagicMock, patch, call

## project imports ##
import base64
import socket
import tempfile
import shutil
import os
from paramiko import ssh_exception
from f5cloudsdk import exceptions

## local test imports ##
from ...shared import constants
from ...shared import mock_utils
from . import utils as BigIpUtils

DFL_MGMT_PORT = 443

USER = constants.USER
USER_PWD = constants.USER_PWD
TOKEN = constants.TOKEN

TOKEN_RESPONSE = {
    'token': {
        'token': TOKEN,
        'selfLink': 'https://localhost/mgmt/shared/authz/tokens/mytoken'
    }
}

class TestBigIp(unittest.TestCase):
    """Test Class: bigip module """
    def setUp(self):
        self.test_tmp_dir = tempfile.mkdtemp()
        self.private_key_file = os.path.join(self.test_tmp_dir, 'id_rsa')

        with open(os.path.join(os.path.dirname(__file__), 'sample_rsa_key')) as _f:
            _file = _f.read()
        with open(self.private_key_file, 'w') as _f:
            _f.write(base64.b64decode(_file).decode('utf-8'))

    def tearDown(self):
        shutil.rmtree(self.test_tmp_dir)

    @patch('requests.request')
    def test_mgmt_client(self, mock_request):
        """Test: Initialize mgmt client

        Assertions
        ----------
        - Mocked request should be called
        - Mock request instance 'json' should be called
        - Device instance token should match 'TOKEN'
        """

        mock_request_instance = mock_request.return_value
        mock_request_instance.json = Mock(return_value=TOKEN_RESPONSE)

        device = BigIpUtils.get_mgmt_client(user=USER, pwd=USER_PWD)

        mock_request_instance.json.assert_called()
        assert mock_request.called
        assert device.token == TOKEN

    @patch('paramiko.SSHClient')
    @patch('requests.request')
    def test_mgmt_client_key_auth(self, mock_request, mock_ssh_client):
        """Test: Initialize mgmt client using key-based auth

        Assertions
        ----------
        - Mocked ssh client should be called
        - Mock ssh client instance exec_command should start with 'tmsh modify'
        - Mocked request should be called
        - Device instance token should match 'TOKEN'
        """

        mock_request.side_effect = mock_utils.create_mock_response(TOKEN_RESPONSE)
        mock_ssh_client_instance = mock_utils.create_mock_ssh_client(
            mock_ssh_client,
            'auth user %s { description user shell bash }' % (USER)
        )

        device = BigIpUtils.get_mgmt_client(
            user=USER, pwd=USER_PWD, private_key_file=self.private_key_file)

        assert mock_ssh_client.called
        calls = [
            call(' list auth user %s' % (USER)),
            call('tmsh modify auth user %s password %s' % (USER, USER_PWD))
        ]
        mock_ssh_client_instance.exec_command.assert_has_calls(calls)
        assert mock_request.called
        assert device.token == TOKEN

    @patch('paramiko.SSHClient')
    @patch('requests.request')
    def test_mgmt_client_key_auth_bash(self, mock_request, mock_ssh_client):
        """Test: Initialize mgmt client using key-based auth - 'shell bash'

        'list auth user <user>' command response containing 'shell tmsh' means
        command should NOT start with 'tmsh'

        Assertions
        ----------
        - Mocked ssh client should be called
        - Mock ssh client instance exec_command should start with ' modify'
        - Mocked request should be called
        - Device instance token should match 'TOKEN'
        """

        mock_request.side_effect = mock_utils.create_mock_response(TOKEN_RESPONSE)
        mock_ssh_client_instance = mock_utils.create_mock_ssh_client(
            mock_ssh_client,
            'auth user %s { description user shell tmsh }' % (USER)
        )

        device = BigIpUtils.get_mgmt_client(
            user=USER, pwd=USER_PWD, private_key_file=self.private_key_file)

        assert mock_ssh_client.called
        calls = [
            call(' list auth user %s' % (USER)),
            call(' modify auth user %s password %s' % (USER, USER_PWD))
        ]
        mock_ssh_client_instance.exec_command.assert_has_calls(calls)
        assert mock_request.called
        assert device.token == TOKEN

    @patch('socket.socket')
    def test_port_discovery(self, mock_socket):
        """Test: Port discovery during mgmt client init

        Assertions
        ----------
        - Mocked socket should be called
        - Mock socket instance 'connect' should be called
        - Device port should match 'DFL_MGMT_PORT'
        - Device port should match 'DFL_MGMT_PORT' when OSError is raised
        """

        mock_socket_instance = mock_utils.create_mock_socket(mock_socket)

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)

        assert mock_socket.called
        mock_socket_instance.connect.assert_called()
        assert device.port == DFL_MGMT_PORT

        # raise OSError (connect refused case) - port should be set to default
        mock_socket_instance = mock_utils.create_mock_socket(mock_socket, connect_raise=OSError)

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)

        assert device.port == DFL_MGMT_PORT

    @patch('socket.socket')
    def test_port_discovery_timeout(self, mock_socket):
        """Test: Port discovery during mgmt client init - when timeout occurrs

        Verify result when timeout for all DFL_ ports occurs

        Assertions
        ----------
        - Mocked socket should be called
        - Mock socket instance 'connect' should be called
        - DFL_MGMT_PORT should be returned
        """

        mock_socket_instance = mock_utils.create_mock_socket(
            mock_socket, connect_raise=socket.timeout)

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)

        assert mock_socket.called
        mock_socket_instance.connect.assert_called()
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
        mock_requests.side_effect = mock_utils.create_mock_response(response)

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

        mock_requests.side_effect = mock_utils.create_mock_response({})

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

        mock_requests.side_effect = mock_utils.create_mock_response({})

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        response = device.make_request('/', bool_response=True)
        assert mock_requests.called
        assert response

    @patch('paramiko.SSHClient')
    @patch('requests.request')
    def test_make_ssh_request_stderr(self, mock_request, mock_ssh_client):
        """Test: make_ssh_request - stderr response should raise exception

        Assertions
        ----------
        - SSHCommandStdError exception should be raised
        """

        mock_request.side_effect = mock_utils.create_mock_response(TOKEN_RESPONSE)
        mock_ssh_client_instance = mock_utils.create_mock_ssh_client(
            mock_ssh_client, '', stderr='error')

        device = BigIpUtils.get_mgmt_client(user=USER, pwd=USER_PWD)

        self.assertRaises(exceptions.SSHCommandStdError, device.make_ssh_request, 'command')
        mock_ssh_client_instance.connect.assert_called()

    @patch('paramiko.SSHClient')
    @patch('requests.request')
    def test_make_ssh_request_connect_error(self, mock_request, mock_ssh_client):
        """Test: make_ssh_request - connect exception should raise exception

        Assertions
        ----------
        - SSHException should be raised
        """

        mock_request.side_effect = mock_utils.create_mock_response(TOKEN_RESPONSE)
        mock_ssh_client_instance = mock_utils.create_mock_ssh_client(
            mock_ssh_client, 'foo', connect_raise=ssh_exception.SSHException)

        device = BigIpUtils.get_mgmt_client(user=USER, pwd=USER_PWD)

        self.assertRaises(ssh_exception.SSHException, device.make_ssh_request, 'command')
        mock_ssh_client_instance.connect.assert_called()
