""" Test BIG-IP module """

import json
import tempfile
import shutil
from os import path

from f5cloudsdk import exceptions
from f5cloudsdk.bigip.toolchain import ToolChainClient

from ...global_test_imports import pytest, Mock

from ...shared import constants
from ...shared import mock_utils

TOKEN = constants.TOKEN

REQ = constants.MOCK['requests']


class TestToolChain(object):
    """Test Class: bigip.toolchain module """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_init(mgmt_client):
        """Test: Initialize toolchain client

        Assertions
        ----------
        - 'package' attribute exists
        - 'service' attribute exists
        """

        toolchain = ToolChainClient(mgmt_client, 'as3')

        assert toolchain.package
        assert toolchain.service

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_component_invalid(mgmt_client):
        """Test: Invalid component

        Assertions
        ----------
        - InvalidComponentError exception should be raised
        """

        pytest.raises(exceptions.InvalidComponentError, ToolChainClient, mgmt_client, 'foo')

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
            version='0.0.0'
        )


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

        toolchain = ToolChainClient(mgmt_client, 'as3', version='3.9.0')

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

        toolchain = ToolChainClient(mgmt_client, 'as3', version='3.9.0')

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
        - is_installed() response should be a dict {'installed': True,
                                                    'installed_version': '3.9.0',
                                                    'latest_version': '3.13.0'}
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

        toolchain = ToolChainClient(mgmt_client, 'as3', version='3.9.0')

        assert toolchain.package.is_installed() == {'installed': True,
                                                    'installed_version': '3.9.0',
                                                    'latest_version': '3.13.0'}

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_failed_task_status(mgmt_client, mocker):
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

        toolchain = ToolChainClient(mgmt_client, 'as3', version='3.9.0')

        pytest.raises(Exception, toolchain.package.is_installed)

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_is_not_installed(mgmt_client, mocker):
        """Test: is_not_installed

        Assertions
        ----------
        - is_installed() response should be a dict {'installed': False,
                                                    'installed_version': '',
                                                    'latest_version': '3.13.0'}
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

        toolchain = ToolChainClient(mgmt_client, 'as3')

        assert toolchain.package.is_installed() == {'installed': False,
                                                    'installed_version': '',
                                                    'latest_version': '3.13.0'}


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
    @pytest.mark.usefixtures("mgmt_client")
    def test_show(mgmt_client, mocker):
        """Test: show

        Assertions
        ----------
        - show() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        toolchain = ToolChainClient(mgmt_client, 'as3')

        assert toolchain.service.show() == mock_response

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_create(mgmt_client, mocker):
        """Test: create

        Assertions
        ----------
        - create() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        toolchain = ToolChainClient(mgmt_client, 'as3')

        assert toolchain.service.create(config={'config': 'foo'}) == mock_response

    @pytest.mark.usefixtures("mgmt_client")
    def test_create_config_file(self, mgmt_client, mocker):
        """Test: create with config file

        Assertions
        ----------
        - create() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        toolchain = ToolChainClient(mgmt_client, 'as3')

        config_file = path.join(self.test_tmp_dir, 'config.json')
        with open(config_file, 'w') as _f:
            _f.write(json.dumps({'config': 'foo'}))

        assert toolchain.service.create(config_file=config_file) == mock_response

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_create_no_config(mgmt_client):
        """Test: create with no config provided

        Assertions
        ----------
        - InputRequiredError exception should be raised
        """

        toolchain = ToolChainClient(mgmt_client, 'as3')

        pytest.raises(exceptions.InputRequiredError, toolchain.service.create)

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_create_async(mgmt_client, mocker):
        """Test: create async response

        Assertions
        ----------
        - create() response should equal task requests response
        - make_request() should be called twice
        - make_request() second call uri should equal task uri
        """

        mock_response = {'foo': 'bar'}
        make_request_mock = mocker.patch(
            'f5cloudsdk.utils.http_utils.make_request',
            side_effect=[({'selfLink': 'https://localhost/foo/1234'}, 202), (mock_response, 200)])

        toolchain = ToolChainClient(mgmt_client, 'as3')

        response = toolchain.service.create(config={'foo': 'bar', 'async': True})

        assert mock_response == response
        assert make_request_mock.call_count == 2
        args, _ = make_request_mock.call_args_list[1]
        assert args[1] == '/foo/1234'

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_delete(mgmt_client, mocker):
        """Test: delete

        Assertions
        ----------
        - delete() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        toolchain = ToolChainClient(mgmt_client, 'as3')

        assert toolchain.service.delete() == mock_response

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_delete_method_exception(mgmt_client):
        """Test: delete - against invalid toolchain component

        For example, DO does not support the 'DELETE' method

        Assertions
        ----------
        - Exception should be raised
        """

        toolchain = ToolChainClient(mgmt_client, 'do')

        pytest.raises(Exception, toolchain.service.delete)

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_is_available(mgmt_client, mocker):
        """Test: is_available

        Assertions
        ----------
        - is_available() response should be boolean (True)
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        toolchain = ToolChainClient(mgmt_client, 'as3')

        assert toolchain.service.is_available()
