"""Helpful decorators """

def check_auth(function):
    """Checks authentication

    Parameters
    ----------
    function: func
        a function to decorate with authentication check

    Returns
    -------
    func
        a decorated function
    """

    def wrapper(self, *args, **kwargs):
        if self.token is None:
            raise Exception('Device authentication required')
        return function(self, *args, **kwargs)
    return wrapper
