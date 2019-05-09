""" Exceptions used throughout this package """

class AuthRequiredError(Exception):
    """ Error raised when authentication is required """

class InputRequiredError(Exception):
    """ Error raised if input is required """

class InvalidComponentError(Exception):
    """ Error raised if invalid component is provided """

class InvalidComponentVersionError(Exception):
    """ Error raised if invalid component version is provided """
