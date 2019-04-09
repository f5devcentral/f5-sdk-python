""" Module for BIG-IP toolchain service configuration """

class Operation():
    """ Toolchain service operation client """
    def __init__(self, client, component):
        self.client = client
        self.component = component

    def create(self, **kwargs):
        """ Create toolchain service """
        component = self.component
        file = kwargs.pop('file', '')

        return {'component': component, 'file': file} # temp
