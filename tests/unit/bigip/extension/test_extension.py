""" Test AS3 Client """

import json
import tempfile
import shutil
from os import path

from f5sdk import exceptions
from f5sdk.utils import http_utils

from ....global_test_imports import pytest, Mock, PropertyMock
from ....shared import constants
from ....shared import mock_utils

REQUESTS = constants.MOCK['requests']
EXAMPLE_VERSION_INFO = {
    'x.x.x': {
        'latest': True
    },
    'x.x.y': {
        'latest': False
    }
}
EXAMPLE_EXTENSION_METADATA = {
    'components': {
        'as3': {
            'versions': EXAMPLE_VERSION_INFO
        },
        'do': {
            'versions': EXAMPLE_VERSION_INFO
        },
        'ts': {
            'versions': EXAMPLE_VERSION_INFO
        },
        'cf': {
            'versions': EXAMPLE_VERSION_INFO
        }
    }
}
FIXED_INFO = {
    'as3': {
        'version': '3.10.0',
        'name': 'f5-appsvcs',
        'package_name': 'f5-appsvcs-3.10.0-5.noarch',
        'previous_version': '3.9.0',
    },
    'do': {
        'version': '1.10.0',
        'name': 'f5-declarative-onboarding',
        'package_name': 'f5-declarative-onboarding-1.10.0-2.noarch',
        'previous_version': '1.9.0',
    },
    'ts': {
        'version': '1.10.0',
        'name': 'f5-telemetry',
        'package_name': 'f5-telemetry-1.10.0-2.noarch',
        'previous_version': '1.9.0',
    },
    'cf': {
        'version': '1.1.0',
        'name': 'f5-cloud-failover',
        'package_name': 'f5-cloud-failover-1.1.0-0.noarch',
        'previous_version': '1.0.0',
    }
}


