""" Exceptions used throughout this package """


class AuthRequiredError(Exception):
    """ Error raised when authentication is required """


class InputRequiredError(Exception):
    """ Error raised if input is required """


class InvalidComponentError(Exception):
    """ Error raised if invalid component is provided """


class InvalidComponentVersionError(Exception):
    """ Error raised if invalid component version is provided """


class HTTPError(Exception):
    """ Error raised http error occurs """


class FileLoadError(Exception):
    """ Error raised if file load error occurs """


class SSHCommandStdError(Exception):
    """ Error raised if ssh client command response contains stderr """


class DeviceReadyError(Exception):
    """ Error raised if device ready check fails """


class RetryInterruptedError(Exception):
    """ Error raised if method retry is intentionally interrupted """


class InvalidAuthError(Exception):
    """ Error raised if authentication fails """
