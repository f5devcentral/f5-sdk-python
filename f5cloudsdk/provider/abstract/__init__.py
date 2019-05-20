""" Abstract base class for provider module

This helps enforce polymorphism for each cloud provider,
as well as provides a clear place to see all public methods
"""

from .imports import ABC, abstractmethod, abstractproperty

class AbstractProviderClient(ABC):
    """Abstract Class """

    @abstractmethod
    def is_logged_in(self):
        """Abstract method """

    @abstractproperty
    def virtual_machines(self):
        """Abstract property """
