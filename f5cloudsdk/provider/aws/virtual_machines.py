"""Python module for provider virtual machines configuration """

from ..abstract.virtual_machines import AbstractOperationClient

class OperationClient(AbstractOperationClient):
    """Operation client class for provider virtual machines

    Attributes
    ----------
    session : object
        the session for the provider
    """

    def __init__(self, session, region_name):
        """Class initialization

        Parameters
        ----------
        session : object
            the session for the provider
        region_name : str
            the region name for the provider

        Returns
        -------
        None
        """
        self.session = session
        self.region_name = region_name

    @staticmethod
    def _normalize_list_response(output):
        """Normalize output from virtual machines list response

        Parameters
        ----------
        output : object
            the virtual machine output object

        Returns
        -------
        dict
            a dict containing information about the virtual machine
        """

        tags = {i['Key']:i['Value'] for i in output['Tags']} if 'Tags' in output else None
        private_ip = output['PrivateIpAddress'] if 'PrivateIpAddress' in output else ''
        public_ip = output['PublicIpAddress'] if 'PublicIpAddress' in output else ''

        return {
            'name': tags['Name'] if tags and 'Name' in tags else '',
            'id': output['InstanceId'],
            'location': output['Placement']['AvailabilityZone'],
            'tags': tags,
            'privateIPAddress': private_ip,
            'publicIPAddress': public_ip
        }

    def list(self, **kwargs):
        """List

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        filter_tag : str
            filter list by tag (key:value)

        Returns
        -------
        list
            contains zero or more virtual machines::

                [{
                    'name': '',
                    'id': '',
                    'location': '',
                    'tags': {},
                    'privateIPAddress': '',
                    'publicIPAddress': ''
                }]

        """
        filter_tag = kwargs.pop('filter_tag', None)

        vms = []

        compute_client = self.session.client('ec2', region_name=self.region_name)
        instances = compute_client.describe_instances()

        # 'Reservations (array)' -> 'Instances (array)' -> 'Instance (dict)'
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                vms.append(instance)

        # filter by tag, if required
        if filter_tag:
            tag_key, tag_value = filter_tag.split(':')
            vms = [i for i in vms
                   if 'Tags' in i and i['Tags']
                   for tag in i['Tags']
                   if tag['Key'] == tag_key and tag['Value'] == tag_value]

        # normalize output into standard format
        return [self._normalize_list_response(i) for i in vms]