# pylint: disable=too-many-public-methods
@pytest.mark.parametrize("component", ["as3", "do", "ts", "cf"])
class TestExtensionClients(object):
    """Test Extension Clients - Iterates through each parametrized component
    and performs tests.  Any test that applies to all components could go here
    """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.test_tmp_dir = tempfile.mkdtemp()

    @classmethod
    def teardown_class(cls):
        """" Teardown func """
        shutil.rmtree(cls.test_tmp_dir)

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_init(component, create_extension_client):
        """Test: Initialize extension client

        Assertions
        ----------
        - 'package' attribute exists
        - 'service' attribute exists
        """
        extension_client = create_extension_client(component=component)

        assert extension_client.package
        assert extension_client.service

    @staticmethod
    @pytest.mark.usefixtures("get_extension_client_class")
    @pytest.mark.usefixtures("mgmt_client")
    def test_component_version_invalid(component, mgmt_client, get_extension_client_class):
        """Test: Invalid component version

        Assertions
        ----------
        - InvalidComponentVersionError exception should be raised
        """

        pytest.raises(
            exceptions.InvalidComponentVersionError,
            get_extension_client_class(component=component),
            mgmt_client,
            version='0.0.0',
            use_latest_metadata=False
        )

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_download_latest_metadata(component, create_extension_client, mocker):
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
        mocker.patch(REQUESTS).side_effect = mock_utils.create_response(
            {},
            conditional=mock_conditions
        )

        extension_client = create_extension_client(
            component=component,
            use_latest_metadata=True
        )

        assert extension_client.version == 'x.x.x'

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_download_latest_metadata_http_error(component, create_extension_client, mocker):
        """Test: Download latest metadata from CDN continues when http error occurs

        Assertions
        ----------
        - Error/exception should be silently caught and logged
        """

        mocker.patch(REQUESTS).side_effect = Exception('Error')

        mock_logger = Mock()
        mocker.patch('f5sdk.logger.Logger.get_logger').return_value = mock_logger

        create_extension_client(component=component, use_latest_metadata=True)

        assert mock_logger.warning.call_count == 1
        error_message = 'Error downloading metadata file'
        assert error_message in mock_logger.warning.call_args_list[0][0][0]

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_install(component, create_extension_client, mocker):
        """Test: install

        Assertions
        ----------
        - install() response should equal:
            {
                'component': '<component>',
                'version': '<component version>'
            }
        """

        extension_client = create_extension_client(
            component=component,
            version=FIXED_INFO[component]['version']
        )

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
        mocker.patch(REQUESTS).side_effect = mock_utils.create_response(
            {},
            conditional=mock_conditions
        )
        mocker.patch(REQUESTS).return_value.json = Mock(
            return_value={
                'id': 'xxxx',
                'status': 'FINISHED',
                'queryResponse': [
                    {
                        'name': FIXED_INFO[component]['name'],
                        'packageName': FIXED_INFO[component]['package_name']
                    }
                ]
            }
        )

        assert extension_client.package.install() == {
            'component': component,
            'version': FIXED_INFO[component]['version']
        }

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_install_with_package_url(component, create_extension_client, mocker, tmpdir):
        """Test: install with package_url

        Assertions
        ----------
        - install() response should equal:
            {
                'component': '<component>',
                'version': '<component version>'
            }
        """

        extension_client = create_extension_client(
            component=component,
            version=FIXED_INFO[component]['version']
        )

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
        mocker.patch(REQUESTS).side_effect = mock_utils.create_response(
            {},
            conditional=mock_conditions
        )
        mocker.patch(REQUESTS).return_value.json = Mock(
            return_value={
                'id': 'xxxx',
                'status': 'FINISHED',
                'queryResponse': [
                    {
                        'name': FIXED_INFO[component]['name'],
                        'packageName': FIXED_INFO[component]['package_name']
                    }
                ]
            }
        )

        mocker.patch("f5sdk.utils.http_utils.download_to_file").side_effect = Mock()
        mocker.patch("f5sdk.constants.TMP_DIR", tmpdir)
        url_remote_file = "https://path/extension.rpm"
        package_name = url_remote_file.split('/')[-1]

        # create dummy file in pytest fixture tmpdir
        tmpdir.join(package_name).write("url_remote_file test")

        assert extension_client.package.install(package_url=url_remote_file) == {
            'component': component,
            'version': FIXED_INFO[component]['version']
            }

        url_local_file = 'file://%s/%s' % (tmpdir, package_name)
        tmpdir.join(package_name).write("url_local_file test")
        assert extension_client.package.install(package_url=url_local_file) == {
            'component': component,
            'version': FIXED_INFO[component]['version']
        }

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_install_package_url_invalid(component, create_extension_client):
        """Test: invalid package_url

        Assertions
        ----------
        - InputRequiredError exception should be raised
        """
        extension_client = create_extension_client(
            component=component,
            version=FIXED_INFO[component]['version']
        )
        pytest.raises(exceptions.InputRequiredError,
                      extension_client.package.install, package_url="invalidUrl")


    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_uninstall(component, create_extension_client, mocker):
        """Test: uninstall

        Assertions
        ----------
        - uninstall() response should equal:
            {
                'component': '<component>',
                'version': '<component version>'
            }
        """

        extension_client = create_extension_client(
            component=component,
            version=FIXED_INFO[component]['version']
        )

        mock_conditions = [
            {
                'type': 'url',
                'value': '/mgmt/shared/iapp/package-management-tasks',
                'response': {
                    'body': {
                        'id': 'xxxx',
                        'status': 'FINISHED',
                        'queryResponse': [
                            {
                                'name': FIXED_INFO[component]['name'],
                                'packageName': FIXED_INFO[component]['package_name']
                            }
                        ]
                    }
                }
            }
        ]
        mocker.patch(REQUESTS).side_effect = mock_utils.create_response(
            {},
            conditional=mock_conditions
        )

        assert extension_client.package.uninstall() == {
            'component': component,
            'version': FIXED_INFO[component]['version']
        }

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_uninstall_any_version(component, create_extension_client, mocker):
        """Test: uninstall (any version)

        Given: Extension client is provided "previous version" which
        is different than the "installed version"

        Assertions
        ----------
        - Package version in uninstall operation should be <component version>
        - uninstall() response should equal:
            {
                'component': '<component>',
                'version': '<component version>'
            }
        """

        extension_client = create_extension_client(
            component=component,
            version=FIXED_INFO[component]['previous_version']
        )

        mock_request = mocker.patch(REQUESTS)
        mock_conditions = [
            {
                'type': 'url',
                'value': '/mgmt/shared/iapp/package-management-tasks',
                'response': {
                    'body': {
                        'id': 'xxxx',
                        'status': 'FINISHED',
                        'queryResponse': [
                            {
                                'name': FIXED_INFO[component]['name'],
                                'packageName': FIXED_INFO[component]['package_name']
                            }
                        ]
                    }
                }
            }
        ]
        mock_request.side_effect = mock_utils.create_response(
            {},
            conditional=mock_conditions
        )

        assert extension_client.package.uninstall() == {
            'component': component,
            'version': FIXED_INFO[component]['version']
        }
        _, kwargs = mock_request.call_args_list[2]
        assert json.loads(kwargs['data'])['packageName'] == FIXED_INFO[component]['package_name']

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_is_installed(component, create_extension_client, mocker):
        """Test: is_installed

        Assertions
        ----------
        - is_installed() response should be a dict
        """

        extension_client = create_extension_client(
            component=component,
            version=FIXED_INFO[component]['version']
        )

        mocker.patch(REQUESTS).return_value.json = Mock(
            return_value={
                'id': 'xxxx',
                'status': 'FINISHED',
                'queryResponse': [
                    {
                        'name': FIXED_INFO[component]['name'],
                        'packageName': FIXED_INFO[component]['package_name']
                    }
                ]
            }
        )

        is_installed = extension_client.package.is_installed()
        assert is_installed['installed']
        assert is_installed['installed_version'] == FIXED_INFO[component]['version']
        assert is_installed['latest_version'] != ''

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_is_installed_similar_package(component, create_extension_client, mocker):
        """Test: is_installed with second package containing component name in it

        Assertions
        ----------
        - is_installed() response should have installed=true and correct version
        """

        extension_client = create_extension_client(
            component=component,
            version=FIXED_INFO[component]['version']
        )

        mocker.patch(REQUESTS).return_value.json = Mock(
            return_value={
                'id': 'xxxx',
                'status': 'FINISHED',
                'queryResponse': [
                    {
                        'name': FIXED_INFO[component]['name'],
                        'packageName': FIXED_INFO[component]['package_name']
                    },
                    {
                        'name': '{}-foo'.format(FIXED_INFO[component]['name']),
                        'packageName': '{}-foo-x.x.x.noarch'.format(FIXED_INFO[component]['name'])
                    }
                ]
            }
        )

        is_installed = extension_client.package.is_installed()
        assert is_installed['installed']
        assert is_installed['installed_version'] == FIXED_INFO[component]['version']

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_failed_task_status(component, create_extension_client, mocker):
        """Test: is_installed with failed RPM task status

        Assertions
        ----------
        - Exception exception should be raised
        """

        extension_client = create_extension_client(component=component)

        mocker.patch(REQUESTS).return_value.json = Mock(
            return_value={
                'id': 'xxxx',
                'status': 'FAILED'
            }
        )

        pytest.raises(Exception, extension_client.package.is_installed)

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_is_installed_two_digit_version(component, create_extension_client, mocker):
        """Test: is_installed where package name major version contains two digits

        Note: This test should live outside the generic tests perhaps...

        Assertions
        ----------
        - is_installed() installed_version response should be correctly parsed
        """

        extension_client = create_extension_client(component=component)

        mocker.patch(REQUESTS).return_value.json = Mock(
            return_value={
                'id': 'xxxx',
                'status': 'FINISHED',
                'queryResponse': [
                    {
                        'name': FIXED_INFO[component]['name'],
                        'packageName': FIXED_INFO[component]['package_name']
                    }
                ]
            }
        )

        is_installed = extension_client.package.is_installed()
        assert is_installed['installed_version'] == FIXED_INFO[component]['version']

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_is_not_installed(component, create_extension_client, mocker):
        """Test: is_not_installed

        Assertions
        ----------
        - is_installed() response should be a dict
        """

        extension_client = create_extension_client(component=component)

        mocker.patch(REQUESTS).return_value.json = Mock(
            return_value={
                'id': 'xxxx',
                'status': 'FINISHED',
                'queryResponse': [
                    {
                        'name': '',
                        'packageName': ''
                    }
                ]
            }
        )

        is_installed = extension_client.package.is_installed()
        assert not is_installed['installed']
        assert is_installed['installed_version'] == ''
        assert is_installed['latest_version'] != ''

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_list_versions(component, create_extension_client):
        """Test: list extension versions

        Assertions
        ----------
        - list_versions() response should be a list
        """

        extension_client = create_extension_client(component=component)
        version_list = extension_client.package.list_versions()
        assert FIXED_INFO[component]['version'] in version_list

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_show(component, create_extension_client, mocker):
        """Test: show

        Assertions
        ----------
        - show() response should equal requests response
        """

        extension_client = create_extension_client(component=component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.show() == mock_response

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_create(component, create_extension_client, mocker):
        """Test: create

        Assertions
        ----------
        - create() response should equal requests response
        """

        extension_client = create_extension_client(component=component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.create(config={'config': 'foo'}) == mock_response

    @pytest.mark.usefixtures("create_extension_client")
    def test_create_config_file(self, component, create_extension_client, mocker):
        """Test: create with config file

        Assertions
        ----------
        - create() response should equal requests response
        """

        extension_client = create_extension_client(component=component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        config_file = path.join(self.test_tmp_dir, 'config.json')
        with open(config_file, 'w') as _f:
            _f.write(json.dumps({'config': 'foo'}))

        assert extension_client.service.create(config_file=config_file) == mock_response

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_create_no_config(component, create_extension_client):
        """Test: create with no config provided

        Assertions
        ----------
        - InputRequiredError exception should be raised
        """

        extension_client = create_extension_client(component=component)

        pytest.raises(exceptions.InputRequiredError, extension_client.service.create)

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_create_async(component, create_extension_client, mocker):
        """Test: create async response

        Assertions
        ----------
        - create() response should equal task requests response
        - make_request() should be called twice
        - make_request() second call uri should equal task uri
        """

        extension_client = create_extension_client(component=component)

        mock_response = {'foo': 'bar'}
        make_request_mock = mocker.patch(
            'f5sdk.utils.http_utils.make_request',
            side_effect=[({'selfLink': 'https://localhost/foo/1234'}, 202), (mock_response, 200)]
        )

        response = extension_client.service.create(config={'foo': 'bar', 'async': True})
        assert response == mock_response
        assert make_request_mock.call_count == 2
        args, _ = make_request_mock.call_args_list[1]
        assert args[1] == '/foo/1234'

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_is_available(component, create_extension_client, mocker):
        """Test: is_available

        Assertions
        ----------
        - is_available() response should be boolean (True)
        """

        extension_client = create_extension_client(component=component)

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={'message': 'success'})

        assert extension_client.service.is_available()

    @staticmethod
    @pytest.mark.usefixtures("create_extension_client")
    def test_show_info(component, create_extension_client, mocker):
        """Test: show_info

        Assertions
        ----------
        - show_info() response should be info endpoint API response
        """

        extension_client = create_extension_client(component=component)

        mocker.patch(REQUESTS).return_value.json = Mock(return_value={'version': 'x.x.x.x'})

        assert extension_client.service.show_info() == {'version': 'x.x.x.x'}


class TestAS3Client(object):
    """Test AS3 Client - performs any component specific tests """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.component = 'as3'

    @pytest.mark.usefixtures("create_extension_client")
    def test_uninstall_with_dependency(self, create_extension_client, mocker):
        """Test: uninstall with existing dependency

        Assertions
        ----------
        - uninstall() should log a warning about existing dependency
        """

        mock_conditions = [
            {
                'type': 'url',
                'value': '/mgmt/shared/iapp/package-management-tasks',
                'response': {
                    'body': {
                        'id': 'xxxx',
                        'status': 'FINISHED',
                        'queryResponse': [
                            {
                                'name': FIXED_INFO[self.component]['name'],
                                'packageName': 'f5-appsvcs-3.9.0-3.noarch'
                            }
                        ]
                    }
                }
            }
        ]
        mocker.patch(REQUESTS).side_effect = mock_utils.create_response(
            {},
            conditional=mock_conditions
        )
        mock_logger = Mock()
        mocker.patch('f5sdk.logger.Logger.get_logger').return_value = mock_logger

        extension_client = create_extension_client(component=self.component)
        extension_client.package.uninstall()

        assert mock_logger.warning.call_count == 1
        logged_message = mock_logger.warning.call_args_list[0][0][0]
        assert 'A component package dependency has not been removed' in logged_message
        assert 'See documentation for more details' in logged_message

    @pytest.mark.usefixtures("create_extension_client")
    def test_delete(self, create_extension_client, mocker):
        """Test: delete

        Assertions
        ----------
        - delete() response should equal requests response
        """

        extension_client = create_extension_client(component=self.component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.delete() == mock_response


class TestDOClient(object):
    """Test DO Client - performs any component specific tests """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.component = 'do'

    @pytest.mark.usefixtures("create_extension_client")
    def test_do_show_inspect(self, create_extension_client, mocker):
        """Test: show_inspect

        Assertions
        ----------
        - show_inspect() response should be inspect endpoint API response
        """

        extension_client = create_extension_client(component=self.component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.show_inspect() == mock_response

    @pytest.mark.usefixtures("create_extension_client")
    def test_do_show_inspect_query_parameters(self, create_extension_client, mocker):
        """Test: show_inspect(**kwargs) query parameters with a GET request to the /inspect endpoint

        For example
        https://MGMT_IP/mgmt/shared/declarative-onboarding/inspect?targetHost=X.X.X.X
        &targetPort=443&targetUsername=admin&targetPassword=admin

        Assertions
        ----------
        - HTTP request uri should contain the query parameters
        - show_inspect() response should be mocked response
        """

        extension_client = create_extension_client(component=self.component)

        inspect_kwargs = {
            'query_parameters': {
                'targetHost': '192.0.2.1',
                'targetPort': 443,
                'targetUsername': 'admin',
                'targetPassword': 'admin'
            }
        }
        mock_request = mocker.patch(REQUESTS)
        mock_request.return_value.json = Mock(return_value={})
        type(mock_request.return_value).status_code = PropertyMock(return_value=200)

        show_inspect_response = extension_client.service.show_inspect(**inspect_kwargs)
        args, _ = mock_request.call_args
        query_params = http_utils.parse_url(args[1])['query']

        for key in inspect_kwargs['query_parameters']:
            assert '{}={}'.format(key, inspect_kwargs['query_parameters'][key]) in query_params
        assert show_inspect_response == {}


class TestCFClient(object):
    """Test CF Client - performs any component specific tests """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.component = 'cf'

    @pytest.mark.usefixtures("create_extension_client")
    def test_cf_show_failover(self, create_extension_client, mocker):
        """Test: show_failover

        Assertions
        ----------
        - show_failover() response should be trigger endpoint API response
        """

        extension_client = create_extension_client(component=self.component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.show_trigger() == mock_response

    @pytest.mark.usefixtures("create_extension_client")
    def test_cf_show_inspect(self, create_extension_client, mocker):
        """Test: show_inspect

        Assertions
        ----------
        - show_inspect() response should be inspect endpoint API response
        """

        extension_client = create_extension_client(component=self.component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.show_inspect() == mock_response

    @pytest.mark.usefixtures("create_extension_client")
    def test_cf_trigger_failover(self, create_extension_client, mocker):
        """Test: show_inspect

        Assertions
        ----------
        - trigger() response should be trigger endpoint API response
        """

        extension_client = create_extension_client(component=self.component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.trigger() == mock_response

    @pytest.mark.usefixtures("create_extension_client")
    def test_cf_reset(self, create_extension_client, mocker):
        """Test: reset

        Assertions
        ----------
        - reset() response should be reset endpoint API response
        """

        extension_client = create_extension_client(component=self.component)

        mock_response = {'message': 'success'}
        mocker.patch(REQUESTS).return_value.json = Mock(return_value=mock_response)

        assert extension_client.service.reset() == mock_response
