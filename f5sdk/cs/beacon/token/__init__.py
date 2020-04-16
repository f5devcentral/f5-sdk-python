"""Module for Beacon Token

    Example - List Token::

        from f5sdk.cs.beacon.token import TokenClient

        token_client = TokenClient(mgmt_client)
        token_client.list()

    Example - Create Token::

        from f5sdk.cs.beacon.token import TokenClient

        token_client = TokenClient(mgmt_client)
        token_client.create(config=token_info)

    Example - Get Token::

        from f5sdk.cs.beacon.token import TokenClient

        token_client = TokenClient(mgmt_client)
        token_client.show(name=example-token)

    Example - Delete Token::

        from f5sdk.cs.beacon.token import TokenClient

        token_client = TokenClient(mgmt_client)
        token_client.delete(name=example-token)
"""

from .token import TokenClient

__all__ = [
    'TokenClient'
]
