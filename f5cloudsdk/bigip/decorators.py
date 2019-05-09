"""Python module containing helpful decorators """

from functools import wraps

from f5cloudsdk.exceptions import AuthRequiredError

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

    # wraps includes docstring for documentation engine retrieval
    @wraps(function)
    def _wrapper(self, *args, **kwargs):
        if self.token is None:
            raise AuthRequiredError('Device authentication required')
        return function(self, *args, **kwargs)
    return _wrapper
