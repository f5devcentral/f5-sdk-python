"""Module for Beacon Insights

    Example - List Insights::

        from f5sdk.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.list()

    Example - Create/Update Insights::

        from f5sdk.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.createOrUpdate(insight=insight_info)

    Example - Get Insight::

        from f5sdk.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.show(title=example-insight)

    Example - Delete Insight::

        from f5sdk.beacon.insights import InsightClient

        insight_client = InsightClient(mgmt_client)
        insight_client.delete(title=example-insight)
"""

from .insight import InsightsClient

__all__ = [
    'InsightsClient'
]
