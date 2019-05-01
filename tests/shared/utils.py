"""Utility module for test framework """

class MockRequestsResponse:
    """ Mock requests response object """
    def __init__(self, body):
        self.body = body

    def raise_for_status(self):
        """ Mock raise_for_status function """
        return True

    def json(self):
        """ Mock json function """
        return self.body


def create_mock_response(response_body):
    """ Create mock response function """

    def _func(*args, **kwargs): # pylint: disable=unused-argument
        """ Function """
        return MockRequestsResponse(response_body)
    return _func
