""" Test provider module """

# project imports
from f5cloudsdk import provider

CREDS_RESPONSE = 'foo'


class TestProvider(object):
    """Test Class: provider module """

    def test_azure_provider_client(self, mocker):
        """Test: azure provider client init

        Assertions
        ----------
        - Provider client credentials attribute equals mocked return
        """

        mocker.patch(
            'f5cloudsdk.provider.azure.ServicePrincipalCredentials',
            return_value=CREDS_RESPONSE
        )

        provider_client = provider.azure.ProviderClient(
            client_id='client_id',
            tenant_id='tenant_id',
            secret='secret',
            subscription_id='subscription_id'
        )

        assert provider_client.credentials == CREDS_RESPONSE

    def test_aws_provider_client(self, mocker):
        """Test: aws provider client init

        Assertions
        ----------
        - Provider client session attribute equals mocked return
        """

        mocker.patch('f5cloudsdk.provider.aws.Session', return_value=CREDS_RESPONSE)

        provider_client = provider.aws.ProviderClient(
            access_key='id',
            secret_key='secret',
            region_name='us-west-1'
        )

        assert provider_client.session == CREDS_RESPONSE
