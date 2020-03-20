""" Functional Test Cloud Services Example File """

import os

from f5sdk.exceptions import FileLoadError
from examples.cloud_services import get_cs_config

def test_cloud_services_example():
    """ Test get_cs_config() method """
    if not os.path.exists(os.path.join(os.getcwd(), './examples/cloud_services.py')):
        raise FileLoadError('Example file cloud_services.py not exists')

    # Run example
    assert get_cs_config().get('status') == 'ACTIVE'
