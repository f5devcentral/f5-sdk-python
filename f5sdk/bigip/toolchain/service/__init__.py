"""Module for BIG-IP toolchain component service configuration

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.toolchain import ToolChainClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        as3 = ToolChainClient(device, 'as3')
        # configure AS3
        as3.service.create(config_file='./decl.json')

    Example - Show::

        as3.service.show()

    Example - Delete::

        as3.service.delete()

    Example - Is Available::

        as3.service.is_available()
"""

from .operation import OperationClient

__all__ = [
    'OperationClient'
]
