""" Test BIG-IP module """
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError:
    # python 2.x support
    from mock import Mock, MagicMock, patch

# SDK imports
from f5cloudsdk.bigip.toolchain import ToolChainClient
# test imports
from ...shared import utils
from . import utils as BigIpUtils

TOKEN = 'mytoken'

class TestPackage(unittest.TestCase):
    """ Test Case """

class TestService(unittest.TestCase):
    """ Test Case """

    @patch('requests.request')
    def test_bigip_toolchain_service_basic(self, mock_request):
        """ Test """
        mock_resp = {'message': 'success'}
        mock_request.side_effect = utils.create_mock_response(mock_resp)

        device = BigIpUtils.get_mgmt_client(token=TOKEN)

        toolchain = ToolChainClient(device, 'as3')
        response = toolchain.service.show()
        assert mock_request.called
        assert mock_resp == response
