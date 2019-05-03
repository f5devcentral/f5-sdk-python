""" Constants used throughout this package """

import logging
import tempfile

VERSION = '0.9.0' # should consolidate with setup version
USER_AGENT = 'f5cloudsdk/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()
DFL_LOG_LEVEL = logging.ERROR
LOG_LEVEL_ENV_VAR = 'F5_SDK_LOG_LEVEL'
F5_AUTH_TOKEN_HEADER = 'X-F5-Auth-Token'
