""" Constants used throughout this package """

import logging
import tempfile

VERSION = '0.9.0' # should consolidate with setup version
USER_AGENT = 'f5cloudsdk/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()
DFL_LOG_LEVEL = logging.ERROR
LOG_LEVEL_ENV_VAR = 'F5_SDK_LOG_LEVEL'
F5_AUTH_TOKEN_HEADER = 'X-F5-Auth-Token'

HTTP_TIMEOUT = {
    'DFL': 60
}
HTTP_VERIFY = False
HTTP_STATUS_CODE = {
    'OK': 200,
    'ACCEPTED': 202
}

RETRIES = {
    'DFL': 120,
    'DFL_DELAY': 1
}

BIGIP_CMDS = {
    'AUTH_LIST': '%s list auth user %s',
    'AUTH_MODIFY': '%s modify auth user %s password %s'
}

F5_CLOUD_SERVICES = {
    'API_ENDPOINT': 'api.cloudservices.f5.com',
    'AUTH_TOKEN_HEADER': 'Authorization'
}
