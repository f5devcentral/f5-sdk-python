""" Test utils.util """
from f5cloudsdk.utils import util

def test_multiply():
    assert util.multiply(2, 5) == 10
