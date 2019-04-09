""" Module for BIG-IP configuration

    Example(s):

    from f5cloudsdk.bigip import ManagementClient
    device = ManagementClient('192.0.2.10', user='admin', password='admin')

    # get BIG-IP info (version, etc.)
    device.get_info()

"""

import json
import requests
from requests.auth import HTTPBasicAuth

def check_auth(function):
    """ Decorator function to check authentication """
    # TODO: need to support refreshing the token - here or elsewhere
    def wrapper(self, *args, **kwargs):
        if self.token is None:
            raise Exception('Device authentication required')
        return function(self, *args, **kwargs)
    return wrapper

class ManagementClient():
    """ Management client class for BIG-IP """
    def __init__(self, host, **kwargs):
        self.host = host
        self.user = kwargs.pop('user', '')
        self.password = kwargs.pop('password', '')
        self.private_key = kwargs.pop('private_key', '')
        self.token = None

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
            'loginProviderName': 'tmos' # need to support other providers
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
        self.token = self._get_token()
        return True

    def _login_using_key(self):
        """ Login (using private key) """

    def get_info(self):
        """ BIG-IP info (version) """
        uri = '/mgmt/tm/sys/version'
        response = self.make_request(uri)

        v_0 = 'https://localhost/mgmt/tm/sys/version/0'
        version = response['entries'][v_0]['nestedStats']['entries']['Version']['description']
        return {'version': version}

    @check_auth
    def make_request(self, uri, **kwargs):
        """ Make request (HTTP) """
        host = self.host
        uri = uri
        method = kwargs.pop('method', 'GET').lower()
        headers = {'X-F5-Auth-Token': self.token} # TODO: add user agent
        # add any user-supplied headers, allow the user to override default headers
        headers.update(kwargs.pop('headers', {}))
        # check for body, normalize
        body = kwargs.pop('body', None)
        body_content_type = kwargs.pop('body_content_type', 'json') # json (default), raw
        if body and body_content_type == 'json':
            headers.update({'Content-Type': 'application/json'})
            body = json.dumps(body)

        # construct url
        url = 'https://%s%s' % (host, uri)
        # make request
        response = requests.request(
            method,
            url,
            headers=headers,
            data=body,
            verify=False
        )
        # check response code
        response.raise_for_status()

        return response.json()

    @check_auth
    def make_request_ssh(self):
        """ Make request (SSH) """
