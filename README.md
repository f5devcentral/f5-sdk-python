[![Releases](https://img.shields.io/github/release/f5devcentral/f5-sdk-python.svg)](https://github.com/f5devcentral/f5-sdk-python/releases)
[![Issues](https://img.shields.io/github/issues/f5devcentral/f5-sdk-python.svg)](https://github.com/f5devcentral/f5-sdk-python/issues)

# Introduction

The F5 SDK (Python) provides client libraries to access various F5 products and services. It focuses primarily on facilitating consuming our most popular APIs and services, currently including BIG-IP (via Automation Tool Chain) and F5 Cloud Services.

Benefits:

- Provides hand-written or auto-generated client code to make F5’s APIs/services simple and intuitive to use.
- Handles the low-level details of communication with the API or service, including authentication sessions, async task handling, protocol handling, large file uploads, and more.
- Can be installed using familiar package management tools such as pip.

## Table of Contents
- [Usage](#usage)
- [User Documentation](#user-documentation)

## Usage

```python
""" Update BIG-IP L4-L7 configuration using AS3

Notes
-----
Set local environment variables first
"""

# export F5_SDK_HOST='192.0.2.10'
# export F5_SDK_USERNAME='admin'
# export F5_SDK_PWD='admin'
# export F5_SDK_AS3_DECL='./my_declaration.json'
# export F5_SDK_LOG_LEVEL='DEBUG'

import os

from f5sdk.bigip import ManagementClient
from f5sdk.bigip.extension import ExtensionClient
from f5sdk.logger import Logger

LOGGER = Logger(__name__).get_logger()


def update_as3_config():
    """ Update AS3 configuration

    Notes
    -----
    Includes package installation, service check while
    maintaining idempotency
    """
    # create management client
    mgmt_client = ManagementClient(
        os.environ['F5_SDK_HOST'],
        user=os.environ['F5_SDK_USERNAME'],
        password=os.environ['F5_SDK_PWD'])

    # create extension client
    as3_client = ExtensionClient(mgmt_client, 'as3')

    # Get installed package version info
    version_info = as3_client.package.is_installed()
    LOGGER.info(version_info['installed'])
    LOGGER.info(version_info['installed_version'])
    LOGGER.info(version_info['latest_version'])

    # install package
    if not version_info['installed']:
        as3_client.package.install()

    # ensure service is available
    as3_client.service.is_available()

    # configure AS3
    return as3_client.service.create(config_file=os.environ['F5_SDK_AS3_DECL'])


if __name__ == '__main__':
    LOGGER.info(update_as3_config())
```

## User Documentation

See the [documentation](https://clouddocs.f5.com/sdk/f5-sdk-python/) for details on installation, usage and much more.

## Source Repository

See the source repository [here](https://github.com/f5devcentral/f5-sdk-python).
