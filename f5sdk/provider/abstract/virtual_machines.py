""" Abstract base class for provider.virtual_machines module """

from .imports import ABC, abstractmethod


class AbstractOperationClient(ABC):
    """Abstract Class """

    @abstractmethod
    def list(self, **kwargs):
        """Abstract method """
