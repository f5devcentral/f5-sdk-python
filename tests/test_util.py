""" Test utils.util """
from f5cloudsdk.utils import util

def test_multiply():
    """ Test util.multiply """
    assert util.multiply(2, 5) == 10
