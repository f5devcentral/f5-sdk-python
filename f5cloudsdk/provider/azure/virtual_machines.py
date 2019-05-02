"""Python module for provider virtual machines configuration """

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

class OperationClient(object):
    """Operation client class for provider virtual machines

    Attributes
    ----------
    credentials : object
        the credentials for the provider
    subscription_id : str
        the subscription
    """

    def __init__(self, credentials, subscription_id):
        """Class initialization

        Parameters
        ----------
        credentials : object
            the credentials for the provider
        subscription_id : str
            the subscription

        Returns
        -------
        None
        """
        self.credentials = credentials
        self.subscription_id = subscription_id

    def _get_interface_details(self, interface_id):
        """Get network interface details using resource ID

        Parameters
        ----------
        interface_id : str
            the resource id of the network interface

        Returns
        -------
        dict
            a dict containing network interface details
        """

        network_client = NetworkManagementClient(self.credentials, self.subscription_id)
        # /subscriptions/<>/resourceGroups/<>/providers/Microsoft.Network/networkInterfaces/<>
        id_parsed = interface_id.split('/')
        nic_group = id_parsed[4]
        nic_name = id_parsed[8]

        nic_details = network_client.network_interfaces.get(nic_group, nic_name)
        return nic_details.as_dict()

    def _get_public_ip_details(self, public_ip_id):
        """Get public IP details using resource ID

        Parameters
        ----------
        public_ip_id : str
            the resource id of the public IP

        Returns
        -------
        dist
            a dict containing the public IP details
        """

        network_client = NetworkManagementClient(self.credentials, self.subscription_id)
        # /subscriptions/<>/resourceGroups/<>/providers/Microsoft.Network/publicIPAddresses/<>
        id_parsed = public_ip_id.split('/')
        ip_group = id_parsed[4]
        ip_name = id_parsed[8]

        return network_client.public_ip_addresses.get(ip_group, ip_name).as_dict()

    def _get_primary_interface(self, interfaces):
        """Get primary network interface details

        Resolve public IP resource ID too

        Parameters
        ----------
        interfaces : array
            an array of network interfaces for a virtual machine

        Returns
        -------
        dict
            a dict containing information about the primary network interface
        """

        key = 'public_ip_address'

        primary_interface = [i for i in interfaces if 'primary' in i and i['primary']]

        # account for scenario where there is no 'primary' key - such as azurecli basher vm
        primary_interface = primary_interface[0] if primary_interface else interfaces[0]
        primary_interface = self._get_interface_details(primary_interface['id'])

        # resolve public IP, if it exists
        for ip_config in primary_interface['ip_configurations']:
            public_ip_id = ip_config[key]['id'] if key in ip_config else None
            if public_ip_id:
                ip_config[key] = self._get_public_ip_details(public_ip_id)

        return primary_interface

    def _normalize_list_response(self, output):
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

        # resolve addresses
        network_interfaces = output['network_profile']['network_interfaces']
        primary_interface = self._get_primary_interface(network_interfaces)

        # get primary IP
        primary_ip = [i for i in primary_interface['ip_configurations'] if i['primary']][0]
        primary_private_ip = primary_ip['private_ip_address']
        # get primary public IP, if it exists
        primary_public_ip = None
        if 'public_ip_address' in primary_ip and 'ip_address' in primary_ip['public_ip_address']:
            primary_public_ip = primary_ip['public_ip_address']['ip_address']
        return {
            'name': output['name'],
            'id': output['vm_id'],
            'location': output['location'],
            'tags': output['tags'] if 'tags' in output else None,
            'privateIPAddress': primary_private_ip,
            'publicIPAddress': primary_public_ip
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

        compute_client = ComputeManagementClient(self.credentials, self.subscription_id)
        vms = [i.as_dict() for i in compute_client.virtual_machines.list_all()]

        # filter by tag, if required
        if filter_tag:
            tag_key, tag_value = filter_tag.split(':')
            vms = [i for i in vms
                   if 'tags' in i
                   and tag_key in i['tags'].keys()
                   and i['tags'][tag_key] == tag_value]
        # normalize output into standard format
        return [self._normalize_list_response(i) for i in vms]
