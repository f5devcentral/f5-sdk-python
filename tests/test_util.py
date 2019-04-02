# import packages
import datetime
import os, sys
sys.path.append(os.getcwd()) # TODO: fix this import process

from f5cloudsdk.shared import util

def test_multiply():
    assert util.multiply(2, 5) == 10
