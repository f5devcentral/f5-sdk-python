""" Test fixtures """

from f5sdk.bigip.extension import ExtensionClient

from ....global_test_imports import pytest


@pytest.fixture
@pytest.mark.usefixtures("mgmt_client")
def extension_client(mgmt_client):
    """ Test fixture: create mgmt client """

    return ExtensionClient(mgmt_client, 'as3', use_latest_metadata=False)
