""" Extension feature steps """

# pylint: disable=function-redefined, import-error
import json
from test_imports import given, when, then, fixtures, use_fixture

RETRIES = {
    'DEFAULT': 10,
    'DELAY_IN_SECS': 1
}


@given('we have a Cloud services account with beacon subscription')
def step_impl(context):
    """ step impl """
    use_fixture(fixtures.cs_management_client, context)
    assert context.cs_mgmt_client


@when('we list insights')
def step_impl(context):
    """ step impl """
    use_fixture(fixtures.cs_beacon_insights_client, context)
    context.response = context.beacon_insights_client.list()


@when('we create an insight with a declaration')
def step_impl(context, **_kwargs):
    """ step impl """
    use_fixture(fixtures.cs_beacon_insights_client, context)
    config = json.loads(context.text)
    context.response = context.beacon_insights_client.create(config=config)
    context.result = context.beacon_insights_client.show(name=config.get('title'))


@when('we update an insight with a declaration')
def step_impl(context, **_kwargs):
    """ step impl """
    use_fixture(fixtures.cs_beacon_insights_client, context)
    config = json.loads(context.text)
    context.response = context.beacon_insights_client.create(config=config)
    context.result = context.beacon_insights_client.show(name=config.get('title'))


@when('we delete a insight with title:foo')
def step_impl(context, **_kwargs):
    """ step impl """
    use_fixture(fixtures.cs_beacon_insights_client, context)
    context.response = context.beacon_insights_client.delete(name='foo', config={})
    context.list_insights = context.beacon_insights_client.list()


@when('we create an application with a declaration')
def step_impl(context, **_kwargs):
    """ step impl """
    use_fixture(fixtures.cs_beacon_declare_client, context)
    context.response = context.beacon_declare_client.create(config=json.loads(context.text))


@when('we create a token with a declaration')
def step_impl(context, **_kwargs):
    """ step impl """
    use_fixture(fixtures.cs_beacon_token_client, context)
    config = json.loads(context.text)
    context.response = context.beacon_token_client.create(config=config)
    context.result = context.beacon_token_client.show(name=config.get('name'))


@when('we list tokens')
def step_impl(context, **_kwargs):
    """ step impl """
    use_fixture(fixtures.cs_beacon_token_client, context)
    context.response = context.beacon_token_client.list()


@when('we delete a token with name "BIGIP1Token"')
def step_impl(context, **_kwargs):
    """ step impl """
    use_fixture(fixtures.cs_beacon_token_client, context)
    context.response = context.beacon_token_client.delete(name='BIGIP1Token', config={})
    context.list_tokens = context.beacon_token_client.list()


@then('an insight with {description} exists')
def step_impl(context, description):
    """ step impl """
    assert context.response.get('createTime')
    assert context.result.get('title') == 'foo'
    assert context.result.get('description') == description


@then('the insight with title:foo will be deleted')
def step_impl(context):
    """ step impl """
    for insight in context.list_insights.get('insights'):
        assert insight.get('title') != 'foo'


@then('insights will be listed')
def step_impl(context):
    """ step impl """
    assert context.response.get('insights')[0].get('title') == 'F5 Assets and Inventory'
    assert context.response.get('insights')[1].get('title') == 'F5 App Protection'


@then('an application named "{text}" will exist')
def step_impl(context, text):
    """ step impl """
    all_applications = context.beacon_declare_client.create(
        config={'action': 'get'}
    )['declaration']
    matching_applications = [
        i for i in all_applications
        if i['application']['name'] == text
    ]
    assert len(matching_applications) >= 1


@then('a token named "BIGIP1Token" is created')
def step_impl(context):
    """ step impl """
    assert context.result.get('name') == 'BIGIP1Token'
    assert context.result.get('description') == 'Token for BIG-IP1'


@then('tokens will be listed')
def step_impl(context):
    """ step impl """
    assert context.response.get('tokens')


@then('the token with name "BIGIP1Token" will be deleted')
def step_impl(context):
    """ step impl """
    for token in context.list_tokens.get('tokens'):
        assert token.get('name') != 'BIGIP1Token'
