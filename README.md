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

## Filing Issues and Getting Help

If you come across a bug or other issue when using the SDK, use [GitHub Issues](https://github.com/f5devcentral/f5-sdk-python/issues) to submit an issue for our team.  You can also see the current known issues on that page, which are tagged with a Known Issue label.  

F5 SDK is community-supported. For more information, see the [Support page](SUPPORT.md).

## Copyright

Copyright 2014-2020 F5 Networks Inc.

### F5 Networks Contributor License Agreement

Before you start contributing to any project sponsored by F5 Networks, Inc. (F5) on GitHub, you will need to sign a Contributor License Agreement (CLA).  

If you are signing as an individual, we recommend that you talk to your employer (if applicable) before signing the CLA since some employment agreements may have restrictions on your contributions to other projects. Otherwise by submitting a CLA you represent that you are legally entitled to grant the licenses recited therein.  

If your employer has rights to intellectual property that you create, such as your contributions, you represent that you have received permission to make contributions on behalf of that employer, that your employer has waived such rights for your contributions, or that your employer has executed a separate CLA with F5.

If you are signing on behalf of a company, you represent that you are legally entitled to grant the license recited therein. You represent further that each employee of the entity that submits contributions is authorized to submit such contributions on behalf of the entity pursuant to the CLA.
