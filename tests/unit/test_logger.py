""" Test logger module """

## project imports ##
from f5cloudsdk.logger import Logger
## unittest imports ##
from ..global_test_imports import Mock

LOGGER_NAME = 'testlogger'

class TestBigIp(object):
    """ Test case """

    def test_logger_can_log(self):
        """ Test logger can log """
        logger = Logger(LOGGER_NAME).get_logger()
        logger._log = Mock(return_value='foo')
        logger.error('foo')
        logger._log.assert_called_with(40, 'foo', ())
