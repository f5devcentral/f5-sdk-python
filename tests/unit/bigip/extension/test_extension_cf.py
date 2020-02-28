""" Test BIG-IP module """

import tempfile
import shutil

from ....global_test_imports import pytest, Mock
from ....shared import constants

REQ = constants.MOCK['requests']


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

        assert cf_extension_client.service.show_trigger() == sample_return_value

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

        assert cf_extension_client.service.show_info() == sample_return_value

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
