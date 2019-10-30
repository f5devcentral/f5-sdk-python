""" Test provider module """

# project imports
from f5cloudsdk import provider
# unittest imports
from ...global_test_imports import Mock

DFL_VAL = 'foo'
DFL_TAGS = {'Name': 'foo'}
DFL_IP = '192.0.2.1'
DFL_PUB_IP = '1.1.1.1'


class TestProviderAws(object):
    """Test Class: provider module (azure) """

    @staticmethod
    def test_virtual_machines_list(mocker):
        """Test: virtual_machines.list()

        Assertions
        ----------
        - virtual_machines.list() response should equal expected value(s)
        """

        mock_session = mocker.patch('f5cloudsdk.provider.aws.Session')

        _response = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': DFL_VAL,
                            'Placement': {
                                'AvailabilityZone': DFL_VAL
                            },
                            'PrivateIpAddress': DFL_IP,
                            'PublicIpAddress': DFL_PUB_IP,
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': DFL_VAL
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        mock_compute_client = mock_session.return_value.client.return_value
        mock_compute_client.describe_instances = Mock(return_value=_response)

        provider_client = provider.aws.ProviderClient(
            access_key='id',
            secret_key='secret',
            region_name='us-west-1'
        )

        vms = provider_client.virtual_machines.list()

        assert mock_session.called
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
