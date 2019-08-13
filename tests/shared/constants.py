""" Constants used throughout this package """

HOST = '192.0.2.1'
PORT = 443
USER = 'admin'
USER_PWD = 'admin'
TOKEN = 'token'
CUSTOM_API_ENDPOINT = 'some_custom_endpoint'
DEFAULT_API_ENDPOINT = 'api.cloudservices.f5.com'

FULL_HOST = 'https://%s:%s' % (HOST, PORT)

MOCK = {
    'requests': 'requests.request'
}

F5_CLOUD_SERVICES = {
    'LOGIN_RESPONSE': {
        'access_token': TOKEN,
        'expires_at': 3600
    },
    'CUSTOM_API_ENDPOINT' : CUSTOM_API_ENDPOINT,
    'DEFAULT_API_ENDPOINT' : DEFAULT_API_ENDPOINT
}
