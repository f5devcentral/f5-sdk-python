""" Test BIG-IQ licensing pool member management """

from f5cloudsdk.bigiq.licensing.pools import \
    RegKeyClient, RegKeyOfferingsClient, RegKeyOfferingMembersClient

from ....global_test_imports import pytest
from ... import utils


class TestRegKeyClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = RegKeyClient(mgmt_client)

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )


class TestRegKeyOfferingsClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = RegKeyOfferingsClient(mgmt_client, pool_name='foo')

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )


class TestRegKeyOfferingMembersClient(object):
    """Test"""

    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(self, mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        client = RegKeyOfferingMembersClient(
            mgmt_client,
            pool_name='foo',
            offering_name='bar'
        )

        utils.validate_crud_operations(
            client,
            mocker=mocker
        )
