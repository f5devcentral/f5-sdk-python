"""Helper utilities for unit tests"""

from ..global_test_imports import Mock
from ..shared import constants

REQ = constants.MOCK['requests']


def set_default_crud_kwargs(method):
    """ Set default crud operation kwargs"""

    kwargs = {}
    if method in ['show', 'update', 'delete']:
        kwargs['name'] = 'foo'
    if method in ['create', 'update']:
        kwargs['config'] = {'foo': 'bar'}
    return kwargs


def validate_crud_operations(client, **kwargs):
    """Validate CRUD operations

    Parameters
    ----------
    client : object
        client to perform operations against
    **kwargs :
        optional keyword arguments

    Keyword Arguments
    -----------------
    methods : list
        list of methods to check
    mocker : object
        mocker to use

    Returns
    -------
    None
    """

    methods = kwargs.pop('methods', ['list', 'create', 'show', 'update', 'delete'])
    mocker = kwargs.pop('mocker', None)

    for method in methods:
        mock_response = {
            'items': [
                {
                    'foo': 'bar'
                }
            ]
        }
        mocker.patch(REQ).return_value.json = Mock(return_value=mock_response)

        kwargs = set_default_crud_kwargs(method)
        assert getattr(client, method)(**kwargs) == mock_response
