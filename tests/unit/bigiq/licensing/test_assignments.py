""" Test BIG-IQ licensing assignment """

from f5sdk.bigiq.licensing import AssignmentClient

from ....global_test_imports import pytest
from ....shared import constants
from ... import utils

REQ = constants.MOCK['requests']


class TestAssignmentClient(object):
    """Test"""

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = AssignmentClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker,
            methods=['list']
        )
