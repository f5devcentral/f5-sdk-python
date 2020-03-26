"""Module for BIG-IP extension component configuration, including AS3, DO, TS and CF

    Example - Basic::

        from f5sdk.bigip import ManagementClient
        from f5sdk.bigip.extension import AS3Client, DOClient, TSClient, CFClient

        mgmt_client = ManagementClient('192.0.2.10', user='admin', password='admin')
        extension_client = AS3Client(mgmt_client)

        # install AS3 package
        extension_client.package.install()
        # check service is available
        extension_client.service.is_available()
        # configure AS3
        extension_client.service.create(config_file='./decl.json')

    Example - Specify Component::

        do_client = DOClient(mgmt_client)
        ts_client = TSClient(mgmt_client)
        cf_client = CFClient(mgmt_client)

    Example - Specify Component Version::

        extension_client = AS3Client(device, version='3.9.0')
"""

from .extension_as3 import AS3Client
from .extension_do import DOClient
from .extension_ts import TSClient
from .extension_cf import CFClient

__all__ = [
    'AS3Client',
    'DOClient',
    'TSClient',
    'CFClient'
]
