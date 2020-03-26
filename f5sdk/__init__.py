"""F5 SDK (Python)

    Example -- Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.extension import AS3Client

        mgmt_client = ManagementClient('192.0.2.10', user='admin', password='admin')
        extension_client = AS3Client(mgmt_client, 'as3')

        # install AS3 package
        extension_client.package.install()
        # check service is available
        extension_client.service.is_available()
        # configure AS3
        extension_client.service.create(config_file='./decl.json')
"""
