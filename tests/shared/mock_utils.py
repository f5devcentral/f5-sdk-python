"""Mock utility module for test framework """

# unittest imports
from ..global_test_imports import Mock


class MockRequestsResponse:
    """ Mock requests response instance """
    def __init__(self, body):
        """ Init """
        self.body = body
        self.status_code = None
        self.reason = None

    @staticmethod
    def raise_for_status():
        """ Mock function """
        return True

    def json(self):
        """ Mock function """
        return self.body

    @staticmethod
    def ok():  # pylint: disable=invalid-name
        """ Mock function """
        return True

    def iter_content(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ Mock function """
        return [self.body]


class ExecCommand(object):
    """ Mock exec_command response instance """

    def __init__(self, response):
        """ Init """
        self.response = response

    def read(self):
        """ Mock function """
        return self.response.encode('ascii')


def create_response(response_body, **kwargs):
    """Create mock requests.request response instance

    Parameters
    ----------
    response_body : str
        response body to use
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    conditional : list
        list containing 1+ dicts to allow for conditional mock response behavior::
            [
                {
                    'type': 'url',
                    'value': 'github.com',
                    'response': {
                        'body': 'foo'
                    }
                }
            ]

    Returns
    -------
    obj
        mocked requests.request response instance
    """

    c_response = kwargs.pop('conditional', None)

    def _func(*a, **k):  # pylint: disable=unused-argument
        """ Function """
        url = a[1]

        if c_response:
            # future format types: 'type': 'method', ...
            for item in c_response:
                if item['type'] == 'url' and item['value'] in url:
                    # gotcha, custom return
                    return MockRequestsResponse(item['response']['body'])
            raise Exception('No condition met - URL: %s conditions: %s' % (url, c_response))

        # standard return
        return MockRequestsResponse(response_body)
    return _func


def create_ssh_client(mock, command_response, **kwargs):
    """Create mock paramiko SSHClient instance

    Parameters
    ----------
    mock : obj
        mocked object
    command_response : str
        command response to use
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    connect_raise : obj
        exception class to raise when mock.connect is called
    stderr : str
        string to provide for stderr in exec_command response

    Returns
    -------
    obj
        mocked ssh client instance
    """

    connect_raise = kwargs.pop('connect_raise', None)
    stderr = kwargs.pop('stderr', '')  # default should be empty string

    instance = mock.return_value
    if connect_raise:
        instance.connect.side_effect = connect_raise

    instance.exec_command = Mock(
        return_value=(
            ExecCommand(''),
            ExecCommand(command_response),
            ExecCommand(stderr))
    )

    return instance
