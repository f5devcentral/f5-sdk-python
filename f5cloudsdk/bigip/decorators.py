""" Helper decorators for BIG-IP module """

def check_auth(function):
    """ Decorator function to check authentication """
    # TODO: need to support refreshing the token - here or elsewhere
    def wrapper(self, *args, **kwargs):
        if self.token is None:
            raise Exception('Device authentication required')
        return function(self, *args, **kwargs)
    return wrapper
