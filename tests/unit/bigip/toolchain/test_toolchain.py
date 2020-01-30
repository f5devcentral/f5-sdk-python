""" Test BIG-IP module """

import json
import tempfile
import shutil
from os import path

from f5sdk import exceptions
from f5sdk.bigip.toolchain import ToolChainClient

from ....global_test_imports import pytest, Mock

from ....shared import constants
from ....shared import mock_utils

TOKEN = constants.TOKEN

REQ = constants.MOCK['requests']

EXAMPLE_TOOLCHAIN_METADATA = {
    'components': {
        'as3': {
            'versions': {
                'x.x.x': {
                    'latest': True
                },
                'x.x.y': {
                    'latest': False
                }
            }
        }
    }
}


class TestToolChain(object):
    """Test Class: bigip.toolchain module """

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_init(toolchain_client):
        """Test: Initialize toolchain client

        Assertions
        ----------
        - 'package' attribute exists
        - 'service' attribute exists
        """

        assert toolchain_client.package
        assert toolchain_client.service

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_component_invalid(mgmt_client):
        """Test: Invalid component

        Assertions
        ----------
        - InvalidComponentError exception should be raised
        """

        pytest.raises(
            exceptions.InvalidComponentError,
            ToolChainClient,
            mgmt_client,
            'foo',
            use_latest_metadata=False
        )

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_component_version_invalid(mgmt_client):
        """Test: Invalid component version

        Assertions
        ----------
        - InvalidComponentVersionError exception should be raised
        """

        pytest.raises(
            exceptions.InvalidComponentVersionError,
            ToolChainClient,
            mgmt_client,
            'as3',
            version='0.0.0',
            use_latest_metadata=False
        )

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_download_latest_metadata(mgmt_client, mocker):
        """Test: Download latest metadata from CDN when
        - use_latest_metadata=True (which is the default)

        Assertions
        ----------
        - instantiating a toolchain client should download metadata
        """

        mock_conditions = [
            {
                'type': 'url',
                'value': 'cdn.f5.com',
                'response': {
                    'body': EXAMPLE_TOOLCHAIN_METADATA
                }
            }
        ]
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            {}, conditional=mock_conditions)

        toolchain_client = ToolChainClient(mgmt_client, 'as3')

        assert toolchain_client.version == 'x.x.x'

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_download_latest_metadata_http_error(mgmt_client, mocker):
        """Test: Download latest metadata from CDN continues when http error occurs

        Assertions
        ----------
        - Error/exception should be silently caught and logged
        """

        mocker.patch(REQ).side_effect = Exception('Error')

        mock_logger = Mock()
        mocker.patch('f5sdk.logger.Logger.get_logger').return_value = mock_logger

        ToolChainClient(mgmt_client, 'as3', use_latest_metadata=True)

        assert mock_logger.warning.call_count == 1
        error_message = 'Error downloading metadata file'
        assert error_message in mock_logger.warning.call_args_list[0][0][0]


