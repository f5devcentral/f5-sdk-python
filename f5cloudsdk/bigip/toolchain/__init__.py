"""Python module for BIG-IP toolchain component configuration, including AS3, DO and TS

    Example - Basic::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.toolchain import ToolChainClient
        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        as3 = ToolChainClient(device, 'as3')
        # install AS3 package
        as3.package.install()
        # check service is available
        as3.service.is_available()
        # configure AS3
        as3.service.create(config_file='./decl.json')

    Example - Specify Component Type::

        do = ToolChainClient(device, 'do')
        ts = ToolChainClient(device, 'ts')

    Example - Specify Component Version::

        as3 = ToolChainClient(device, 'as3', version='3.9.0')
"""

from .toolchain import ToolChainClient

__all__ = [
    'ToolChainClient'
]
