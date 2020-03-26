"""Module for BIG-IP extension component package configuration

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.extension import AS3Client

        mgmt_client = ManagementClient('192.0.2.10', user='admin', password='admin')
        extension_client = AS3Client(mgmt_client)

        # install AS3 package
        as3.package.install()

    Example - Uninstall::

        extension_client.package.uninstall()

    Example - Check if extension component is installed::

        extension_client.package.is_installed()
"""

from .operation import OperationClient

__all__ = [
    'OperationClient'
]
