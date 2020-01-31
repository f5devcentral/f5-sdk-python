"""F5 SDK (Python)

    Example -- Basic::

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
"""
