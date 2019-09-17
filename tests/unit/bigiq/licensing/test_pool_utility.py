""" Test BIG-IQ licensing pool member management """

from f5cloudsdk.bigiq.licensing.pool import \
    UtilityClient, UtilityOfferingsClient, UtilityOfferingMembersClient

from ....global_test_imports import pytest
from ... import utils


class TestUtilityClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = UtilityClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )


class TestUtilityOfferingsClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = UtilityOfferingsClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )


class TestUtilityOfferingMembersClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = UtilityOfferingMembersClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )
