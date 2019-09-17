""" global imports for tests - abstracts away try/except"""

import unittest
import pytest
try:
    from unittest.mock import Mock, MagicMock, PropertyMock, patch, call
except ImportError: # python 2.x support
    from mock import Mock, MagicMock, PropertyMock, patch, call

__all__ = [
    'unittest',
    'pytest',
    'Mock',
    'MagicMock',
    'PropertyMock',
    'patch',
    'call'
]
