""" Functional Test: Cloud Services Example Files """

from examples.cs_subscription import run_example as run_subscription_example
from examples.cs_beacon import run_example as run_beacon_example

def test_cs_subscription_example():
    """ Test F5CS Subscription Example """

    assert run_subscription_example().get('status').upper() == 'ACTIVE'

def test_cs_beacon_example():
    """ Test F5CS Beacon Example """

    assert run_beacon_example().get('action').upper() == 'GET'
