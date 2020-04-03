"""Module for Beacon Declarative API

    Example - Get Application(s)::

        from f5sdk.cs.beacon.declare import DeclareClient

        declare_client = DeclareClient(mgmt_client)
        declare_client.create(config={'action': 'deploy', 'declaration': []})

    Example - Create Application(s)::

        from f5sdk.cs.beacon.declare import DeclareClient

        declare_client = DeclareClient(mgmt_client)
        declare_client.create(config={'action': 'deploy', 'declaration': []})
"""

from .declare import DeclareClient

__all__ = [
    'DeclareClient'
]
