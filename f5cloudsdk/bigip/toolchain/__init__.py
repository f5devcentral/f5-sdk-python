""" Module for BIG-IP toolchain configuration

    Example(s):

    ## Example: Basic
    from f5cloudsdk.bigip import ManagementClient
    from f5cloudsdk.bigip.toolchain import ToolChainClient
    device = ManagementClient('192.0.2.10', user='admin', password='admin')

    as3 = ToolChainClient(device, 'as3')
    # install AS3 package
    as3.package.install()
    # create AS3 service
    as3.service.create('./my_local_decl')

"""

from .package import Operation as packageClient
from .service import Operation as serviceClient

class ToolChainClient():
    """ Toolchain client class for BIG-IP """
    def __init__(self, client, component):
        self.client = client
        self.component = component

    @property
    def package(self):
        """ Package """
        return packageClient(self.client, self.component)

    @property
    def service(self):
        """ Service """
        return serviceClient(self.client, self.component)
