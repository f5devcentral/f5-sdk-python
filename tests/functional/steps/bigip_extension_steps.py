""" Extension feature steps """

# pylint: disable=function-redefined, import-error
import json
from test_imports import given, when, then, fixtures, use_fixture


@given('we have a BIG-IP available')
def step_impl(context):
    """ step impl """
    use_fixture(fixtures.bigip_management_client, context)
    assert context.mgmt_client


@given('{component} is installed')
def step_impl(context, component):
    """ step impl """
    use_fixture(fixtures.bigip_extension_client, context, component=component)
    # check if package is already installed
    if not context.extension_client.package.is_installed()['installed']:
        context.extension_client.package.install()
    context.extension_client.service.is_available()


@when('we install {component}')
def step_impl(context, component):
    """ step impl """
    use_fixture(fixtures.bigip_extension_client, context, component=component)
    # ensure package is uninstalled prior to performing installation
    if context.extension_client.package.is_installed()['installed']:
        context.extension_client.package.uninstall()
    context.extension_client.package.install()
    context.extension_client.service.is_available()


@when('we get info from {component}')
def step_impl(context, **_kwargs):
    """ step impl """
    context.exentension_client_info = context.extension_client.service.show_info()


@when('we configure {component} with a declaration')
def step_impl(context, **_kwargs):
    """ step impl """
    context.extension_client.service.create(config=json.loads(context.text))


@then('{component} will be installed')
def step_impl(context, **_kwargs):
    """ step impl """
    assert context.extension_client.package.is_installed()['installed']


@then('{component} will return a version')
def step_impl(context, **_kwargs):
    """ step impl """
    if isinstance(context.exentension_client_info, list):
        context.exentension_client_info = context.exentension_client_info[0]
    assert context.exentension_client_info['version'] != ''


@then('a virtual server will be created with address {virtual_address}')
def step_impl(context, virtual_address):
    """ step impl """
    virtual_servers = context.mgmt_client.make_request('/mgmt/tm/ltm/virtual')['items']
    match = [i for i in virtual_servers
             if i['destination'].split('/')[-1].split(':')[0] == virtual_address
            ]
    assert len(match) == 1, virtual_servers
