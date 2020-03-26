"""Module for BIG-IP extension component service configuration

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.extension import AS3Client

        mgmt_client = ManagementClient('192.0.2.10', user='admin', password='admin')
        extension_client = AS3Client(mgmt_client)

        # configure AS3
        extension_client.service.create(config_file='./decl.json')

    Example - Show::

        extension_client.service.show()

    Example - Delete::

        extension_client.service.delete()

    Example - Is Available::

        extension_client.service.is_available()

    Example - Show Info::

        extension_client.service.show_info()

    Example - Show Inspect (DO)::

        extension_client = DOClient(device)
        extension_client.service.show_inspect()

"""

from .operation import OperationClient

__all__ = [
    'OperationClient'
]
