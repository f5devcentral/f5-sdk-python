""" Local imports - abstracts away if/else """

import sys
import abc
from abc import abstractmethod, abstractproperty

if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta('ABC', (), {})

__all__ = ['ABC', 'abstractmethod', 'abstractproperty']
