""" Constants used throughout this package """

import logging
import tempfile
import operator

VERSION = '0.9.2'
USER_AGENT = 'f5sdk/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()
DFL_LOG_LEVEL = logging.WARNING
F5_AUTH_TOKEN_HEADER = 'X-F5-Auth-Token'
HTTPS_REQUEST_WARNING_VALUE = 'ignore:Unverified HTTPS request'
HTTP_TIMEOUT = {
    'DFL': 60
}
HTTP_VERIFY = False
HTTP_STATUS_CODE = {
    'OK': 200,
    'ACCEPTED': 202,
    'BAD_REQUEST_BODY': 'code: 400',
    'FAILED_AUTHENTICATION': 'code: 401'
}

RETRIES = {
    'DEFAULT': 60,
    'LONG': 300,
    'DELAY_IN_SECS': 1
}

COMPARISON_OPERATORS = {
    'greaterThanOrEqual': operator.ge,
    'lessThanOrEqual': operator.le
}

BIGIP_CMDS = {
    'AUTH_LIST': '%s list auth user %s',
    'AUTH_MODIFY': '%s modify auth user %s password %s'
}

F5_CS = {
    'API_ENDPOINT': 'api.cloudservices.f5.com',
    'AUTH_TOKEN_HEADER': 'Authorization'
}

ENV_VARS = {
    'LOG_LEVEL_ENV_VAR': 'F5_SDK_LOG_LEVEL',
    'DISABLE_SSL_WARNINGS': 'F5_DISABLE_SSL_WARNINGS'
}
