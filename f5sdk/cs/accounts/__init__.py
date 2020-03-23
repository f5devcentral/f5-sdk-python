"""Module for Accounts API

    Example - Show Current User::

        from f5sdk.cs.accounts import AccountClient

        account_client = SubscriptionClient(mgmt_client)

        # show current user information
        account_client.show_user()
"""

from .account import AccountClient

__all__ = [
    'AccountClient'
]
