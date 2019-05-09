""" Test BIG-IP module """

## unittest imports ##
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError: # python 2.x support
    from mock import Mock, MagicMock, patch

## standard imports ##
from os import path
import json
import tempfile
import shutil

## project imports ##
from f5cloudsdk import exceptions
from f5cloudsdk.bigip.toolchain import ToolChainClient

## local test imports ##
from ...shared import utils
from . import utils as BigIpUtils

TOKEN = 'mytoken'

class TestToolChain(unittest.TestCase):
    """Test Class: bigip.toolchain module """

    def test_init(self):
        """Test: Initialize toolchain client

        Assertions
        ----------
        - 'package' attribute exists
        - 'service' attribute exists
        """

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        assert toolchain.package
        assert toolchain.service

    def test_component_invalid(self):
        """Test: Invalid component

        Assertions
        ----------
        - InvalidComponentError exception should be raised
        """

        device = BigIpUtils.get_mgmt_client(token=TOKEN)

        self.assertRaises(exceptions.InvalidComponentError, ToolChainClient, device, 'foo')

    def test_component_version_invalid(self):
        """Test: Invalid component version

        Assertions
        ----------
        - InvalidComponentVersionError exception should be raised
        """

        device = BigIpUtils.get_mgmt_client(token=TOKEN)

        self.assertRaises(
            exceptions.InvalidComponentVersionError,
            ToolChainClient,
            device,
            'as3',
            version='0.0.0'
        )

class TestToolChainPackage(unittest.TestCase):
    """Test Class: bigip.toolchain.package module """

    @patch('requests.request')
    def test_install(self, mock_request):
        """Test: install

        Assertions
        ----------
        - Mocked request should be called
        - install() response should equal:
            {
                'component': 'as3',
                'version': '3.9.0'
            }
        """

        mock_conditions = [
            {
                'type': 'url',
                'value':'github.com',
                'response': {'body': 'foo'.encode()}
            },
            {
                'type': 'url',
                'value':'/mgmt/shared/file-transfer/uploads',
                'response': {'body': {'id': 'xxxx'}}
            },
            {
                'type': 'url',
                'value':'/mgmt/shared/iapp/package-management-tasks',
                'response': {'body': {'id': 'xxxx', 'status': 'FINISHED'}}
            }
        ]
        mock_request.side_effect = utils.create_mock_response({}, conditional=mock_conditions)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        response = toolchain.package.install()
        assert mock_request.called
        assert response == {
            'component': 'as3',
            'version': '3.9.0'
        }

    @patch('requests.request')
    def test_uninstall(self, mock_request):
        """Test: uninstall

        Assertions
        ----------
        - Mocked request should be called
        - uninstall() response should equal:
            {
                'component': 'as3',
                'version': '3.9.0'
            }
        """

        mock_conditions = [
            {
                'type': 'url',
                'value':'/mgmt/shared/file-transfer/uploads',
                'response': {'body': {'id': 'xxxx'}}
            },
            {
                'type': 'url',
                'value':'/mgmt/shared/iapp/package-management-tasks',
                'response': {'body': {'id': 'xxxx', 'status': 'FINISHED'}}
            }
        ]
        mock_request.side_effect = utils.create_mock_response({}, conditional=mock_conditions)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        response = toolchain.package.uninstall()
        assert mock_request.called
        assert response == {
            'component': 'as3',
            'version': '3.9.0'
        }


    @patch('requests.request')
    def test_is_installed(self, mock_request):
        """Test: is_installed

        Assertions
        ----------
        - Mocked request should be called
        - is_installed() response should be boolean (True)
        """

        mock_resp = {
            'id': 'xxxx',
            'status': 'FINISHED',
            'queryResponse': [
                {
                    'packageName': 'f5-appsvcs-3.9.0-3.noarch'
                }
            ]
        }
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        response = toolchain.package.is_installed()
        assert mock_request.called
        assert response

    @patch('requests.request')
    def test_failed_task_status(self, mock_request):
        """Test: is_installed with failed RPM task status

        Assertions
        ----------
        - Exception exception should be raised
        """

        mock_resp = {
            'id': 'xxxx',
            'status': 'FAILED',
            'queryResponse': [
                {
                    'packageName': 'f5-appsvcs-3.9.0-3.noarch'
                }
            ]
        }
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        self.assertRaises(Exception, toolchain.package.is_installed)

class TestToolChainService(unittest.TestCase):
    """Test Class: bigip.toolchain.service module """
    def setUp(self):
        self.test_tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_tmp_dir)

    @patch('requests.request')
    def test_show(self, mock_request):
        """Test: show

        Assertions
        ----------
        - Mocked request should be called
        - show() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.show()
        assert mock_request.called
        assert mock_resp == response

    @patch('requests.request')
    def test_create(self, mock_request):
        """Test: create

        Assertions
        ----------
        - Mocked request should be called
        - create() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.create(config={'config': 'foo'})
        assert mock_request.called
        assert mock_resp == response

    @patch('requests.request')
    def test_create_config_file(self, mock_request):
        """Test: create with config file

        Assertions
        ----------
        - Mocked request should be called
        - create() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        config_file = path.join(self.test_tmp_dir, 'config.json')
        with open(config_file, 'w') as _f:
            _f.write(json.dumps({'config': 'foo'}))

        response = toolchain.service.create(config_file=config_file)
        assert mock_request.called
        assert mock_resp == response

    @patch('requests.request')
    def test_create_no_config(self, mock_request):
        """Test: create with no config provided

        Assertions
        ----------
        - InputRequiredError exception should be raised
        """

        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        self.assertRaises(exceptions.InputRequiredError, toolchain.service.create)

    @patch('requests.request')
    def test_delete(self, mock_request):
        """Test: delete

        Assertions
        ----------
        - Mocked request should be called
        - delete() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.delete()
        assert mock_request.called
        assert mock_resp == response

    @patch('requests.request')
    def test_delete_methods_exception(self, mock_request):
        """Test: delete

        Assertions
        ----------
        - Exception exception should be raised
        """

        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'do')

        self.assertRaises(Exception, toolchain.service.delete)

    @patch('requests.request')
    def test_is_available(self, mock_request):
        """Test: is_available

        Assertions
        ----------
        - Mocked request should be called
        - is_available() response should be boolean (True)
        """

        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.is_available()
        assert mock_request.called
        assert response
