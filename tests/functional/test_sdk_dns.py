"""Functional test for SDK BIG-IP DNS"""

import os
import re

from f5sdk.bigip.extension import ExtensionClient
from f5sdk.logger import Logger
from f5sdk.bigip.dns import DataCentersClient, ServersClient, PoolsClient

LOGGER = Logger(__name__).get_logger()


DATAC = {"name": "SDKDataCenter1", "create": {"name": "SDKDataCenter1"},
         "update": {"description": "Updated"}}
CSERVER = {"name": "SDKServer1", "datacenter": "SDKDataCenter1",
           "exposeRouteDomains": "no", "virtualServerDiscovery": "enabled",
           "addresses": [{"name": "10.0.1.1", "deviceName": "sdkbigipmv0",
                          "translation": "none"}]}
SERVER = {"name": "SDKServer1", "create": CSERVER,
          "update": {"description": "Updated", "datacenter": "SDKDataCenter1"}}
POOL1 = {"name": "SDKPool1", "create": {"name": "SDKPool1"},
         "update": {"description": "Updated"}}
POOL2 = {"name": "SDKPoolNAPTR", "create": {"name": "SDKPoolNAPTR"},
         "update": {"description": "Updated"}}


def test_management_client(management_client):
    """Validate management client connection by check version on a BIG-IP"""
    version_info = management_client.get_info()
    assert re.search('[0-9].[0-9]+', version_info['version']), 'Validate managemennt client failed'


def test_extension_as3(management_client):
    """Validate extension client and create the following DNS objects using AS3
    . A data center named SDKDataCenter
    . A server named SDKServer with one device
    . VirtualServerDiscoveryMode set to allow Service Discovery
    . ExposeRouteDomainsEnabled set to true
    . A pool named SDKPool and set resourceRecordType to "A"
    """
    # Validate extension client created and installed
    as3_client = ExtensionClient(management_client, 'as3')
    version_info = as3_client.package.is_installed()
    if not version_info['installed']:
        as3_client.package.install()
    # Validate service is available
    assert as3_client.service.is_available(), 'Validate AS3 service available failed'

    # Configure DNS objects using AS3 extension
    as3_client.service.create(config_file=os.path.join(os.path.dirname(__file__),
                                                       "dns_declaration.json"))
    # Validate DNS objects created by AS3 extension
    datac = {'name': 'SDKDataCenter', 'object': DataCentersClient(management_client)}
    server = {'name': 'SDKServer', 'object': ServersClient(management_client)}
    pool = {'name': 'SDKPool', 'object': PoolsClient(management_client, record_type='/a')}
    for obj in (datac, server, pool):
        validate_list(obj)


def validate_create(dicts):
    """"Validate create objects"""
    create_obj = dicts['object'].create(config=dicts['create'])
    assert create_obj['name'] in dicts['name'], ('Validate create {} failed.'.format(dicts['name']))


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
    assert update_obj['description'] in "Updated", ('Validate update {} failed.'
                                                    .format(dicts['name']))


def validate_delete(dicts):
    """"Validate delete objects"""
    delete_obj = dicts['object'].delete(name=dicts['name'])
    assert not delete_obj, 'Validate delete {} failed.'.format(dicts['name'])


def validate_show(dicts):
    """"Validate show objects"""
    show_obj = dicts['object'].show(name=dicts['name'])
    assert show_obj['name'] in dicts['name'], 'Validate show{} failed.'.format(dicts['name'])


def validate_crud_operations(dicts):
    """Validate CRUD SDK DNS"""
    for method in ('create', 'list', 'update', 'show', 'delete'):
        if 'create' in method:
            validate_create(dicts)
        elif 'list' in method:
            validate_list(dicts)
        elif 'update' in method:
            validate_update(dicts)
        elif 'delete' in method:
            validate_delete(dicts)
        else:
            validate_show(dicts)


def test_datacenter(management_client):
    """Validate CRUD datacenter"""
    DATAC.update({"object": DataCentersClient(management_client)})
    validate_crud_operations(DATAC)


def test_server(management_client):
    """Validate CRUD server"""
    DATAC.update({"object": DataCentersClient(management_client)})
    SERVER.update({'object': ServersClient(management_client)})
    validate_create(DATAC)
    validate_crud_operations(SERVER)
    validate_delete(DATAC)


def test_pool(management_client):
    """Validate CRUD pool"""
    POOL1.update({'object': PoolsClient(management_client, record_type='/a')})
    validate_crud_operations(POOL1)


def test_dns_create(management_client):
    """Validate create datacenter, server, and pool with various record types"""
    DATAC.update({"object": DataCentersClient(management_client)})
    SERVER.update({'object': ServersClient(management_client)})
    POOL1.update({'object': PoolsClient(management_client, record_type='/a')})
    POOL2.update({'object': PoolsClient(management_client, record_type='/naptr')})
    for obj in (DATAC, SERVER, POOL1, POOL2):
        validate_create(obj)


def test_dns_delete(management_client):
    """Validate delete pool, server, and datacenter"""
    DATAC.update({"object": DataCentersClient(management_client)})
    SERVER.update({'object': ServersClient(management_client)})
    POOL1.update({'object': PoolsClient(management_client, record_type='/a')})
    POOL2.update({'object': PoolsClient(management_client, record_type='/naptr')})
    for obj in (POOL1, POOL2, SERVER, DATAC):
        validate_delete(obj)
