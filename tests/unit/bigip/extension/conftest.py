""" Test fixtures """

from f5sdk.bigip.extension import ExtensionClient

from ....global_test_imports import pytest


@pytest.fixture
@pytest.mark.usefixtures("mgmt_client")
def extension_client(mgmt_client):
    """ Test fixture: create as3 extension client """

    return ExtensionClient(mgmt_client, 'as3')


@pytest.fixture
@pytest.mark.usefixtures("mgmt_client")
def ts_extension_client(mgmt_client):
    """ Test fixture: create ts extension client """

    return ExtensionClient(mgmt_client, 'ts')

@pytest.fixture
@pytest.mark.usefixtures("mgmt_client")
def cf_extension_client(mgmt_client):
    """ Test fixture: create as3 extension client """

    return ExtensionClient(mgmt_client, 'cf')
