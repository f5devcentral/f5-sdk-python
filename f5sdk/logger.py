"""Python module for logging

    Example - Basic::

        from f5sdk.logger import Logger
        logger = Logger(__name__).get_logger()

    Example - Log level set using environment variable::

        # export F5_SDK_LOG_LEVEL='INFO'
"""

import os
import logging
import f5sdk.constants as constants

DFL_LEVEL = constants.DFL_LOG_LEVEL
LEVEL_ENV_VAR = constants.ENV_VARS.get('LOG_LEVEL_ENV_VAR')
LEVEL_ENV_VAR_VAL = os.environ[LEVEL_ENV_VAR] if LEVEL_ENV_VAR in os.environ else None

# add custom trace logging level
logging.TRACE = 5
logging.addLevelName(logging.TRACE, 'TRACE')


class MyLogger(logging.getLoggerClass()):
    """ Create custom logger class """
    def trace(self, msg, *args, **kwargs):
        """ Add trace method to logger """
        self.log(logging.TRACE, msg, *args, **kwargs)


logging.setLoggerClass(MyLogger)


class Logger():
    """Class initialization

    This class is a simple wrapper around the built-in logging module functionality.

    Attributes
    ----------
    name : str
        the logger name
    level : str
        the logging level to use, such as ERROR, WARNING, INFO or DEBUG

    Methods
    -------
    get_logger()
        Refer to method documentation

    Notes
    -----
    The built-in logging module returns a pointer if the 'named' logger exists
    """

    def __init__(self, name, **kwargs):
        """Class initialization

        Parameters
        ----------
        name : str
            the logger name
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        level : str
            the logging level to use

        Returns
        -------
        None

        Notes
        -----
        If log level is not provided via kwargs it checks for a named environment
        variable, if that does not exist it uses a default log level
        """

        self.name = name
        self.level = kwargs.pop('level', LEVEL_ENV_VAR_VAL if LEVEL_ENV_VAR_VAL else DFL_LEVEL)

    def get_logger(self):
        """Get Logger

        Parameters
        ----------
        None

        Returns
        -------
        object
            instantiated logger
        """

        # create a logger + add handler and formatter
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

        return logger
