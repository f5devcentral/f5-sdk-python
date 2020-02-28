""" Extension feature steps """

# pylint: disable=function-redefined, import-error
import json
from retry import retry
from test_imports import given, when, then, fixtures, use_fixture

RETRIES = {
    'DEFAULT': 10,
    'DELAY_IN_SECS': 1
}

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
def step_impl(context, component, **_kwargs):
    """ step impl """
    config = json.loads(context.text)

    if component == 'cf':
        config['environment'] = context.deployment_info['environment']
        config['externalStorage']['scopingTags']['f5_cloud_failover_label'] \
            = context.deployment_info['deploymentId']
        config["failoverAddresses"]["scopingTags"]["f5_cloud_failover_label"] \
            = context.deployment_info['deploymentId']
        config["failoverRoutes"]["scopingTags"]["f5_cloud_failover_label"] \
            = context.deployment_info['deploymentId']

    elif component == 'do':
        current_decl = context.mgmt_client.make_request('/mgmt/shared/declarative-onboarding')
        current_decl = current_decl['declaration']
        # note: creating/updating "db vars" in "Common"
        current_decl['Common']['dbVars'].update(config)
        # note: account for local/remote password being removed from DO (ID: TBD)
        if 'trust' in current_decl['Common']:
            password = [
                i for i in context.deployment_info['instances']
                if i['primary']][0]['admin_password']
            current_decl['Common']['trust']['localPassword'] = password
            current_decl['Common']['trust']['remotePassword'] = password
        config = current_decl

    context.extension_client.service.create(config=config)


@when('we get inspect from {component}')
def step_impl(context, **_kwargs):
    """ step impl """
    context.response = context.extension_client.service.show_inspect()

@when('we post reset to {component}')
def step_impl(context, **_kwargs):
    """ step impl """
    context.response = context.extension_client.service.reset()

@when('we post trigger to {component}')
def step_impl(context, **_kwargs):
    """ step impl """
    context.response = context.extension_client.service.trigger()

@when('we call get trigger from {component}')
def step_impl(context, **_kwargs):
    """ step impl """
    context.response = context.extension_client.service.show_trigger()

@then('{component} will be installed')
def step_impl(context, **_kwargs):
    """ step impl """
    context.response = context.extension_client.package.is_installed()['installed']

@then('{component} will return a version')
def step_impl(context, **_kwargs):
    """ step impl """
    if isinstance(context.exentension_client_info, list):
        context.exentension_client_info = context.exentension_client_info[0]
    assert context.exentension_client_info['version'] != ''

@then('a virtual server will be created with address {virtual_address}')
@retry(tries=RETRIES['DEFAULT'], delay=RETRIES['DELAY_IN_SECS'])
def step_impl(context, virtual_address):
    """ step impl """
    virtual_servers = context.mgmt_client.make_request('/mgmt/tm/ltm/virtual')['items']
    match = [i for i in virtual_servers
             if i['destination'].split('/')[-1].split(':')[0] == virtual_address
            ]
    assert len(match) == 1, virtual_servers

@then('cf will validate and return response')
def step_impl(context, **_kwargs):
    """ step impl """
    assert context.response.get('message')

@then('a success message is returned by {component}')
def step_impl(context, **_kwargs):
    """ step impl """
    body = context.extension_client.service.show()
    assert body.get('message') == 'success'

@then('{component} will return inspect info')
def step_impl(context, **_kwargs):
    """ step impl """
    if isinstance(context.response, list):
        context.response = context.extension_client.service.show_inspect()[0]
        assert context.response

@then('advisory text will be set to "{text}"')
def step_impl(context, text):
    """ step impl """
    assert context.mgmt_client.make_request(
        '/mgmt/tm/sys/db/ui.advisory.text'
    )['value'] == text
