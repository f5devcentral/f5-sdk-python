"""F5 Cloud SDK package

    Example -- Basic::

        from f5cloudsdk.bigip import ManagementClient
        from f5cloudsdk.bigip.toolchain import ToolChainClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')
        as3 = ToolChainClient(device, 'as3')
        # install AS3 package
        as3.package.install()
"""
