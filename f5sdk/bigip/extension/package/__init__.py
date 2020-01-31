"""Module for BIG-IP extension component package configuration

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.extension import ExtensionClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        as3 = ExtensionClient(device, 'as3')
        # install AS3 package
        as3.package.install()

    Example - Uninstall::

        as3.package.uninstall()

    Example - Check if extension component is installed::

        as3.package.is_installed()
"""

from .operation import OperationClient

__all__ = [
    'OperationClient'
]
