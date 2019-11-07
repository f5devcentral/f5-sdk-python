""" Test BIG-IP DNS datacenters client """

from f5cloudsdk.bigip.dns import VirtualServersClient

from ....global_test_imports import pytest
from ....shared import constants
from ... import utils

REQ = constants.MOCK['requests']


class TestVirtualServersClient(object):
    """Test"""

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = VirtualServersClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )
