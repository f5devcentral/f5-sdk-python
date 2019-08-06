""" Test logger module """

# project imports
from f5cloudsdk.logger import Logger
# unittest imports
from ..global_test_imports import Mock

LOGGER_NAME = 'testlogger'


class TestLogger(object):
    """Test Class: logger module """

    def test_logger_can_log(self):
        """Test: logger can log

        Assertions
        ----------
        - _log method should be called with 40, 'foo'
        """
        logger = Logger(LOGGER_NAME).get_logger()
        logger._log = Mock()
        logger.error('foo')
        logger._log.assert_called_with(40, 'foo', ())

    def test_logger_with_custom_trace_level(self):
        """Test: logger can log with custom trace level

        Assertions
        ----------
        - _log method should be called with 5, 'foo'
        """
        logger = Logger(LOGGER_NAME, level='TRACE').get_logger()
        logger._log = Mock()
        logger.trace('foo')
        logger._log.assert_called_with(5, 'foo', ())
