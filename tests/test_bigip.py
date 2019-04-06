""" Test bigip """
try:
    from unittest import mock
except ImportError:
    import mock # python 2.x support

from f5cloudsdk.bigip import ManagementClient

class MockRequestsResponse:
    """ Mock requests lib response object """
    def __init__(self, body):
        self.body = body

    def json(self):
        """ Mock json function """
        return self.body

def mock_get_token(*args, **kwargs):
    """ Mock get token requests call """
    response_body = {
        'token': {
            'token': 'foo'
        }
    }
    return MockRequestsResponse(response_body)

@mock.patch('requests.post', side_effect=mock_get_token)
def test_bigip_mgmt_client(*args):
    """ Test f5cloudsdk.bigip """
    user = 'admin'
    password = 'admin'
    device = ManagementClient('192.0.2.1', user=user, password=password)
    assert device.user == user
