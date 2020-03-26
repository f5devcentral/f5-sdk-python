""" Test fixtures """

import importlib

from ....global_test_imports import pytest


@pytest.fixture(name="get_extension_client_class")
def get_extension_client_class_fixture():
    """ Test fixture: Get Extension Client Class (Factory)"""

    def _func(**kwargs):
        component = kwargs.pop('component', 'as3')

        module = importlib.import_module('f5sdk.bigip.extension')

        if component == 'as3':
            extension_client_class = getattr(module, 'AS3Client')
        elif component == 'do':
            extension_client_class = getattr(module, 'DOClient')
        elif component == 'ts':
            extension_client_class = getattr(module, 'TSClient')
        elif component == 'cf':
            extension_client_class = getattr(module, 'CFClient')
        else:
            raise Exception('Unknown component: {}'.format(component))

        return extension_client_class

    return _func

@pytest.fixture(name="create_extension_client")
@pytest.mark.usefixtures("get_extension_client_class")
@pytest.mark.usefixtures("mgmt_client")
def create_extension_client_fixture(mgmt_client, get_extension_client_class):
    """ Test fixture: Create Extension Client (Factory)"""

    def _func(**kwargs):
        component = kwargs.pop('component', 'as3')
        version = kwargs.pop('version', None)
        use_latest_metadata = kwargs.pop('use_latest_metadata', False)

        # define extension client kwargs
        kwargs = {}
        if use_latest_metadata:
            kwargs['use_latest_metadata'] = use_latest_metadata
        if version is not None:
            kwargs['version'] = version

        # get extension client class and instantiate
        extension_client_class = get_extension_client_class(component=component)
        return extension_client_class(mgmt_client, **kwargs)

    return _func
