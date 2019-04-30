"""Module for provider(s)

    Example -- Basic (Azure)::

        from f5cloudsdk.provider.azure import ProviderClient

        provider_client = ProviderClient(
            client_id='id',
            tenant_id='id',
            secret='secret',
            subscription_id='')
        # list virtual machines - filter by tag
        virtual_machines = provider_client.virtual_machines.list(filter_tag='f5devicetype:bigip')

    Example -- Basic (AWS)::

        from f5cloudsdk.provider.aws import ProviderClient

        provider_client = ProviderClient(
            access_key='id',
            secret_key='secret',
            region_name='us-west-1')
        # list virtual machines - filter by tag
        virtual_machines = provider_client.virtual_machines.list(filter_tag='f5devicetype:bigip')

    Example -- Check provider is logged in::

        from f5cloudsdk.provider.aws import ProviderClient

        provider_client = ProviderClient()
        provider_client.is_logged_in()
"""

from . import azure, aws

__all__ = ['azure', 'aws']
