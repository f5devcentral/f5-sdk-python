""" Functional Test Cloud Services Example File """

import os

from f5sdk.exceptions import FileLoadError
from examples.cs import get_cs_config

def test_cs_example():
    """ Test get_cs_config() method """
    if not os.path.exists(os.path.join(os.getcwd(), './examples/cs.py')):
        raise FileLoadError('Example file cs.py not exists')

    # Run example
    assert get_cs_config().get('status') == 'ACTIVE'
