""" Test provider module """

# project imports
from f5cloudsdk import provider
# unittest imports
from ...global_test_imports import Mock

DFL_VAL = 'foo'
DFL_TAGS = {'foo': 'bar'}
DFL_IP = '192.0.2.1'
DFL_PUB_IP = '1.1.1.1'


class ResponseItem(object):
    """ mock response item """
    def __init__(self, response):
        self.response = response

    def as_dict(self):
        """ mock function """
        return self.response


class TestProviderAzure(object):
    """Test Class: provider module (azure) """

    def test_virtual_machines_list(self, mocker):
        """Test: virtual_machines.list()

        Assertions
        ----------
        - virtual_machines.list() response should equal expected value(s)
        """

        mocker.patch('f5cloudsdk.provider.azure.ServicePrincipalCredentials')
        mock_compute_client = mocker.patch(
            'f5cloudsdk.provider.azure.virtual_machines.ComputeManagementClient')
        mock_network_client = mocker.patch(
            'f5cloudsdk.provider.azure.virtual_machines.NetworkManagementClient')

        # compute client response
        _response = [
            {
                'name': DFL_VAL,
                'vm_id': DFL_VAL,
                'location': DFL_VAL,
                'tags': DFL_TAGS,
                'network_profile': {
                    'network_interfaces': [
                        {
                            'primary': True,
                            'id': '/s/<>/rG/<>/p/M.N/nI/<>'
                        }
                    ]
                }
            }
        ]
        response = [ResponseItem(i) for i in _response]
        mock_compute_client.return_value.virtual_machines.list_all = Mock(return_value=response)

        # network client network_interfaces.get response
        _response = {
            'ip_configurations': [
                {
                    'primary': True,
                    'private_ip_address': DFL_IP,
                    'public_ip_address': {
                        'id': '/s/<>/rG/<>/p/M.N/nI/<>'
                    }
                }
            ]
        }
        response = ResponseItem(_response)
        mock_network_client.return_value.network_interfaces.get = Mock(return_value=response)

        # network client public_ip_addresses.get response
        _response = {
            'ip_address': DFL_PUB_IP
        }
        response = ResponseItem(_response)
        mock_network_client.return_value.public_ip_addresses.get = Mock(return_value=response)

        provider_client = provider.azure.ProviderClient(
            client_id='client_id',
            tenant_id='tenant_id',
            secret='secret',
            subscription_id='subscription_id'
        )

        vms = provider_client.virtual_machines.list()

        assert vms == [
            {
                'name': DFL_VAL,
                'id': DFL_VAL,
                'location': DFL_VAL,
                'tags': DFL_TAGS,
                'privateIPAddress': DFL_IP,
                'publicIPAddress': DFL_PUB_IP
            }
        ]
