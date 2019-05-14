""" Test provider module """

## unittest imports ##
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError:
    # python 2.x support
    from mock import Mock, MagicMock, patch

## project imports ##
from f5cloudsdk import provider

class TestProvider(unittest.TestCase):
    """Test Class: provider module """

    @patch('f5cloudsdk.provider.azure.ServicePrincipalCredentials', return_value='credentials')
    def test_azure_provider_client(self, mock_get_creds):
        """Test: azure provider client init

        Assertions
        ----------
        - Mocked _get_credentials should be called
        - Provider client credentials attribute equals mocked return
        """

        provider_client = provider.azure.ProviderClient(
            client_id='client_id',
            tenant_id='tenant_id',
            secret='secret',
            subscription_id='subscription_id'
        )

        assert mock_get_creds.called
        assert provider_client.credentials == 'credentials'

    @patch('f5cloudsdk.provider.aws.Session', return_value='session')
    def test_aws_provider_client(self, mock_get_session):
        """Test: aws provider client init

        Assertions
        ----------
        - Mocked _get_session should be called
        - Provider client session attribute equals mocked return
        """

        provider_client = provider.aws.ProviderClient(
            access_key='id',
            secret_key='secret',
            region_name='us-west-1'
        )

        assert mock_get_session.called
        assert provider_client.session == 'session'
