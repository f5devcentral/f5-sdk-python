""" Test BIG-IP module """

import json
import tempfile
import shutil
from os import path

from f5sdk import exceptions
from f5sdk.bigip.extension import ExtensionClient

from ....global_test_imports import pytest, Mock

from ....shared import constants
from ....shared import mock_utils

TOKEN = constants.TOKEN

REQ = constants.MOCK['requests']

EXAMPLE_EXTENSION_METADATA = {
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


class TestExtension(object):
    """Test Class: bigip.extension module """

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_init(extension_client):
        """Test: Initialize extension client

        Assertions
        ----------
        - 'package' attribute exists
        - 'service' attribute exists
        """

        assert extension_client.package
        assert extension_client.service

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
            ExtensionClient,
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
            ExtensionClient,
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
        - instantiating a extension client should download metadata
        """

        mock_conditions = [
            {
                'type': 'url',
                'value': 'cdn.f5.com',
                'response': {
                    'body': EXAMPLE_EXTENSION_METADATA
                }
            }
        ]
        mocker.patch(REQ).side_effect = mock_utils.create_response(
            {}, conditional=mock_conditions)

        extension_client = ExtensionClient(mgmt_client, 'as3', use_latest_metadata=True)

        assert extension_client.version == 'x.x.x'

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

        ExtensionClient(mgmt_client, 'as3', use_latest_metadata=True)

        assert mock_logger.warning.call_count == 1
        error_message = 'Error downloading metadata file'
        assert error_message in mock_logger.warning.call_args_list[0][0][0]


class TestExtensionPackage(object):
    """Test Class: bigip.extension.package module """

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

        extension = ExtensionClient(mgmt_client, 'as3', version='3.9.0')

        assert extension.package.install() == {
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

        extension = ExtensionClient(mgmt_client, 'as3', version='3.9.0')

        assert extension.package.uninstall() == {
            'component': 'as3',
            'version': '3.9.0'
        }

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_uninstall_with_dependency(mgmt_client, mocker):
        """Test: uninstall with existing dependency

        Assertions
        ----------
        - uninstall() should log a warning about existing dependency
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
        mock_logger = Mock()
        mocker.patch('f5sdk.logger.Logger.get_logger').return_value = mock_logger

        extension = ExtensionClient(mgmt_client, 'as3', version='3.10.0')
        extension.package.uninstall()

        assert mock_logger.warning.call_count == 1
        logged_message = mock_logger.warning.call_args_list[0][0][0]
        assert 'A component package dependency has not been removed' in logged_message
        assert 'See documentation for more details' in logged_message

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

        extension_client = ExtensionClient(
            mgmt_client, 'as3', version='3.9.0')

        is_installed = extension_client.package.is_installed()
        assert is_installed['installed']
        assert is_installed['installed_version'] == '3.9.0'
        assert is_installed['latest_version'] != ''

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_failed_task_status(extension_client, mocker):
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

        pytest.raises(Exception, extension_client.package.is_installed)

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_is_installed_two_digit_version(mgmt_client, mocker):
        """Test: is_installed where package name major version contains two digits

        Assertions
        ----------
        - is_installed() installed_version response should be correctly parsed
        """

        mock_resp = {
            'id': 'xxxx',
            'status': 'FINISHED',
            'queryResponse': [
                {
                    'packageName': 'f5-appsvcs-1.10.0-0.noarch'
                }
            ]
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_resp)

        extension_client = ExtensionClient(
            mgmt_client, 'as3')

        is_installed = extension_client.package.is_installed()
        assert is_installed['installed_version'] == '1.10.0'

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_is_not_installed(extension_client, mocker):
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

        is_installed = extension_client.package.is_installed()
        assert not is_installed['installed']
        assert is_installed['installed_version'] == ''
        assert is_installed['latest_version'] != ''


class TestExtensionService(object):
    """Test Class: bigip.extension.service module """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.test_tmp_dir = tempfile.mkdtemp()

    @classmethod
    def teardown_class(cls):
        """" Teardown func """
        shutil.rmtree(cls.test_tmp_dir)

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_show(extension_client, mocker):
        """Test: show

        Assertions
        ----------
        - show() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.show() == mock_response

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_create(extension_client, mocker):
        """Test: create

        Assertions
        ----------
        - create() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.create(config={'config': 'foo'}) == mock_response

    @pytest.mark.usefixtures("extension_client")
    def test_create_config_file(self, extension_client, mocker):
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

        assert extension_client.service.create(config_file=config_file) == mock_response

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_create_no_config(extension_client):
        """Test: create with no config provided

        Assertions
        ----------
        - InputRequiredError exception should be raised
        """

        pytest.raises(exceptions.InputRequiredError, extension_client.service.create)

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_create_async(extension_client, mocker):
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

        response = extension_client.service.create(config={'foo': 'bar', 'async': True})

        assert response == mock_response
        assert make_request_mock.call_count == 2
        args, _ = make_request_mock.call_args_list[1]
        assert args[1] == '/foo/1234'

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_delete(extension_client, mocker):
        """Test: delete

        Assertions
        ----------
        - delete() response should equal requests response
        """

        mock_response = {'message': 'success'}
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.delete() == mock_response

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_delete_method_exception(mgmt_client):
        """Test: delete - against invalid extension component

        For example, DO does not support the 'DELETE' method

        Assertions
        ----------
        - Exception should be raised
        """

        extension_client = ExtensionClient(mgmt_client, 'do')

        pytest.raises(Exception, extension_client.service.delete)

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_is_available(extension_client, mocker):
        """Test: is_available

        Assertions
        ----------
        - is_available() response should be boolean (True)
        """

        mocker.patch(REQ).return_value.json = Mock(return_value={'message': 'success'})

        assert extension_client.service.is_available()

    @staticmethod
    @pytest.mark.usefixtures("extension_client")
    def test_show_inspect(extension_client, mocker):
        """Test: show_info

        Assertions
        ----------
        - show_info() response should be info endpoint API response
        """

        mocker.patch(REQ).return_value.json = Mock(return_value={'version': 'x.x.x.x'})

        assert extension_client.service.show_info() == {'version': 'x.x.x.x'}

    @staticmethod
    @pytest.mark.usefixtures("cf_extension_client")
    def test_cf_show_failover(cf_extension_client, mocker):
        """Test: show_failover

        Assertions
        ----------
        - show_failover() response should be trigger endpoint API response
        """
        sample_return_value = {
            "code": 200,
            "failoverOperations": {},
            "instance": "A",
            "message": "Failover state file was reset",
            "taskState": "SUCCEEDED",
            "timestamp": "XYZ"
        }


        mocker.patch(REQ).return_value.json = Mock(return_value=sample_return_value)

        assert cf_extension_client.service.show_failover() == sample_return_value

    @staticmethod
    @pytest.mark.usefixtures("cf_extension_client")
    def test_cf_show_inspect(cf_extension_client, mocker):
        """Test: show_inspect

        Assertions
        ----------
        - show_inspect() response should be inspect endpoint API response
        """

        sample_return_value = {
            "addresses": [
                {
                    "networkInterfaceId": "nic0",
                    "privateIpAddress": "x.x.x.x",
                    "publicIpAddress": "y.y.y.y"
                },
                {
                    "networkInterfaceId": "nic1",
                    "privateIpAddress": "x.x.x.x",
                    "publicIpAddress": "y.y.y.y"
                },
                {
                    "networkInterfaceId": "nic2",
                    "privateIpAddress": "x.x.x.x",
                    "publicIpAddress": "null"
                }
            ],
            "deviceStatus": "active",
            "hostName": "test",
            "instance": "test-i",
            "routes": [
                {
                    "networkId": "int-net-test",
                    "routeTableId": "1",
                    "routeTableName": "test-i"
                }
            ],
            "trafficGroup": [
                {
                    "name": "/Common/traffic-group-1"
                }
            ]
        }

        mocker.patch(REQ).return_value.json = Mock(return_value=sample_return_value)

        assert cf_extension_client.service.show_inspect() == sample_return_value

    @staticmethod
    @pytest.mark.usefixtures("cf_extension_client")
    def test_cf_trigger_failover(cf_extension_client, mocker):
        """Test: show_inspect

        Assertions
        ----------
        - trigger() response should be trigger endpoint API response
        """

        sample_return_value = {
            "failoverOperations": {
                "addresses": {
                    "fwdRules": {
                        "operations": []
                    },
                    "nics": {
                        "associate": [],
                        "disassociate": []
                    }
                },
                "routes": {
                    "operations": []
                }
            },
            "instance": "test-i",
            "message": "Failover Completed Successfully",
            "taskState": "SUCCEEDED",
            "timestamp": "XYZ"
        }

        mocker.patch(REQ).return_value.json = Mock(return_value=sample_return_value)

        assert cf_extension_client.service.trigger() == sample_return_value

    @staticmethod
    @pytest.mark.usefixtures("cf_extension_client")
    def test_cf_show_info(cf_extension_client, mocker):
        """Test: reset

        Assertions
        ----------
        - reset() response should be reset endpoint API response
        """

        sample_return_value = {
            "version": "0",
            "schemaCurrent": "0.9.1",
            "schemaMinimum": "1.0.0",
            "release": "1"
        }

        mocker.patch(REQ).return_value.json = Mock(return_value=sample_return_value)

        assert cf_extension_client.service.info() == sample_return_value

    @staticmethod
    @pytest.mark.usefixtures("cf_extension_client")
    def test_cf_reset(cf_extension_client, mocker):
        """Test: reset

        Assertions
        ----------
        - reset() response should be reset endpoint API response
        """

        sample_return_value = {
            "message": "success"
        }

        mocker.patch(REQ).return_value.json = Mock(return_value=sample_return_value)

        assert cf_extension_client.service.reset() == sample_return_value

    @staticmethod
    @pytest.mark.usefixtures("ts_extension_client")
    def test_ts_show_info(ts_extension_client, mocker):
        """Test: show_info

        Assertions
        ----------
        - show_info() response should be info endpoint API response
        """
        sample_return_value = {
            "nodeVersion": "v8.11.1",
            "version": "1.9.0",
            "release": "1",
            "schemaCurrent": "0.9.0",
            "schemaMinimum": "1.9.0"
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=sample_return_value)

        assert ts_extension_client.service.show_info() == sample_return_value
