""" Test BIG-IP module """

## standard imports ##
from os import path
import json
import tempfile
import shutil
## project imports ##
from f5cloudsdk import exceptions
from f5cloudsdk.bigip.toolchain import ToolChainClient
## unittest imports ##
from ...global_test_imports import pytest

## local test imports ##
from ...shared import constants
from ...shared import mock_utils
from . import utils as BigIpUtils

TOKEN = constants.TOKEN

## packages to mock ##
REQ = constants.MOCK['requests']

class TestToolChain(object):
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

        pytest.raises(exceptions.InvalidComponentError, ToolChainClient, device, 'foo')

    def test_component_version_invalid(self):
        """Test: Invalid component version

        Assertions
        ----------
        - InvalidComponentVersionError exception should be raised
        """

        device = BigIpUtils.get_mgmt_client(token=TOKEN)

        pytest.raises(
            exceptions.InvalidComponentVersionError,
            ToolChainClient,
            device,
            'as3',
            version='0.0.0'
        )

class TestToolChainPackage(object):
    """Test Class: bigip.toolchain.package module """

    def test_install(self, mocker):
        """Test: install

        Assertions
        ----------
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
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            {}, conditional=mock_conditions)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        response = toolchain.package.install()
        assert response == {
            'component': 'as3',
            'version': '3.9.0'
        }

    def test_uninstall(self, mocker):
        """Test: uninstall

        Assertions
        ----------
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
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            {}, conditional=mock_conditions)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        response = toolchain.package.uninstall()
        assert response == {
            'component': 'as3',
            'version': '3.9.0'
        }

    def test_is_installed(self, mocker):
        """Test: is_installed

        Assertions
        ----------
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
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        response = toolchain.package.is_installed()
        assert response

    def test_failed_task_status(self, mocker):
        """Test: is_installed with failed RPM task status

        Assertions
        ----------
        - Exception exception should be raised
        """

        mock_resp = {
            'id': 'xxxx',
            'status': 'FAILED'
        }
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3', version='3.9.0')

        pytest.raises(Exception, toolchain.package.is_installed)

class TestToolChainService(object):
    """Test Class: bigip.toolchain.service module """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.test_tmp_dir = tempfile.mkdtemp()
    @classmethod
    def teardown_class(cls):
        """" Teardown func """
        shutil.rmtree(cls.test_tmp_dir)

    def test_show(self, mocker):
        """Test: show

        Assertions
        ----------
        - show() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mocker.patch(REQ).side_effect = mock_utils.create_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.show()
        assert mock_resp == response

    def test_create(self, mocker):
        """Test: create

        Assertions
        ----------
        - create() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mocker.patch(REQ).side_effect = mock_utils.create_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.create(config={'config': 'foo'})
        assert mock_resp == response

    def test_create_config_file(self, mocker):
        """Test: create with config file

        Assertions
        ----------
        - create() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mocker.patch(REQ).side_effect = mock_utils.create_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        config_file = path.join(self.test_tmp_dir, 'config.json')
        with open(config_file, 'w') as _f:
            _f.write(json.dumps({'config': 'foo'}))

        response = toolchain.service.create(config_file=config_file)
        assert mock_resp == response

    def test_create_no_config(self, mocker):
        """Test: create with no config provided

        Assertions
        ----------
        - InputRequiredError exception should be raised
        """

        mock_resp = {'message': 'success'}
        mocker.patch(REQ).side_effect = mock_utils.create_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        pytest.raises(exceptions.InputRequiredError, toolchain.service.create)

    def test_delete(self, mocker):
        """Test: delete

        Assertions
        ----------
        - delete() response should equal requests response
        """

        mock_resp = {'message': 'success'}
        mocker.patch(REQ).side_effect = mock_utils.create_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.delete()
        assert mock_resp == response

    def test_delete_method_exception(self, mocker):
        """Test: delete - against invalid toolchain component

        For example, DO does not support the 'DELETE' method

        Assertions
        ----------
        - Exception should be raised
        """

        mock_resp = {'message': 'success'}
        mocker.patch(REQ).side_effect = mock_utils.create_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'do')

        pytest.raises(Exception, toolchain.service.delete)

    def test_is_available(self, mocker):
        """Test: is_available

        Assertions
        ----------
        - is_available() response should be boolean (True)
        """

        mock_resp = {'message': 'success'}
        mocker.patch(REQ).side_effect = mock_utils.create_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)
        toolchain = ToolChainClient(device, 'as3')

        response = toolchain.service.is_available()
        assert response
