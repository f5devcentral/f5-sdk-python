"""Module for Beacon Declarative API

    Example - Get Declaration (Applications, Monitors, etc.)::

        from f5sdk.cs.beacon.declare import DeclareClient

        declare_client = DeclareClient(mgmt_client)
        declare_client.create(config={'action': 'get'})

    Example - Create Application::

        from f5sdk.cs.beacon.declare import DeclareClient

        declare_client = DeclareClient(mgmt_client)
        declare_client.create(config={
            'action': 'deploy',
            'declaration': [
                {
                    'application': {
                        'name': 'Test Application',
                        'description': 'Test Description',
                        'labels':{ 'test_label': 'test_value'},
                        'dependencies': [],
                        'metrics': []
                    }
                }
            ]
        })

    Example - Create Monitor::

        from f5sdk.cs.beacon.declare import DeclareClient

        declare_client = DeclareClient(mgmt_client)
        declare_client.create(config={
            'action': 'deploy',
            'declaration': [
                {
                    'monitor': {
                        'name': 'Test Monitor',
                        'description': 'Test Description',
                        'url': 'http://example.com',
                        'method': 'HEAD',
                        'interval': '30',
                        'type': 'MONITOR_TYPE_HEALTH_CHECK'
                    }
                }
            ]
        })
"""

from .declare import DeclareClient

__all__ = [
    'DeclareClient'
]
