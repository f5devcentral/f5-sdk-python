""" Test BIG-IP module """

import base64
import socket
import os
from paramiko import ssh_exception
from f5sdk import exceptions
from f5sdk import constants as project_constants

from ...global_test_imports import pytest, Mock, PropertyMock, call

from ...shared import constants
from ...shared import mock_utils
from . import utils as BigIpUtils

REQ = constants.MOCK['requests']

HOST = constants.HOST
USER = constants.USER
USER_PWD = constants.USER_PWD
TOKEN = constants.TOKEN
DFL_MGMT_PORT = constants.PORT

TOKEN_RESPONSE = {
    'token': {
        'token': TOKEN,
        'selfLink': 'https://localhost/mgmt/shared/authz/tokens/mytoken'
    }
}


class TestBigIp(object):
    """Test Class: bigip module """

    @classmethod
    def setup_class(cls):
        """" Setup func """

        with open(os.path.join(os.path.dirname(__file__), 'sample_rsa_key')) as _f:
            _file = _f.read()

        cls.private_key = base64.b64decode(_file).decode('utf-8')

    @classmethod
    def teardown_class(cls):
        """" Teardown func """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_mgmt_client(mgmt_client):
        """Test: Initialize mgmt client

        Assertions
        ----------
        - Device instance token should match 'TOKEN'
        """

        assert mgmt_client.token == TOKEN

    def test_mgmt_client_key_auth(self, mocker):
        """Test: Initialize mgmt client using key-based auth

        Assertions
        ----------
        - Mock ssh client instance exec_command should start with 'tmsh modify'
        - Device instance token should match 'TOKEN'
        """

        mocker.patch(REQ).return_value.json = Mock(return_value=TOKEN_RESPONSE)
        mock_ssh_client_instance = mock_utils.create_ssh_client(
            mocker.patch('paramiko.SSHClient'),
            'auth user %s { description user shell bash }' % (USER)
        )
        mocker.patch('paramiko.rsakey.open', mocker.mock_open(read_data=self.private_key))
        mocker.patch('paramiko.pkey.open', mocker.mock_open(read_data=self.private_key))

        device = BigIpUtils.get_mgmt_client(
            user=USER, pwd=USER_PWD, private_key_file='foo')

        calls = [
            call(' list auth user %s' % (USER)),
            call('tmsh modify auth user %s password %s' % (USER, USER_PWD))
        ]
        mock_ssh_client_instance.exec_command.assert_has_calls(calls)
        assert device.token == TOKEN

    def test_mgmt_client_key_auth_bash(self, mocker):
        """Test: Initialize mgmt client using key-based auth - 'shell bash'

        'list auth user <user>' command response containing 'shell tmsh' means
        command should NOT start with 'tmsh'

        Assertions
        ----------
        - Mock ssh client instance exec_command should start with ' modify'
        - Device instance token should match 'TOKEN'
        """

        mocker.patch(REQ).return_value.json = Mock(return_value=TOKEN_RESPONSE)
        mock_ssh_client_instance = mock_utils.create_ssh_client(
            mocker.patch('paramiko.SSHClient'),
            'auth user %s { description user shell tmsh }' % (USER)
        )
        mocker.patch('paramiko.rsakey.open', mocker.mock_open(read_data=self.private_key))
        mocker.patch('paramiko.pkey.open', mocker.mock_open(read_data=self.private_key))

        device = BigIpUtils.get_mgmt_client(
            user=USER, pwd=USER_PWD, private_key_file='foo')

        calls = [
            call(' list auth user %s' % (USER)),
            call(' modify auth user %s password %s' % (USER, USER_PWD))
        ]
        mock_ssh_client_instance.exec_command.assert_has_calls(calls)
        assert device.token == TOKEN

    @staticmethod
    def test_port_discovery(mocker):
        """Test: Port discovery during mgmt client init

        Assertions
        ----------
        - Mock socket instance 'connect' should be called
        - Device port should match 'DFL_MGMT_PORT'
        - Device port should match 'DFL_MGMT_PORT' when OSError is raised
        """

        mock_socket = mocker.patch('socket.socket').return_value

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)

        mock_socket.connect.assert_called()
        assert device.port == DFL_MGMT_PORT

        # raise OSError (connect refused case) - port should be set to default
        mock_socket = mocker.patch('socket.socket').return_value.connect.side_effect = OSError

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)

        assert device.port == DFL_MGMT_PORT

    @staticmethod
    def test_port_discovery_timeout(mocker):
        """Test: Port discovery during mgmt client init - when timeout occurrs

        Verify result when timeout for all DFL_ ports occurs

        Assertions
        ----------
        - Mock socket instance 'connect' should be called
        - DFL_MGMT_PORT should be returned
        """

        mock_socket = mocker.patch('socket.socket').return_value
        mock_socket.connect.side_effect = socket.timeout

        device = BigIpUtils.get_mgmt_client(token=TOKEN, port=None)

        mock_socket.connect.assert_called()
        assert device.port == DFL_MGMT_PORT

    @staticmethod
    def test_port_is_int(mocker):
        """Test: Kwarg port of type string is cast to an int

        Assertions
        ----------
        - Mock socket instance 'connect' should be called with port of type int
        """

        mock_socket = mocker.patch('socket.socket').return_value

        BigIpUtils.get_mgmt_client(token=TOKEN, skip_ready_check=False, port='443')

        mock_socket.connect.assert_called_with((HOST, 443))

    @staticmethod
    def test_is_ready(mocker):
        """Test: Device ready check

        Assertions
        ----------
        - Mock socket instance 'connect' should be called with correct host/port
        """

        mock_socket = mocker.patch('socket.socket').return_value

        device = BigIpUtils.get_mgmt_client(token=TOKEN, skip_ready_check=False)

        mock_socket.connect.assert_called_with((HOST, device.port))

    @staticmethod
    def test_is_ready_false(mocker):
        """Test: Device ready check should raise exception

        Assertions
        ----------
        - Mgmt client should raise DeviceReadyError on socket.timeout error
        """

        mock_socket = mocker.patch('socket.socket').return_value
        mock_socket.connect.side_effect = socket.timeout

        mocker.patch('time.sleep')

        pytest.raises(
            exceptions.DeviceReadyError,
            BigIpUtils.get_mgmt_client,
            token=TOKEN,
            skip_ready_check=False)

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_get_info(mgmt_client, mocker):
        """Test: get_info

        Assertions
        ----------
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
        mocker.patch(REQ).return_value.json = Mock(return_value=response)

        assert mgmt_client.get_info()['version'] == version

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_request_no_token(mgmt_client):
        """Test: make_request with no device token

        Assertions
        ----------
        - AuthRequiredError exception should be raised
        """

        mgmt_client.token = None

        pytest.raises(exceptions.AuthRequiredError, mgmt_client.make_request, '/')

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_request_auth_header(mgmt_client, mocker):
        """Test: make_request should insert auth header

        Assertions
        ----------
        - make_request should insert auth header: {'X-F5-Auth-Token': 'token'}
        """

        mock = mocker.patch(REQ)

        mgmt_client.make_request('/')

        _, kwargs = mock.call_args
        assert kwargs['headers'][project_constants.F5_AUTH_TOKEN_HEADER] == TOKEN

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_request_bool(mgmt_client, mocker):
        """Test: make_request with bool_response=True

        Assertions
        ----------
        - make_request should return boolean (True)
        """

        mocker.patch(REQ).return_value.json = Mock(return_value={})

        assert mgmt_client.make_request('/', bool_response=True)

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_ssh_request_stderr(mgmt_client, mocker):
        """Test: make_ssh_request - stderr response should raise exception

        Assertions
        ----------
        - SSHCommandStdError exception should be raised
        """

        mock_utils.create_ssh_client(
            mocker.patch('paramiko.SSHClient'),
            '',
            stderr='error'
        )

        pytest.raises(exceptions.SSHCommandStdError, mgmt_client.make_ssh_request, 'command')

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_ssh_request_connect_error(mgmt_client, mocker):
        """Test: make_ssh_request - connect exception should raise exception

        Assertions
        ----------
        - SSHException should be raised
        """

        mock_utils.create_ssh_client(
            mocker.patch('paramiko.SSHClient'), '', connect_raise=ssh_exception.SSHException)

        pytest.raises(ssh_exception.SSHException, mgmt_client.make_ssh_request, 'command')

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_request_content_length_header_zero(mgmt_client, mocker):
        """Test: make_request with Content-Length header set to '0'

        Assertions
        ----------
        - Response should equal empty dict
        """

        mock_request = mocker.patch(REQ).return_value
        mock_request.json = Mock(return_value={'foo': 'bar'})
        type(mock_request).headers = PropertyMock(return_value={'content-length': '0'})

        assert mgmt_client.make_request('/') is None

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_make_request_with_204_status_code(mgmt_client, mocker):
        """Test: make_request with Content-Length header set to '0'

        Assertions
        ----------
        - Response should equal empty dict
        """

        mock_request = mocker.patch(REQ).return_value
        type(mock_request).status_code = PropertyMock(return_value=204)

        assert mgmt_client.make_request('/') is None
