"""Module for BIG-IQ licensing

    Example - Assignments::

        from f5sdk.bigiq import ManagementClient
        from f5sdk.bigiq.licensing import AssignmentClient

        device = ManagementClient('192.0.2.10', user='admin', password='admin')

        license_client = AssignmentClient(device)

        # list license assignments
        license_client.list()
"""

from .assignments import AssignmentClient

__all__ = [
    'AssignmentClient'
]
