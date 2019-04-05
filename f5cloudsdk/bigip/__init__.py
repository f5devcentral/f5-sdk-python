""" Module for BIG-IP configuration

    Example(s):

    from f5cloudsdk.bigip import ManagementClient
    device = ManagementClient('192.0.2.10', user='admin', password='admin')

    # get BIG-IP info (version, etc.)
    device.get_info()

"""

# TODO: abstract this out into util lib that handles authn/authz
import requests
from requests.auth import HTTPBasicAuth

def check_auth(function):
    """ Decorator function to check authentication """
    def wrapper(self, *args, **kwargs):
        if self.device_token is None:
            raise Exception('Device authentication must be performed first')
        return function(self, *args, **kwargs)
    return wrapper

class ManagementClient():
    """ Management client class for BIG-IP """
    def __init__(self, host, **kwargs):
        self.host = host
        self.user = kwargs.pop('user', '') # conditional
        self.password = kwargs.pop('password', '') # conditional
        self.private_key = kwargs.pop('private_key', '') # conditional
        self.device_token = None

        if self.user and self.password:
            self._login_using_credentials()
        elif self.private_key:
            self._login_using_key()
        else:
            raise Exception('user/password credentials or private key required')

    def _get_token(self):
        """ Login (using user/password credentials) """
        url = 'https://%s/mgmt/shared/authn/login' % (self.host)
        body = {
            'username': self.user,
            'password': self.password,
            'loginProviderName': 'tmos' # implement other providers
        }
        response = requests.post(
            url,
            json=body,
            auth=HTTPBasicAuth(self.user, self.password),
            verify=False
        ).json()
        return response['token']['token']

    def _login_using_credentials(self):
        """ Login (using user/password credentials) """
        self.device_token = self._get_token()
        return True

    def _login_using_key(self):
        """ Login (using private key) """

    @check_auth
    def get_info(self):
        """ BIG-IP info (version) """
        url = 'https://%s/mgmt/tm/sys/version' % (self.host)
        response = requests.get(
            url,
            headers={
                'X-F5-Auth-Token': self.device_token
            },
            verify=False
        ).json()

        v_0 = 'https://localhost/mgmt/tm/sys/version/0'
        version = response['entries'][v_0]['nestedStats']['entries']['Version']['description']
        return {'version': version}
