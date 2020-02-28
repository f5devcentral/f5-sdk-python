"""Module for BIG-IP extension component service configuration

    Example - Basic::
        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.extension import ExtensionClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        as3 = ExtensionClient(device, 'as3')

        # configure AS3
        as3.service.create(config_file='./decl.json')

    Example - Show::

        as3.service.show()

    Example - Delete::

        as3.service.delete()

    Example - Is Available::

        as3.service.is_available()

    Example - Show Info::

        as3.service.show_info()

    Example - Show Inspect (specific to DO component)::

        do_client = ExtensionClient(device, 'do')
        do_client.service.show_inspect()

"""

from .operation import OperationClient

__all__ = [
    'OperationClient'
]
