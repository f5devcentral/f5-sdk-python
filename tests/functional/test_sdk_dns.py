"""Functional test for SDK BIG-IP DNS"""

import os
import re

from f5cloudsdk.bigip.toolchain import ToolChainClient
from f5cloudsdk.logger import Logger
from f5cloudsdk.bigip.dns import DataCentersClient, ServersClient, PoolsClient

LOGGER = Logger(__name__).get_logger()


def test_management_client(management_client):
    """Validate management client connection by check version on a BIG-IP"""
    version_info = management_client.get_info()
    assert re.search('[0-9].[0-9]+', version_info['version']), 'Validate managemennt client failed'


def test_toolchain_as3(management_client):
    """Validate toolchain client and create the following DNS objects using AS3
    . A data center named SDKDataCenter
    . A server named SDKServer with one device
    . VirtualServerDiscoveryMode set to allow Service Discovery
    . ExposeRouteDomainsEnabled set to true
    . A pool named SDKPool and set resourceRecordType to "A"
    """
    # Validate toolchain client created and installed
    as3_client = ToolChainClient(management_client, 'as3')
    version_info = as3_client.package.is_installed()
    if not version_info['installed']:
        as3_client.package.install()
    # Validate service is available
    assert as3_client.service.is_available(), 'Validate AS3 service available failed'

    # Configure DNS objects using AS3 extension
    as3_client.service.create(config_file=os.path.join(os.path.dirname(__file__),\
                                "dns_declaration.json"))

def validate_create(dicts):
    """"Validate create objects"""
    create_obj = dicts['object'].create(config=dicts['create'])
    assert create_obj['name'] in dicts['name'],\
            ('Validate create {} failed.'.format(dicts['name']))


def validate_list(dicts):
    """"Validate list objects"""
    if 'items' not in dicts['object'].list() or not dicts['object'].list()['items']:
        assert False, "Expected name: {} in items".format(dicts['name'])
    else:
        for item in dicts['object'].list()['items']:
            if item['name'] == dicts['name']:
                break
        else:
            assert False, "Validate list {} failed ".format(dicts['name'])


def validate_update(dicts):
    """Validate update objects"""
    update_obj = dicts['object'].update(name=dicts['name'], config=dicts['update'])
    assert update_obj['description'] in "Updated",\
            ('Validate update {} failed.'.format(dicts['name']))


def validate_delete(dicts):
    """"Validate delete objects"""
    delete_obj = dicts['object'].delete(name=dicts['name'])
    assert not delete_obj, 'Validate delete {} failed.'.format(dicts['name'])


def validate_crud_operations(dicts):
    """Validate CRUD SDK DNS"""
    for method in ('create', 'list', 'update', 'delete'):
        if 'create' in method:
            validate_create(dicts)
        if 'list' in method:
            validate_list(dicts)
        if 'update' in method:
            validate_update(dicts)
        if 'delete' in method:
            validate_delete(dicts)


def test_datacenter(management_client):
    """Validate CRUD datacenter"""
    datac = {"name": "SDKDataCenter1", "object": DataCentersClient(management_client),
             "create": {"name": "SDKDataCenter1"}, "update": {"description": "Updated"}}
    validate_crud_operations(datac)


def test_server(management_client):
    """Validate CRUD server"""
    datac = {"name": "SDKDataCenter1", "object": DataCentersClient(management_client),
             "create": {"name": "SDKDataCenter1"}, "update": {"description": "Updated"}}
    cserver = {"name": "SDKServer1", "datacenter": "SDKDataCenter1",
               "exposeRouteDomains": "no", "virtualServerDiscovery": "enabled",
               "addresses": [{"name": "10.0.1.1", "deviceName": "sdkbigipmv0",
                              "translation": "none"}]}
    server = {"name": "SDKServer1", "object": ServersClient(management_client),
              "create": cserver, "update": {"description": "Updated",
                                            "datacenter": "SDKDataCenter1"}}
    validate_create(datac)
    validate_crud_operations(server)
    validate_delete(datac)


def test_pool(management_client):
    """Validate CRUD pool"""
    pool = {'name': 'SDKPool1', 'object': PoolsClient(management_client, uri='/a'),
            'create': {"name": "SDKPool1"}, 'update': {"description": "Updated"}}
    validate_crud_operations(pool)
