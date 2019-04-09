""" Constants used throughout this package """

import tempfile

VERSION = '0.9.0' # should consolidate with setup version
USER_AGENT = 'f5cloudsdk/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()
