"""Module for Beacon Insights

    Example - List Insights::

        from f5sdk.cs.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.list()

    Example - Create/Update Insights::

        from f5sdk.cs.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.create(config=insight_info)

    Example - Get Insight::

        from f5sdk.cs.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.show(name=example-insight)

    Example - Delete Insight::

        from f5sdk.cs.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.delete(name=example-insight)
"""

from .insights import InsightsClient

__all__ = [
    'InsightsClient'
]
