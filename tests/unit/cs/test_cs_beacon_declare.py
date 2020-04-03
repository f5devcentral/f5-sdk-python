""" Test module """

from f5sdk.cs.beacon.declare import DeclareClient

from ...global_test_imports import pytest
from .. import utils


class TestDeclare(object):
    """Test Class: cs.beacon.declare module """

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_crud_operations(mgmt_client, mocker):
        """Test: CRUD operation functions

        Assertions
        ----------
        - response should match mocked return value
        """

        utils.validate_crud_operations(
            DeclareClient(mgmt_client),
            mocker=mocker,
            methods=['create']
        )

    @staticmethod
    @pytest.mark.usefixtures("mgmt_client")
    def test_create_async(mgmt_client, mocker):
        """Test: Create with an async 'taskReference'

        Assertions
        ----------
        - create() response should equal taskReference response
        - make_request() should be called twice
        - make_request() second call uri should equal task uri
        """

        declare_client = DeclareClient(mgmt_client)

        mock_response = {'action': 'deploy', 'status': 'Completed'}
        make_request_mock = mocker.patch(
            'f5sdk.utils.http_utils.make_request',
            side_effect=[
                ({'taskReference': 'https://localhost/declare-task/1234'}, 200),
                (mock_response, 200)
            ]
        )

        assert declare_client.create(config={'action': 'deploy'}) == mock_response
        assert make_request_mock.call_count == 2
        args, _ = make_request_mock.call_args_list[1]
        assert args[1] == '/declare-task/1234'
