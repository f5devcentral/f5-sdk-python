""" Test provider module """
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError:
    # python 2.x support
    from mock import Mock, MagicMock, patch

from f5cloudsdk.provider import azure, aws

class TestProvider(unittest.TestCase):
    """ Test case """

    @patch('f5cloudsdk.provider.azure.ProviderClient._get_credentials', return_value='creds')
    def test_azure_provider_client_basic(self, mock_get_creds):
        """ Test azure provider client (basic) """

        provider_client = azure.ProviderClient(
            client_id='client_id',
            tenant_id='tenant_id',
            secret='secret',
            subscription_id='subscription_id')

        assert mock_get_creds.called
        assert provider_client.credentials == 'creds'

    @patch('f5cloudsdk.provider.aws.ProviderClient._get_session', return_value='session')
    def test_aws_provider_client_basic(self, mock_get_creds):
        """ Test aws provider client (basic) """

        provider_client = aws.ProviderClient(
            access_key='id',
            secret_key='secret',
            region_name='us-west-1')

        assert mock_get_creds.called
        assert provider_client.session == 'session'
