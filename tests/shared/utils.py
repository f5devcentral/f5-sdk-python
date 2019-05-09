"""Utility module for test framework """

class MockRequestsResponse:
    """ Mock requests response instance """
    def __init__(self, body):
        """ Init """
        self.body = body

    def raise_for_status(self):
        """ Mock function """
        return True

    def json(self):
        """ Mock function """
        return self.body

    def ok(self):
        """ Mock function """
        return True

    def iter_content(self, *args, **kwargs):
        """ Mock function """
        return [self.body]

class MockSocket:
    """ Mock socket.socket object """
    def __init__(self, **kwargs):
        """ Init """
        self.connect_raise = kwargs.pop('connect_raise', None)

    def settimeout(self, *args):
        """ Mock function """

    def connect(self, *args):
        """ Mock function """
        if self.connect_raise:
            raise self.connect_raise
        return True

def create_mock_response(response_body, **kwargs):
    """Create mock requests.request response instance

    Parameters
    ----------
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

    def _func(*a, **k): # pylint: disable=unused-argument
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

def create_mock_socket(**kwargs):
    """Create mock socket.socket instance

    Parameters
    ----------
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    connect_raise : obj
        exception class to raise when mock is called (passed directly to Mock init)

    Returns
    -------
    obj
        mocked socket instance
    """

    def _func(*a, **k): # pylint: disable=unused-argument
        """ Function """
        return MockSocket(**kwargs)
    return _func