class TestToolChainPackage(object):
    """Test Class: bigip.toolchain.package module """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_install(mgmt_client, mocker):
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
                'value': 'github.com',
                'response': {'body': 'foo'.encode()}
            },
            {
                'type': 'url',
                'value': '/mgmt/shared/file-transfer/uploads',
                'response': {'body': {'id': 'xxxx'}}
            },
            {
                'type': 'url',
                'value': '/mgmt/shared/iapp/package-management-tasks',
                'response': {'body': {'id': 'xxxx', 'status': 'FINISHED'}}
            }
        ]
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            {}, conditional=mock_conditions)

        toolchain = ToolChainClient(mgmt_client, 'as3', version='3.9.0', use_latest_metadata=False)

        assert toolchain.package.install() == {
            'component': 'as3',
            'version': '3.9.0'
        }

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_uninstall(mgmt_client, mocker):
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
                'value': '/mgmt/shared/file-transfer/uploads',
                'response': {'body': {'id': 'xxxx'}}
            },
            {
                'type': 'url',
                'value': '/mgmt/shared/iapp/package-management-tasks',
                'response': {'body': {'id': 'xxxx', 'status': 'FINISHED'}}
            }
        ]
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            {}, conditional=mock_conditions)

        toolchain = ToolChainClient(mgmt_client, 'as3', version='3.9.0', use_latest_metadata=False)

        assert toolchain.package.uninstall() == {
            'component': 'as3',
            'version': '3.9.0'
        }

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_is_installed(mgmt_client, mocker):
        """Test: is_installed

        Assertions
        ----------
        - is_installed() response should be a dict
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
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_resp)

        toolchain_client = ToolChainClient(
            mgmt_client, 'as3', version='3.9.0', use_latest_metadata=False)

        is_installed = toolchain_client.package.is_installed()
        assert is_installed['installed']
        assert is_installed['installed_version'] == '3.9.0'
        assert is_installed['latest_version'] != ''

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_failed_task_status(toolchain_client, mocker):
        """Test: is_installed with failed RPM task status

        Assertions
        ----------
        - Exception exception should be raised
        """

        mock_resp = {
            'id': 'xxxx',
            'status': 'FAILED'
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_resp)

        pytest.raises(Exception, toolchain_client.package.is_installed)

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_is_not_installed(toolchain_client, mocker):
        """Test: is_not_installed

        Assertions
        ----------
        - is_installed() response should be a dict
        """

        mock_resp = {
            'id': 'xxxx',
            'status': 'FINISHED',
            'queryResponse': [
                {
                    'packageName': ''
                }
            ]
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_resp)

        is_installed = toolchain_client.package.is_installed()
        assert not is_installed['installed']
        assert is_installed['installed_version'] == ''
        assert is_installed['latest_version'] != ''


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

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_show(toolchain_client, mocker):
        """Test: show

        Assertions
        ----------
        - show() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        assert toolchain_client.service.show() == mock_response

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_create(toolchain_client, mocker):
        """Test: create

        Assertions
        ----------
        - create() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        assert toolchain_client.service.create(config={'config': 'foo'}) == mock_response

    @pytest.mark.usefixtures("toolchain_client")
    def test_create_config_file(self, toolchain_client, mocker):
        """Test: create with config file

        Assertions
        ----------
        - create() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        config_file = path.join(self.test_tmp_dir, 'config.json')
        with open(config_file, 'w') as _f:
            _f.write(json.dumps({'config': 'foo'}))

        assert toolchain_client.service.create(config_file=config_file) == mock_response

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_create_no_config(toolchain_client):
        """Test: create with no config provided

        Assertions
        ----------
        - InputRequiredError exception should be raised
        """

        pytest.raises(exceptions.InputRequiredError, toolchain_client.service.create)

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_create_async(toolchain_client, mocker):
        """Test: create async response

        Assertions
        ----------
        - create() response should equal task requests response
        - make_request() should be called twice
        - make_request() second call uri should equal task uri
        """

        mock_response = {'foo': 'bar'}
        make_request_mock = mocker.patch(
            'f5sdk.utils.http_utils.make_request',
            side_effect=[({'selfLink': 'https://localhost/foo/1234'}, 202), (mock_response, 200)])

        response = toolchain_client.service.create(config={'foo': 'bar', 'async': True})

        assert response == mock_response
        assert make_request_mock.call_count == 2
        args, _ = make_request_mock.call_args_list[1]
        assert args[1] == '/foo/1234'

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_delete(toolchain_client, mocker):
        """Test: delete

        Assertions
        ----------
        - delete() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        assert toolchain_client.service.delete() == mock_response

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_delete_method_exception(mgmt_client):
        """Test: delete - against invalid toolchain component

        For example, DO does not support the 'DELETE' method

        Assertions
        ----------
        - Exception should be raised
        """

        toolchain_client = ToolChainClient(mgmt_client, 'do', use_latest_metadata=False)

        pytest.raises(Exception, toolchain_client.service.delete)

    @staticmethod
    @pytest.mark.usefixtures("toolchain_client")
    def test_is_available(toolchain_client, mocker):
        """Test: is_available

        Assertions
        ----------
        - is_available() response should be boolean (True)
        """

        mocker.patch(REQ).return_value.json = Mock(return_value={'message': 'success'})

        assert toolchain_client.service.is_available()
