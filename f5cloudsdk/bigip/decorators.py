"""Helpful decorators """

def check_auth(function):
    """Checks authentication

    Parameters
    ----------
    function : function
        a function to decorate with authentication check

    Returns
    -------
    function
        a decorated function
    """

    def _wrapper(self, *args, **kwargs):
        if self.token is None:
            raise Exception('Device authentication required')
        return function(self, *args, **kwargs)
    return _wrapper
