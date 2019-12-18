"""Python module containing helpful decorators

Note
----

Wraps makes doc string available for decorated functions, this is used
during documentation engine retrieval
"""

from functools import wraps

from f5sdk.exceptions import AuthRequiredError
from f5sdk import constants


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

    @wraps(function)
    def _wrapper(self, *args, **kwargs):
        if self.token is None:
            raise AuthRequiredError('Device authentication required')
        return function(self, *args, **kwargs)
    return _wrapper


def add_auth_header(function):
    """Add authentication header

    Parameters
    ----------
    function : function
        a function to decorate with authentication header

    Returns
    -------
    function
        a decorated function
    """

    @wraps(function)
    def _wrapper(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers'].update({
            constants.F5_AUTH_TOKEN_HEADER: self.token
        })
        return function(self, *args, **kwargs)
    return _wrapper
