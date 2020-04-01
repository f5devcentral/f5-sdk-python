"""Beacon management client
"""


from f5sdk.logger import Logger


class ManagementClient(object):
    """A class used as a management client for Beacon
    """

    def __init__(self, host, **kwargs):
        """Class initialization

        Returns
        -------
        None
        """

        self.logger = Logger(__name__).get_logger()
