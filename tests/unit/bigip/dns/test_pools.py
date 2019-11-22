""" Test BIG-IP DNS pools client """

from f5cloudsdk.bigip.dns import PoolsClient

from ....global_test_imports import pytest
from ....shared import constants
from ... import utils

REQ = constants.MOCK['requests']


class TestPoolsClient(object):
    """Test"""

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = PoolsClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )
