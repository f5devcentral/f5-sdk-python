""" Test logger module """
import unittest
try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError:
    # python 2.x support
    from mock import Mock, MagicMock, patch

from f5cloudsdk.logger import Logger

LOGGER_NAME = 'testlogger'

# pylint: disable=protected-access

class TestBigIp(unittest.TestCase):
    """ Test case """

    def test_logger_can_log(self):
        """ Test logger can log """
        logger = Logger(LOGGER_NAME).get_logger()
        logger._log = MagicMock(return_value='foo')
        logger.error('foo')
        logger._log.assert_called_with(40, 'foo', ())
