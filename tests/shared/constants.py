""" Constants used throughout this package """

HOST = '192.0.2.1'
PORT = 443
USER = 'admin'
USER_PWD = 'admin'
TOKEN = 'token'

FULL_HOST = 'https://%s:%s' % (HOST, PORT)

MOCK = {
    'requests': 'requests.request'
}

F5_CLOUD_SERVICES = {
    'LOGIN_RESPONSE': {
        'access_token': TOKEN,
        'expires_at': 3600
    }
}
