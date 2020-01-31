"""Python module for BIG-IP extension component configuration, including AS3, DO and TS

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.extension import ExtensionClient
        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        as3 = ExtensionClient(device, 'as3')
        # install AS3 package
        as3.package.install()
        # check service is available
        as3.service.is_available()
        # configure AS3
        as3.service.create(config_file='./decl.json')

    Example - Specify Component Type::

        do = ExtensionClient(device, 'do')
        ts = ExtensionClient(device, 'ts')

    Example - Specify Component Version::

        as3 = ExtensionClient(device, 'as3', version='3.9.0')
"""

from .extension import ExtensionClient

__all__ = [
    'ExtensionClient'
]
