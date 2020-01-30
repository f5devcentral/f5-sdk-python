""" Test fixtures """

from f5sdk.bigip.toolchain import ToolChainClient

from ....global_test_imports import pytest


@pytest.fixture
@pytest.mark.usefixtures("mgmt_client")
def toolchain_client(mgmt_client):
    """ Test fixture: create mgmt client """

    return ToolChainClient(mgmt_client, 'as3', use_latest_metadata=False)
