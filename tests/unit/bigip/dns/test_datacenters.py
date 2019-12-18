""" Test BIG-IP DNS datacenters client """

from f5sdk.bigip.dns import DataCentersClient

from ....global_test_imports import pytest
from ....shared import constants
from ... import utils

REQ = constants.MOCK['requests']


class TestDataCentersClient(object):
    """Test"""

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = DataCentersClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )
